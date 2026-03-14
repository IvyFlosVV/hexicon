import sqlite3
from collections import Counter

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


def get_db_connection():
    """Connect to hexicon.db and return a connection with Row factory."""
    conn = sqlite3.connect("hexicon.db")
    conn.row_factory = sqlite3.Row
    return conn


def initialize_db():
    """Create ui_elements table if it doesn't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ui_elements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            element_type TEXT NOT NULL,
            tags TEXT,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def get_trending_tags(rows, top_n=5):
    """Extract tag strings from rows, count frequency, return top N tag names."""
    counts = Counter()
    for row in rows:
        tags_str = (row["tags"] or "").strip()
        for tag in tags_str.split(","):
            t = tag.strip()
            if t:
                counts[t] += 1
    return [tag for tag, _ in counts.most_common(top_n)]


def _query_is_subsequence_of_text(query: str, text: str) -> bool:
    """True if every character of query appears in text in order (allows typos / missing chars)."""
    if not query or not text:
        return not query
    q = query.lower()
    t = text.lower()
    i = 0
    for c in q:
        j = t.find(c, i)
        if j == -1:
            return False
        i = j + 1
    return True


@app.route("/")
def index():
    """Index page: list ui_elements (filtered by search if provided), trending tags, and analytics."""
    search_query = request.args.get("q", "").strip()
    search_type = request.args.get("type", "name")
    if search_type not in ("name", "tags"):
        search_type = "name"

    conn = get_db_connection()

    if search_query and search_type == "name":
        pattern = f"%{search_query.lower()}%"
        rows_by_substring = conn.execute(
            "SELECT * FROM ui_elements WHERE LOWER(name) LIKE ?",
            (pattern,),
        ).fetchall()
        seen_ids = {r["id"] for r in rows_by_substring}
        rows_all_for_fuzzy = conn.execute("SELECT * FROM ui_elements").fetchall()
        rows_extra = [
            r
            for r in rows_all_for_fuzzy
            if r["id"] not in seen_ids
            and _query_is_subsequence_of_text(search_query, r["name"] or "")
        ]
        rows_filtered = list(rows_by_substring) + rows_extra
    elif search_query and search_type == "tags":
        tag_pattern = f"%{search_query.lower()}%"
        rows_filtered = conn.execute(
            "SELECT * FROM ui_elements WHERE LOWER(COALESCE(tags, '')) LIKE ?",
            (tag_pattern,),
        ).fetchall()
    else:
        rows_filtered = conn.execute("SELECT * FROM ui_elements").fetchall()

    rows_all = conn.execute("SELECT * FROM ui_elements").fetchall()
    conn.close()

    trending_tags = get_trending_tags(rows_all)
    total_items = len(rows_all)
    css_count = sum(1 for r in rows_all if (r["element_type"] or "").strip().lower() == "css")
    css_percentage = int(round(css_count / total_items * 100)) if total_items else 0
    top_tag = trending_tags[0] if trending_tags else "None"

    return render_template(
        "index.html",
        items=rows_filtered,
        trending_tags=trending_tags,
        total_items=total_items,
        css_percentage=css_percentage,
        top_tag=top_tag,
        search_query=search_query,
        search_type=search_type,
    )


@app.route("/create", methods=["GET", "POST"])
def create():
    """GET: show create form. POST: insert new item and redirect to index."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        raw_type = request.form.get("element_type", "").strip().lower()
        tags = request.form.get("tags", "").strip()
        content = request.form.get("content", "").strip()
        if not name or raw_type not in ("color", "css") or not content:
            return redirect(url_for("create"))
        element_type = "Color" if raw_type == "color" else "CSS"
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO ui_elements (name, element_type, tags, content) VALUES (?, ?, ?, ?)",
            (name, element_type, tags, content),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("create.html")


def _editor_initial_for_item(item):
    """Build initial editor content. For CSS, wrap in a minimal HTML template."""
    raw = (item["content"] or "").strip()
    elem_type = (item["element_type"] or "").lower()
    if elem_type == "css":
        return (
            "<!DOCTYPE html>\n<html>\n<head>\n<style>\n"
            "html, body { background-color: transparent !important; }\n"
            ".card {\n  "
            + raw
            + "\n}\n</style>\n</head>\n<body>\n<div class=\"card\">Sample Header<br>This element is styled by your snippet.</div>\n</body>\n</html>"
        )
    return raw


@app.route("/preview/<int:id>")
def preview(id):
    """Show the Visual Sandbox for the item with the given ID."""
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM ui_elements WHERE id = ?", (id,)).fetchone()
    conn.close()
    if row is None:
        return redirect(url_for("index"))
    editor_initial = _editor_initial_for_item(row)
    return render_template("preview.html", item=row, editor_initial=editor_initial)


@app.route("/delete/<int:id>", methods=["POST"])
def delete_item(id):
    """Delete the item with the given ID and redirect to index."""
    conn = get_db_connection()
    conn.execute("DELETE FROM ui_elements WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    """GET: show edit form. POST: update item and redirect to index."""
    conn = get_db_connection()
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        raw_type = request.form.get("element_type", "").strip().lower()
        tags = request.form.get("tags", "").strip()
        content = request.form.get("content", "").strip()
        if not name:
            conn.close()
            return redirect(url_for("edit", id=id))
        if raw_type not in ("color", "css"):
            conn.close()
            return redirect(url_for("edit", id=id))
        element_type = "Color" if raw_type == "color" else "CSS"
        if not content:
            conn.close()
            return redirect(url_for("edit", id=id))
        conn.execute(
            "UPDATE ui_elements SET name = ?, element_type = ?, tags = ?, content = ? WHERE id = ?",
            (name, element_type, tags, content, id),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    row = conn.execute("SELECT * FROM ui_elements WHERE id = ?", (id,)).fetchone()
    conn.close()
    if row is None:
        return redirect(url_for("index"))
    return render_template("edit.html", item=row)


if __name__ == "__main__":
    initialize_db()
    app.run(debug=True)
