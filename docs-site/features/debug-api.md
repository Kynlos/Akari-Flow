---
title: Debug Api
layout: default
---

# debug_api.py

*Auto-generated from `debug_api.py`*

# `debug_api.py`

> A tiny demo that exercises the **tree_sitter** Python bindings.  
> It shows two ways to create a `Parser` for Python source code and prints the
> resulting syntax tree.

---

## 1. Overview

`debug_api.py` is **not** a library – it is a self‑contained script that
illustrates how to:

1. Load the Python language definition from `tree_sitter_python`.
2. Create a `Language` object.
3. Instantiate a `Parser` (either via constructor or by setting the
   `language` property later).
4. Parse a short Python snippet (`"def foo(): pass"`).
5. Print the root node of the parsed tree.

The script is useful for debugging or learning the `tree_sitter` API
behaviour, especially when you need to know whether the constructor
or the property‑assignment approach works on a particular platform.

---

## 2. Exports

| Export | Type | Description |
|--------|------|-------------|
| **None** | – | The module contains only top‑level code; it does not expose any
functions, classes, or interfaces for import. |

> If you want to reuse the parsing logic, copy the relevant blocks into your
> own module or wrap them in a function.

---

## 3. Usage Examples

### 3.1 Run the script directly

```bash
$ python debug_api.py
Testing API usage...
Language created
Parser created via constructor
Parsed successfully via constructor
<tree_sitter.Node: root>
```

If the constructor fails (e.g., on a platform where the shared library
cannot be loaded), the fallback path will be executed:

```bash
$ python debug_api.py
Testing API usage...
Constructor failed: <error message>
Parser language set via property
Parsed successfully via property
<tree_sitter.Node: root>
```

### 3.2 Re‑use the logic in your own code

```python
import tree_sitter
import tree_sitter_python

def parse_python(source: bytes) -> tree_sitter.Tree:
    """Parse Python source and return the syntax tree."""
    lang = tree_sitter.Language(tree_sitter_python.language())
    parser = tree_sitter.Parser(lang)
    return parser.parse(source)

tree = parse_python(b"def foo(): pass")
print(tree.root_node)
```

---

## 4. Parameters & Return Values

Below is a quick reference for the key `tree_sitter` classes and methods
used in the script.

| Function / Method | Parameters | Return Value | Notes |
|-------------------|------------|--------------|-------|
| `tree_sitter.Language(language_bytes)` | `bytes` – raw language definition (e.g. `tree_sitter_python.language()`) | `Language` instance | Raises `OSError` if the shared library cannot be loaded. |
| `tree_sitter.Parser(language=None)` | `Language` or `None` | `Parser` instance | If `None`, the `language` property must be set before parsing. |
| `Parser.language` | `Language` | `Language` | Property; can be set after construction. |
| `Parser.parse(source_bytes)` | `bytes` – source code | `Tree` | Parses the source and returns a syntax tree. |
| `Tree.root_node` | – | `Node` | The root node of the parsed tree. |
| `tree_sitter_python.language()` | – | `bytes` | Returns the compiled language definition for Python. |

---

## 5. Error Handling

The script uses a `try/except` block to demonstrate two common failure
scenarios:

1. **Constructor failure** – e.g., the shared library is missing or
   incompatible.  
   The fallback creates a `Parser` without a language and assigns it later.

2. **Property‑assignment failure** – e.g., the `Parser` object does not
   accept a language after construction.  
   The script prints the exception message for debugging.

Feel free to adapt the error handling to your own needs (e.g., logging,
re‑raising, or graceful degradation).

---

### TL;DR

- **What it does** – Demonstrates how to load the Python language, create a
  parser, parse a snippet, and print the syntax tree.
- **Exports** – None (pure demo script).
- **How to use** – Run the file or copy the parsing logic into your own
  module.
- **Key API calls** – `Language`, `Parser`, `parse`, `root_node`.
