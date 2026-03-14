# Hexicon

**Hexicon** is a premium, developer-centric library designed for managing UI components and color palettes. Moving beyond a simple storage system, Hexicon serves as an interactive digital sandbox where code, color, and materiality converge.

## Core Features

* **Subsequence Fuzzy Search**: A high-performance, typo-tolerant search engine built on a subsequence matching algorithm. It ensures precise resource retrieval even with partial or slightly inaccurate inputs.
* **Interactive Live Sandbox**: A real-time rendering playground integrated with the `iro.js` engine, allowing users to manipulate background environments and observe CSS component behavior simultaneously.
* **Analytics Dashboard**: A data-driven overview of your design assets, providing real-time statistics on resource volume, CSS dominance, and trending tags.
* **IDE-Grade Workspace**: A specialized sub-page layout featuring a "Control Tower" sidebar and a scrollable code editor with a sticky preview stage for high-efficiency editing.

## Technical Stack

* **Backend**: Flask (Python), SQLite
* **Frontend**: HTML5, CSS3 (Advanced 3D Shaders & Transforms), Vanilla JavaScript
* **Engines**: `iro.js` for dynamic color picking

## Design Philosophy: The "Mercury" System

The visual identity of Hexicon is defined by a modern interpretation of **Skeuomorphism**, focusing on physical materiality and spatial stability.

* **Liquid Metal Typography**: The primary headers utilize layered text-shadow stacking and linear-gradient keyframe animations to simulate the 3D thickness and fluid motion of liquid mercury.
* **Forged Iron UI Elements**: Action buttons are engineered with heavy metallic gradients and multi-layered inner shadows to provide a sense of weight and tactile feedback.
* **Spatial Consistency**: The interface adheres to a "Zero-Baseline" alignment logic. The back-navigation, titles, and content cards share a unified coordinate system across the Home, Preview, and Edit pages to eliminate visual jumpiness during transitions.
* **Glassmorphism**: Component containers utilize high-index blur filters and semi-transparent borders to maintain a deep, immersive dark-mode aesthetic.

## Installation & Setup

1.  **Clone the Repository**:
    ```bash
    git clone [https://github.com/IvyFlosVV/Hexicon.git](https://github.com/IvyFlosVV/Hexicon.git)
    cd Hexicon
    ```

2.  **Environment Configuration**:
    It is recommended to use a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install flask
    ```

3.  **Run the Application**:
    ```bash
    python app.py
    ```
    Access the system at `http://127.0.0.1:5000`.

## Collaborative Acknowledgement

This project was developed using an **AI-Human Collaborative Workflow**.
* **Design & Engineering**: Ivy Weng
* **Collaborative Partners**: Cursor & Gemini

---

<p align="center">
  <small>Crafted with Cursor & Gemini</small>
</p>
