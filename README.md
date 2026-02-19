# shahil-sk.github.io CMS

A custom offline Content Management System built with PySide6 (Qt) to manage the [shahil-sk.github.io](https://github.com/shahil-sk/shahil-sk.github.io) portfolio website.

## Features
- **Post Management**: Create, edit, and delete Markdown blog posts with frontmatter support.
- **Profile Editor**: Graphical editor for `data.json` (Hero, About, Experience, etc.).
- **Build System**: Trigger the site's build script directly from the UI.
- **Git Integration**: Commit and push changes without leaving the app.

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/shahil-sk/portfolio-cms.git
   cd portfolio-cms
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # venv\Scripts\activate   # Windows
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

4. On first run, go to the **Settings** tab and select your local clone of `shahil-sk.github.io`.
