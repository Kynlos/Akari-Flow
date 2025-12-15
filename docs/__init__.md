# __init__.py

*Auto-generated from `.github/scripts/polyglot/__init__.py`*

# Polyglot Analysis Package – `__init__.py`

> **File**: `__init__.py`  
> **Purpose**: Package initializer for the Polyglot Analysis library, powered by Tree‑sitter.

---

## 1. Overview

`__init__.py` is the entry point for the **Polyglot Analysis** package.  
It sets up the package namespace and provides a high‑level description of the library.  
The package itself is built on top of **Tree‑sitter**, a fast incremental parsing system, and offers a set of tools for analyzing source code written in multiple programming languages.

> **Key points**
> - Acts as a namespace for the package.
> - Contains a module‑level docstring that describes the package.
> - No executable code or public API is defined here; all functionality resides in sub‑modules.

---

## 2. Exports

| Export | Type | Description |
|--------|------|-------------|
| **None** | – | This module does not expose any functions, classes, or interfaces directly. All public APIs are provided by sub‑modules such as `polyglot_analysis.parser`, `polyglot_analysis.analyzer`, etc. |

> **Tip**: Import sub‑modules directly to access the library’s functionality, e.g. `from polyglot_analysis import parser`.

---

## 3. Usage Examples

Below are practical examples of how to use the package from a consumer script.  
These examples assume the package is installed and available on your `PYTHONPATH`.

### 3.1 Importing the Package

```python
# Import the package root (no direct exports)
import polyglot_analysis

# Import a specific sub‑module
from polyglot_analysis import parser
```

### 3.2 Using a Sub‑Module (Example: `parser`)

```python
from polyglot_analysis.parser import parse_source

source_code = """
def hello_world():
    print("Hello, world!")
"""

tree = parse_source(source_code, language="python")
print(tree.root_node.type)  # e.g., 'module'
```

### 3.3 Using Another Sub‑Module (Example: `analyzer`)

```python
from polyglot_analysis.analyzer import analyze_tree

analysis = analyze_tree(tree)
print(analysis.metrics)  # e.g., {'lines_of_code': 3, 'functions': 1}
```

> **Note**: The actual API of sub‑modules may vary; refer to their dedicated documentation for detailed usage.

---

## 4. Parameters

Since `__init__.py` contains no functions or classes, there are no parameters to document here.

---

## 5. Return Values

No functions or classes are defined in this module, so there are no return values to describe.

---

## 6. Additional Notes

- **Tree‑sitter Integration**: The package relies on the Tree‑sitter library for parsing. Ensure that the appropriate language grammars are installed (e.g., `tree-sitter-python`, `tree-sitter-javascript`).
- **Extensibility**: New language parsers or analysis tools can be added as sub‑modules within the `polyglot_analysis` package.
- **Testing**: Run the test suite with `pytest` from the package root to verify all sub‑modules work correctly.

---

**Happy coding!**