# test_doc_integration.py

*Auto-generated from `test_doc_integration.py`*

# test_doc_integration.py – API Documentation

> **Location**: `.github/scripts/test_doc_integration.py`  
> **Purpose**: A lightweight integration test that demonstrates how the `extract_symbols_detailed` helper from the repository’s documentation generator can be used to parse Python source code and emit a structured list of symbols.

---

## 1. Overview

`test_doc_integration.py` is a **stand‑alone test script** that:

1. Dynamically imports the `generate-docs.py` module (which lives in `.github/scripts` and contains the documentation‑generation logic).
2. Calls the `extract_symbols_detailed` function to parse a small snippet of Python code.
3. Prints a human‑readable summary of the symbols found.

The script is **not part of the public API** of the library; it is meant for developers to quickly verify that the symbol extraction logic works as expected.

---

## 2. Exports

| Export | Type | Description |
|--------|------|-------------|
| **None** | – | The file does not expose any functions, classes, or interfaces. It is a runnable script only. |

> **Note**: The script *uses* the `extract_symbols_detailed` function from `generate-docs.py`, but it does **not** re‑export it.

---

## 3. Usage Examples

### 3.1 Running the Script

```bash
# From the repository root
python .github/scripts/test_doc_integration.py
```

**Expected output**

```
Testing Extraction...
Symbols found: 2
- function: hello_world (line 3)
  Signature: hello_world()
- class: MyClass (line 6)
  Signature: MyClass()
```

The script prints the number of symbols found and a short description of each.

### 3.2 Using the Extractor in Your Own Code

If you want to use the same extractor in a different script, you can copy the import logic:

```python
import importlib.util
import sys
import os

# Path to the generate-docs.py script
spec = importlib.util.spec_from_file_location(
    "generate_docs",
    os.path.join(os.getcwd(), ".github", "scripts", "generate-docs.py")
)
generate_docs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generate_docs)

extract_symbols = generate_docs.extract_symbols_detailed

# Example usage
code = """
def foo(x, y=42):
    return x + y

class Bar:
    def baz(self, *args, **kwargs):
        pass
"""

symbols = extract_symbols(code, "example.py")
print(symbols)
```

---

## 4. Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `code` | `str` | A string containing the Python source code to analyze. |
| `filename` | `str` | The *logical* name of the file being parsed (used only for reporting). |

> These parameters are passed to `extract_symbols_detailed`, which is imported from `generate-docs.py`. The test script itself does not expose any parameters.

---

## 5. Return Values

The script itself does **not** return a value; it simply prints to `stdout`.  
However, the `extract_symbols_detailed` function returns:

| Return Type | Description |
|-------------|-------------|
| `List[Dict[str, Any]]` | A list of dictionaries, each representing a symbol found in the source code. |

Each dictionary contains at least the following keys:

| Key | Type | Description |
|-----|------|-------------|
| `type` | `str` | Symbol type (`"function"`, `"class"`, `"method"`, etc.). |
| `name` | `str` | Fully‑qualified name of the symbol. |
| `lineno` | `int` | Line number where the symbol is defined. |
| `signature` | `str` | Human‑readable signature (e.g., `foo(x, y=42)`). |

---

## 6. Dependencies

- **Python 3.8+** (required for `importlib.util.spec_from_file_location` and f‑strings).
- The repository must contain `.github/scripts/generate-docs.py` with an `extract_symbols_detailed` function.

---

## 7. Extending the Test

You can modify the `code` variable in the script to test more complex scenarios:

```python
code = """
def outer(a, b):
    def inner(c):
        return c * 2
    return inner(a) + b

class OuterClass:
    @staticmethod
    def static_method(x):
        return x

    @classmethod
    def class_method(cls, y):
        return y
"""
```

Running the script will then enumerate all functions, nested functions, and class methods.

---

## 8. Summary

`test_doc_integration.py` is a quick, self‑contained example that demonstrates how to:

1. Dynamically import a helper module.
2. Invoke the symbol extraction routine.
3. Inspect the resulting symbol metadata.

It is intended for developers and CI pipelines to validate that the documentation generator’s core logic is functioning correctly.