# site_generator.py

*Auto-generated from `.github/scripts/site_generator.py`*

# site_generator.py – Static Site Generator for Documentation

## Overview

`site_generator.py` is a lightweight, self‑contained static site generator written in Python.  
It scans a `docs/` directory for Markdown files, converts each file to HTML, and writes a fully‑styled site into `docs-site/`.  
The generated site includes:

* A dark‑mode CSS theme (based on GitHub’s dark theme)
* Syntax highlighting via **highlight.js**
* Mermaid diagram support via **mermaid.js**
* A sidebar navigation that automatically highlights the current page
* Breadcrumbs and a “last‑updated” timestamp

The script is intentionally simple – it can be dropped into any repository that contains Markdown documentation and run with a single command.

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `DOCS_DIR` | `Path` | Path to the source Markdown directory (`docs/`). |
| `SITE_DIR` | `Path` | Path to the output directory (`docs-site/`). |
| `HTML_TEMPLATE` | `str` | Jinja‑style template used to wrap each page’s content. |
| `CSS_STYLES` | `str` | CSS stylesheet applied to all pages. |
| `build_site()` | `function` | Main entry point that builds the entire site. |
| `__main__` block | – | Executes `build_site()` when the script is run directly. |

> **Note** – The module does not expose any classes or interfaces; everything is procedural.

---

## Usage Examples

### 1. Run the script from the command line

```bash
# Ensure you have the required dependencies
pip install markdown

# Build the site
python site_generator.py
```

After execution you’ll find a fully‑rendered site in `docs-site/`. Open `docs-site/index.html` in a browser to view it.

### 2. Call `build_site()` from another Python script

```python
# my_build_script.py
from site_generator import build_site

# Optionally change the source or output directories
# from pathlib import Path
# DOCS_DIR = Path('my_docs')
# SITE_DIR = Path('my_site')

build_site()
```

### 3. Customizing the source or output directories

```python
# Override the constants before calling build_site()
from site_generator import DOCS_DIR, SITE_DIR, build_site
from pathlib import Path

DOCS_DIR = Path('custom_docs')
SITE_DIR = Path('public')

build_site()
```

### 4. Adding a custom CSS file

Create a file named `custom.css` in the same directory as the script and modify `CSS_STYLES`:

```python
# site_generator.py
CSS_STYLES = """
/* Your custom styles here */
"""
```

The generated site will use your styles instead of the default dark theme.

---

## Parameters

| Function | Parameter | Type | Description |
|----------|-----------|------|-------------|
| `build_site()` | *none* | – | The function does not accept any arguments. It uses the module‑level constants `DOCS_DIR` and `SITE_DIR`. |

> If you need to change the source or output directories, modify the constants before calling `build_site()`.

---

## Return Values

| Function | Return Value | Description |
|----------|--------------|-------------|
| `build_site()` | `None` | The function writes files to disk and prints status messages. It does not return any value. |

---

## Detailed Behavior

1. **Check for source directory**  
   If `DOCS_DIR` does not exist, the script prints an error and exits.

2. **Clean the output directory**  
   Any existing `SITE_DIR` is removed (`shutil.rmtree`) and recreated.

3. **Write the CSS**  
   `CSS_STYLES` is written to `SITE_DIR/styles.css`.

4. **Discover Markdown files**  
   All `*.md` files in `DOCS_DIR` are sorted alphabetically.

5. **Generate navigation**  
   For each page, a sidebar list is built. The current page link receives the CSS class `active`.

6. **Convert Markdown to HTML**  
   Uses the `markdown` library with `fenced_code` and `tables` extensions.  
   If the library is missing, a fallback renders the raw text inside a `<pre>` tag and prints a warning.

7. **Render the page**  
   `HTML_TEMPLATE` is formatted with:
   * `title` – the file stem (e.g., `getting-started`)
   * `nav_links` – the per‑page navigation list
   * `breadcrumbs` – a simple “Docs > <page>” string
   * `date` – current date (`YYYY‑MM‑DD`)
   * `content` – the converted Markdown

8. **Write the page**  
   Each page is written as `<name>.html` inside `SITE_DIR`.

9. **Generate the index**  
   * If `docs/README.md` exists, it is used as the home page (currently a placeholder – you can replace the logic to convert it).
   * Otherwise, the first Markdown file is copied as `index.html`.

10. **Finish**  
    A final message prints the location of the built site.

---

## Customization Tips

| What to change | Where to change | Example |
|----------------|-----------------|---------|
| **Source directory** | `DOCS_DIR` | `DOCS_DIR = Path('my_docs')` |
| **Output directory** | `SITE_DIR` | `SITE_DIR = Path('public')` |
| **CSS theme** | `CSS_STYLES` | Replace the default dark theme with your own CSS. |
| **Template** | `HTML_TEMPLATE` | Add meta tags, analytics, or modify the layout. |
| **Date format** | `datetime.now().strftime(...)` | Use `'%B %d, %Y'` for a different format. |
| **Navigation** | The loop that builds `page_nav` | Add icons or nested lists. |
| **Index page** | The `if (DOCS_DIR / 'README.md').exists():` block | Convert `README.md` to HTML instead