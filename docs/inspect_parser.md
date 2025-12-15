# inspect_parser.py

*Auto-generated from `inspect_parser.py`*

# inspect_parser.py

> A lightweight helper script that introspects the `tree_sitter.Parser` class.  
> It prints the public attributes of the class and attempts to instantiate it without arguments, reporting any errors that occur.

---

## 1. Overview

`inspect_parser.py` is a **stand‑alone script** (not a library) that:

1. Imports the `tree_sitter` package.
2. Prints the list of attributes/methods available on `tree_sitter.Parser`.
3. Tries to create a `Parser` instance with no arguments.
4. Prints the instance’s attributes if construction succeeds, or the exception message if it fails.

The script is useful for quick sanity checks when working with the `tree_sitter` Python bindings, especially to confirm that the `Parser` class is available and can be instantiated in the current environment.

---

## 2. Exports

| Export | Type | Description |
|--------|------|-------------|
| **None** | – | The module does **not** expose any functions, classes, or variables for import. It only runs code at import time. |

> Because the module is intended to be executed directly (`python inspect_parser.py`), it has no public API to document.

---

## 3. Usage Examples

### 3.1 Running the script from the command line

```bash
$ python inspect_parser.py
```

**Typical output** (may vary depending on the `tree_sitter` version):

```
['Parser', 'Language', 'Node', 'Tree', 'TreeCursor', ...]
Parser instantiated without args
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', ...]
```

If the `Parser` cannot be instantiated (e.g., missing native bindings), you’ll see:

```
Parser() failed: <error message>
```

### 3.2 Importing the script in another Python file

> **Caution:** Importing will immediately execute the script and print to stdout.

```python
# main.py
import inspect_parser  # This will run the introspection code
```

The import will produce the same output as running the script directly.

---

## 4. Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| **None** | – | The script takes no command‑line arguments or function parameters. |

---

## 5. Return Values

| Function | Return Value | Notes |
|----------|--------------|-------|
| `print` statements | `None` | All output is sent to `stdout`. |
| `tree_sitter.Parser()` | `Parser` instance | Returned only if the constructor succeeds; otherwise an exception is raised and caught. |

> The module itself does not return a value; its side effect is printing information to the console.

---

## 6. Dependencies

- `tree_sitter` (Python bindings for the Tree‑Sitter parsing library).  
  Install via `pip install tree_sitter`.

---

## 7. Notes & Common Issues

| Issue | Explanation | Fix |
|-------|-------------|-----|
| `ImportError: No module named tree_sitter` | The `tree_sitter` package is not installed. | Run `pip install tree_sitter`. |
| `AttributeError: module 'tree_sitter' has no attribute 'Parser'` | The bindings were compiled without the `Parser` component. | Re‑install or rebuild the `tree_sitter` package with the correct options. |
| `RuntimeError: Failed to load language` | The native library for the language you plan to parse is missing. | Load the language using `Language.build_library(...)` before creating a `Parser`. |

---

## 8. License

This file is part of the `tree_sitter` ecosystem and is released under the same license as the `tree_sitter` Python bindings. Refer to the `tree_sitter` project for details.