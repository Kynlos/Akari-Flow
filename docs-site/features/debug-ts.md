---
title: Debug Ts
layout: default
---

# debug_ts.py

*Auto-generated from `debug_ts.py`*

# `debug_ts.py`

> A lightweight demo script that shows how to use the **PolyglotAnalyzer** to extract symbols from a TypeScript snippet.

> **Location**: `.github/scripts/polyglot/debug_ts.py`

---

## 1. Overview

`debug_ts.py` is a one‑off test harness that:

1. **Prepends** the local `polyglot` package to `sys.path` so the script can import the analyzer.
2. **Instantiates** a `PolyglotAnalyzer`.
3. **Feeds** a small TypeScript function into the analyzer.
4. **Prints** the extracted symbol information or an error traceback.

It is *not* a library module; it simply demonstrates the public API of `PolyglotAnalyzer`.

---

## 2. Exports

| Export | Type | Description |
|--------|------|-------------|
| `PolyglotAnalyzer` | Class | The main analyzer class that can parse source code in multiple languages. |
| `analyzer` | Instance | A singleton instance of `PolyglotAnalyzer` created by the script. |
| `extract_symbols` | Method | Public method of `PolyglotAnalyzer` that returns a list of symbol descriptors for a given source string. |

> **Note**: The script itself does not expose any functions or classes; it only uses the above exports.

---

## 3. Usage Examples

### 3.1 Running the Demo Script

```bash
python .github/scripts/polyglot/debug_ts.py
```

**Expected output**

```
Testing TS extraction...
Symbols: [{'name': 'add', 'type': 'function', 'return_type': 'number', 'parameters': [{'name': 'a', 'type': 'number'}, {'name': 'b', 'type': 'number'}]}]
```

If the analyzer cannot be imported, the script will print an error and exit.

---

### 3.2 Using `PolyglotAnalyzer` in Your Own Code

```python
from polyglot_analyzer import PolyglotAnalyzer

analyzer = PolyglotAnalyzer()

ts_code = """
function multiply(x: number, y: number): number {
    return x * y;
}
"""

symbols = analyzer.extract_symbols(ts_code, '.ts')
print(symbols)
```

---

## 4. Parameters

### `PolyglotAnalyzer.extract_symbols(code, file_extension)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `code` | `str` | The raw source code to analyze. |
| `file_extension` | `str` | The file extension that indicates the language (e.g., `'.ts'` for TypeScript, `'.py'` for Python). |

> The analyzer uses the extension to select the appropriate parser.

---

## 5. Return Values

`extract_symbols` returns a **list of dictionaries**. Each dictionary represents a symbol found in the source code and typically contains:

| Key | Type | Example | Meaning |
|-----|------|---------|---------|
| `name` | `str` | `"add"` | The identifier name. |
| `type` | `str` | `"function"` | Symbol kind (`function`, `class`, `variable`, etc.). |
| `return_type` | `str` | `"number"` | (Optional) Return type for functions. |
| `parameters` | `list[dict]` | `[{'name': 'a', 'type': 'number'}, …]` | Parameter list for functions. |
| `location` | `dict` | `{'line': 1, 'column': 1}` | (Optional) Source location. |

> The exact shape of the dictionary depends on the language and the parser implementation.

---

## 6. Error Handling

- If `polyglot_analyzer` cannot be imported, the script prints the exception and exits with status `1`.
- If `extract_symbols` raises an exception, the script prints the error message and a full traceback.

---

## 7. Extending the Demo

To test other languages, simply change the `file_extension` argument:

```python
python_code = "def foo(): pass"
symbols = analyzer.extract_symbols(python_code, '.py')
```

The same `extract_symbols` method will dispatch to the appropriate language parser.

---

## 8. Dependencies

- `polyglot_analyzer` (must be present in `.github/scripts/polyglot` or installed in the environment).

---

### TL;DR

`debug_ts.py` is a quick sanity‑check script that shows how to:

1. Import `PolyglotAnalyzer`.
2. Call `extract_symbols(code, '.ts')`.
3. Inspect the returned symbol list.

Use it as a template for building your own language‑agnostic code‑analysis tooling.
