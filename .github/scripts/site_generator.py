#!/usr/bin/env python3
"""
Static Site Generator for Documentation
"""

import os
import sys
import shutil
import markdown
from pathlib import Path
from datetime import datetime

DOCS_DIR = Path('docs')
SITE_DIR = Path('docs-site')

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - CI/CD Docs</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/github-dark.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>
        hljs.highlightAll();
        mermaid.initialize({ startOnLoad: true, theme: 'dark' });
    </script>
</head>
<body class="dark-mode">
    <div class="app-container">
        <aside class="sidebar">
            <div class="logo">
                <h2>📚 Docs</h2>
            </div>
            <nav>
                <ul>
                    <li><a href="index.html" class="{active_index}">Home</a></li>
                    {nav_links}
                </ul>
            </nav>
        </aside>
        <main class="content">
            <header>
                <div class="breadcrumbs">{breadcrumbs}</div>
                <div class="last-updated">Updated: {date}</div>
            </header>
            <article class="markdown-body">
                {content}
            </article>
        </main>
    </div>
</body>
</html>
"""

CSS_STYLES = """
:root {
    --bg-primary: #0d1117;
    --bg-secondary: #161b22;
    --text-primary: #c9d1d9;
    --text-secondary: #8b949e;
    --accent: #58a6ff;
    --border: #30363d;
}

body {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    background-color: var(--bg-primary);
    color: var(--text-primary);
}

.app-container {
    display: flex;
    min-height: 100vh;
}

.sidebar {
    width: 280px;
    background-color: var(--bg-secondary);
    border-right: 1px solid var(--border);
    padding: 1rem;
    position: fixed;
    height: 100vh;
    overflow-y: auto;
}

.logo {
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1rem;
}

nav ul {
    list-style: none;
    padding: 0;
}

nav li {
    margin-bottom: 0.5rem;
}

nav a {
    color: var(--text-secondary);
    text-decoration: none;
    display: block;
    padding: 0.5rem;
    border-radius: 6px;
    transition: all 0.2s;
}

nav a:hover, nav a.active {
    background-color: rgba(56, 139, 253, 0.1);
    color: var(--accent);
}

.content {
    margin-left: 280px;
    padding: 2rem;
    width: 100%;
    max-width: 900px;
}

header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 2rem;
    color: var(--text-secondary);
    font-size: 0.9rem;
}

.markdown-body {
    line-height: 1.6;
}

.markdown-body h1 { border-bottom: 1px solid var(--border); padding-bottom: 0.3em; }
.markdown-body h2 { border-bottom: 1px solid var(--border); padding-bottom: 0.3em; margin-top: 1.5em; }
.markdown-body code { background-color: rgba(110,118,129,0.4); padding: 0.2em 0.4em; border-radius: 6px; }
.markdown-body pre { background: #161b22; padding: 16px; border-radius: 6px; overflow: auto; }
.markdown-body pre code { background: none; padding: 0; }
.markdown-body blockquote { border-left: 4px solid var(--border); color: var(--text-secondary); padding-left: 1em; }
.markdown-body table { border-collapse: collapse; width: 100%; }
.markdown-body th, .markdown-body td { border: 1px solid var(--border); padding: 6px 13px; }
.markdown-body tr:nth-child(2n) { background-color: #161b22; }

/* Mermaid */
.mermaid {
    background-color: #161b22;
    padding: 1rem;
    border-radius: 6px;
    display: flex;
    justify-content: center;
}
"""

def build_site():
    if not DOCS_DIR.exists():
        print("No docs directory found")
        return

    # Clean output
    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
    SITE_DIR.mkdir()

    # Write CSS
    with open(SITE_DIR / 'styles.css', 'w', encoding='utf-8') as f:
        f.write(CSS_STYLES)

    # Get Markdown files
    md_files = sorted(list(DOCS_DIR.glob('*.md')))
    
    # Generate Nav
    nav_links = ""
    for md_file in md_files:
        name = md_file.stem
        nav_links += f'<li><a href="{name}.html" class="{{active_{name}}}">{name}</a></li>'

    # Process files
    for md_file in md_files:
        name = md_file.stem
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Convert MD to HTML (using basic parsing or library if available)
        # Using markdown library if installed, else fallback to basic replacement
        try:
            html_content = markdown.markdown(content, extensions=['fenced_code', 'tables'])
        except:
            # Simple fallback
            html_content = f"<pre>{content}</pre>"
            print("Warning: 'markdown' lib not found, using raw text")

        # HTML Template
        final_html = HTML_TEMPLATE.format(
            title=name,
            active_index="",
            nav_links=nav_links.format(**{f"active_{name}": "active", **{f"active_{o.stem}": "" for o in md_files if o != md_file}}),
            breadcrumbs=f"Docs > {name}",
            date=datetime.now().strftime('%Y-%m-%d'),
            content=html_content
        )
        
        # Clean up format strings for other inactive links (hacky but works for simple case)
        # Actually the f-string approach above is complex. Let's simplify.
        
        # Simpler Nav Generation per page
        page_nav = ""
        for n in md_files:
            active = "active" if n.stem == name else ""
            page_nav += f'<li><a href="{n.stem}.html" class="{active}">{n.stem}</a></li>'
            
        final_html = HTML_TEMPLATE.format(
            title=name,
            active_index="",
            nav_links=page_nav,
            breadcrumbs=f"Docs > {name}",
            date=datetime.now().strftime('%Y-%m-%d'),
            content=html_content
        )

        with open(SITE_DIR / f"{name}.html", 'w', encoding='utf-8') as f:
            f.write(final_html)
            
        print(f"Generated {name}.html")

    # Generate Index (Copy README or first doc)
    index_content = "<h1>Welcome to CI/CD Docs</h1><p>Select a page from the sidebar.</p>"
    if (DOCS_DIR / 'README.md').exists(): # If docs has readme
        # Use that
        pass
    elif len(md_files) > 0:
        # Use first file
         shutil.copy(SITE_DIR / f"{md_files[0].stem}.html", SITE_DIR / "index.html")

    print(f"Site built in {SITE_DIR}")

if __name__ == '__main__':
    # Need markdown package
    try:
        import markdown
    except ImportError:
        os.system('pip install markdown')
        import markdown
        
    build_site()
