---
title: Inspect Ts Binding
layout: default
---

# inspect_ts_binding.py

*Auto-generated from `inspect_ts_binding.py`*

# inspect_ts_binding.py

> A lightweight script that demonstrates how to inspect the **tree_sitter_typescript** binding.  
> It prints the public API of the module and shows the types returned by the two language factory functions.

---

## Overview

`inspect_ts_binding.py` is a **demo script** that:

1. Imports the `tree_sitter_typescript` package.
2. Prints the list of attributes and functions exposed by the package (`dir()`).
3. Calls the two language‑factory functions:
   * `language_typescript()` – returns a `Language` instance for plain TypeScript.
   * `language_tsx()` – returns a `Language` instance for TSX (TypeScript + JSX).
4. Prints the Python type of each returned object, handling any errors gracefully.

This script is useful for developers who want to quickly verify that the `tree_sitter_typescript` binding is correctly installed and to see what objects are available.

---

## Exports

The script itself does **not** export any symbols.  
It relies on the following public functions from the `tree_sitter_typescript` package:

| Function | Description |
|----------|-------------|
| `language_typescript()` | Returns a `Language` object for TypeScript. |
| `language_tsx()` | Returns a `Language` object for TSX. |

> **Note:** These functions are part of the `tree_sitter_typescript` package, not the script.

---

## Usage Examples

### 1. Running the Script

```bash
python inspect_ts_binding.py
```

Typical output:

```
['__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'language_tsx', 'language_typescript', ...]
TypeScript type: <class 'tree_sitter.Language'>
TSX type: <class 'tree_sitter.Language'>
```

### 2. Importing and Using the Functions Manually

```python
import tree_sitter_typescript

# Get the TypeScript language
ts_lang = tree_sitter_typescript.language_typescript()
print(f"TypeScript Language: {ts_lang}")

# Get the TSX language
tsx_lang = tree_sitter_typescript.language_tsx()
print(f"TSX Language: {tsx_lang}")
```

### 3. Handling Errors

If the binding is not compiled correctly, the functions may raise an exception. The script catches these and prints a friendly message:

```python
try:
    ts_lang = tree_sitter_typescript.language_typescript()
except Exception as e:
    print(f"Failed to load TypeScript language: {e}")
```

---

## Parameters

| Function | Parameters | Description |
|----------|------------|-------------|
| `language_typescript()` | *None* | No parameters. |
| `language_tsx()` | *None* | No parameters. |

> Both functions are zero‑argument factory functions that load the compiled language definitions.

---

## Return Values

| Function | Return Type | Description |
|----------|-------------|-------------|
| `language_typescript()` | `tree_sitter.Language` | An instance representing the TypeScript grammar. |
| `language_tsx()` | `tree_sitter.Language` | An instance representing the TSX grammar. |

> The returned `Language` objects can be passed to `tree_sitter.Parser` to parse TypeScript/TSX source code.

---

## Additional Notes

- The script uses `print(dir(tree_sitter_typescript))` to list all exported names.  
- The `try/except` blocks ensure that any runtime errors (e.g., missing compiled bindings) are reported without crashing the script.  
- The output of `type()` shows that the returned objects are instances of `tree_sitter.Language`, confirming that the binding is functional.

---
