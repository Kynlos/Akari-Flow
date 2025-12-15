---
title: Inspect Query
layout: default
---

# inspect_query.py

*Auto-generated from `inspect_query.py`*

# inspect_query.py

> A lightweight introspection script that demonstrates how to build a **Tree‑Sitter** query for Python, inspect the resulting query object, and parse a simple Python snippet.  
> The script is intentionally minimal – it runs on import and prints diagnostic information to `stdout`.

---

## 1. Overview

| Feature | What it does |
|---------|--------------|
| **Language loading** | Loads the built‑in Tree‑Sitter Python grammar (`tree_sitter_python.language()`) and creates a `Language` instance. |
| **Query construction** | Builds a query that captures the name of every `function_definition` node (`(function_definition name: (identifier) @name.definition)`). |
| **Introspection** | Prints the attributes/methods of the `Query` object (`dir(query)`). |
| **Parser usage** | Instantiates a `Parser` with the loaded language, parses a tiny Python snippet (`"def foo(): pass"`), and stores the resulting syntax tree. |
| **Feature detection** | Checks whether the `Query` object implements the `captures` or `matches` methods and prints a message if found. |
| **Error handling** | Wraps everything in a `try/except` block and prints a friendly error message if anything goes wrong. |

> **Why use this script?**  
> It’s a quick sanity‑check for developers who are learning the Tree‑Sitter API or debugging query syntax. The printed output shows you the exact API surface of the `Query` object and whether you can use the newer `captures`/`matches` helpers.

---

## 2. Exports

> This module does **not** expose any public functions, classes, or interfaces.  
> All logic runs at import time and writes to `stdout`.

| Export | Type | Notes |
|--------|------|-------|
| *None* | – | The module only performs side‑effects when imported or executed. |

---

## 3. Usage Examples

### 3.1 Run as a script

```bash
python inspect_query.py
```

You should see output similar to:

```
Query object methods:
['captures', 'matches', 'match', 'match_all', 'pattern', ...]
Has captures method
Has matches method
```

> The exact list of methods will depend on the Tree‑Sitter version you have installed.

### 3.2 Import in another module

```python
# other_module.py
import inspect_query  # The script runs automatically on import
```

> Importing will trigger the same diagnostics. If you want to avoid side‑effects, wrap the logic in a function or guard it with `if __name__ == "__main__":`.

---

## 4. Parameters

> The script contains **no functions or methods** that accept parameters.  
> All values are hard‑coded:

| Variable | Value | Purpose |
|----------|-------|---------|
| `query_src` | `"(function_definition name: (identifier) @name.definition)"` | The Tree‑Sitter query string. |
| `source_code` | `b"def foo(): pass"` | The byte string parsed by the `Parser`. |

---

## 5. Return Values

| Function | Return |
|----------|--------|
| `tree_sitter.Language` constructor | A `Language` instance representing the Python grammar. |
| `lang.query(query_src)` | A `Query` object that can be used to match against syntax trees. |
| `parser.parse(...)` | A `Tree` object representing the parsed syntax tree. |
| `hasattr(query, 'captures')` / `hasattr(query, 'matches')` | Boolean values indicating the presence of those methods. |

> All other operations are side‑effects (printing to the console). No values are returned to the caller.

---

## 6. Extending the Script

If you want to turn this into a reusable helper, consider refactoring:

```python
def build_python_query() -> tree_sitter.Query:
    lang = tree_sitter.Language(tree_sitter_python.language())
    query_src = "(function_definition name: (identifier) @name.definition)"
    return lang.query(query_src)

def parse_python(code: str) -> tree_sitter.Tree:
    lang = tree_sitter.Language(tree_sitter_python.language())
    parser = tree_sitter.Parser(lang)
    return parser.parse(code.encode())

if __name__ == "__main__":
    query = build_python_query()
    tree = parse_python("def foo(): pass")
    print(dir(query))
```

This keeps the public API clean while preserving the original introspection logic.
