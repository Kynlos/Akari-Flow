---
title: Debug Polyglot
layout: default
---

# debug_polyglot.py

*Auto-generated from `debug_polyglot.py`*

# debug_polyglot.py – API Documentation

> **Purpose** – A lightweight debugging helper that demonstrates how to use the `PolyglotAnalyzer` class to extract symbols from source code snippets.  
> **Location** – `debug_polyglot.py` (top‑level script, not a library module).

---

## 1. Overview

`debug_polyglot.py` is a **stand‑alone script** that:

1. **Adds** the `./.github/scripts/polyglot` directory to `sys.path` so that the local `polyglot_analyzer` package can be imported.
2. **Imports** `PolyglotAnalyzer` from `polyglot_analyzer`.
3. **Instantiates** the analyzer and prints status messages.
4. **Runs** a quick test by calling `extract_symbols` on a tiny Python snippet.
5. **Prints** the extracted symbols or any errors that occur.

The script is meant for developers who want to verify that the analyzer works correctly in the current environment. It is **not** intended to be imported as a library.

---

## 2. Exports

| Export | Type | Description |
|--------|------|-------------|
| None | – | The script does **not** expose any functions, classes, or variables for import. It only executes code when run. |

> **Note** – The script *uses* the `PolyglotAnalyzer` class from `polyglot_analyzer`, but it does not re‑export it.

---

## 3. Usage Examples

### 3.1 Running the Script

```bash
python debug_polyglot.py
```

You should see output similar to:

```
Instantiating PolyglotAnalyzer...
Analyzer instantiated.
Testing extract_symbols...
Symbols found: ['hello']
```

### 3.2 Customizing the Test Code

Edit the `code` variable in the script to test different snippets:

```python
code = """
class Greeter:
    def greet(self, name):
        print(f"Hello, {name}!")
"""
```

Run the script again to see the symbols extracted from the new snippet.

### 3.3 Using the Analyzer Programmatically

If you want to use `PolyglotAnalyzer` directly in another script:

```python
import sys
import os

# Add the polyglot directory to sys.path
sys.path.append(os.path.join(os.getcwd(), '.github', 'scripts', 'polyglot'))

from polyglot_analyzer import PolyglotAnalyzer

analyzer = PolyglotAnalyzer()
symbols = analyzer.extract_symbols("""
def foo():
    pass
""", '.py')
print(symbols)  # ['foo']
```

---

## 4. Parameters

### `PolyglotAnalyzer.extract_symbols(code: str, file_extension: str) -> List[str]`

| Parameter | Type | Description |
|-----------|------|-------------|
| `code` | `str` | The source code to analyze. |
| `file_extension` | `str` | The file extension (e.g., `'.py'`, `'.js'`) that informs the analyzer which language parser to use. |

> **Important** – The `file_extension` must match a supported language; otherwise the analyzer may raise an error.

---

## 5. Return Values

`PolyglotAnalyzer.extract_symbols` returns a **list of strings** representing the names of top‑level symbols found in the provided code. For example:

```python
>>> analyzer.extract_symbols("def foo(): pass", ".py")
['foo']
```

If no symbols are found, an empty list `[]` is returned.

---

## 6. Error Handling

- **ImportError** – If `polyglot_analyzer` cannot be found, the script prints an error and exits with status `1`.
- **Instantiation Failure** – Any exception raised during `PolyglotAnalyzer()` construction is printed with a traceback, and the script exits.
- **Extraction Failure** – Exceptions from `extract_symbols` are caught, printed with a traceback, and the script continues (or exits if desired).

---

## 7. Extending the Script

If you want to add more tests:

1. Define additional `code` strings.
2. Call `analyzer.extract_symbols` with the appropriate file extension.
3. Print or assert the expected symbols.

Example:

```python
tests = [
    ("def bar(): pass", ".py", ["bar"]),
    ("function baz() {}", ".js", ["baz"]),
]

for src, ext, expected in tests:
    result = analyzer.extract_symbols(src, ext)
    assert result == expected, f"Expected {expected}, got {result}"
```

---

### TL;DR

- **Run** `python debug_polyglot.py` to see a quick demo of `PolyglotAnalyzer`.
- **Use** `PolyglotAnalyzer.extract_symbols(code, ext)` to get a list of symbol names from any supported language snippet.
- The script itself **does not export** anything; it’s purely for debugging and demonstration.
