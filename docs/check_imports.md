# check_imports.py

*Auto-generated from `check_imports.py`*

# check_imports.py

> A lightweight diagnostic script that verifies whether the `tree_sitter` and `tree_sitter_python` packages are available in the current Python environment and prints a quick snapshot of the `tree_sitter_python` module’s public interface.

---

## 1. Overview

`check_imports.py` is a **stand‑alone script** (not a library) that:

1. Tries to import the `tree_sitter` package.
2. Tries to import the `tree_sitter_python` package.
3. Prints a confirmation message for each successful import.
4. Prints the list of attributes and sub‑modules exposed by `tree_sitter_python` (`dir(tree_sitter_python)`).
5. Catches and reports any `ImportError` or other exception that occurs during the import process.

It is intended for quick debugging or environment validation when working with the Tree‑Sitter parsing library.

---

## 2. Exports

| Export | Type | Description |
|--------|------|-------------|
| **None** | – | The file does not expose any functions, classes, or interfaces. It only runs code at import time. |

> **Note:** Because the script runs at import time, it is best used as a **stand‑alone executable** (`python check_imports.py`) rather than imported into another module.

---

## 3. Usage Examples

### 3.1 Running the script from the command line

```bash
$ python check_imports.py
tree_sitter imported
tree_sitter_python imported
['__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', '__path__', 'Language', 'Parser', 'tree_sitter']
```

If a package is missing, you’ll see an error message:

```bash
$ python check_imports.py
ImportError: No module named 'tree_sitter'
```

### 3.2 Using the script programmatically

While not intended for import, you can still execute the logic from another script:

```python
import subprocess

result = subprocess.run(
    ["python", "check_imports.py"],
    capture_output=True,
    text=True
)

print("STDOUT:")
print(result.stdout)
print("STDERR:")
print(result.stderr)
```

---

## 4. Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| *None* | – | The script takes no command‑line arguments or function parameters. |

---

## 5. Return Values

| Function | Return Value | Description |
|----------|--------------|-------------|
| *None* | – | The script does not return a value. It only prints to `stdout` and `stderr`. |

---

## 6. Implementation Details

```python
try:
    import tree_sitter
    print("tree_sitter imported")
    import tree_sitter_python
    print("tree_sitter_python imported")
    print(dir(tree_sitter_python))
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Error: {e}")
```

- **`try` block**: Attempts to import the two packages.
- **`print` statements**: Provide immediate feedback on success.
- **`dir(tree_sitter_python)`**: Reveals the public API of the `tree_sitter_python` module.
- **`except ImportError`**: Catches missing‑module errors and prints a clear message.
- **`except Exception`**: Catches any other unexpected errors and prints them.

---

## 7. Common Use Cases

| Scenario | Why use this script? |
|----------|----------------------|
| **Environment validation** | Quickly confirm that the required Tree‑Sitter packages are installed and importable. |
| **Debugging import issues** | Identify which package is missing or causing import errors. |
| **CI/CD checks** | Add as a step in a pipeline to ensure dependencies are correctly installed before running tests. |

---

## 8. Extending the Script

If you want to turn this into a reusable helper, consider refactoring into a function:

```python
def check_tree_sitter_imports() -> dict:
    """Return a dict with import status and module attributes."""
    result = {}
    try:
        import tree_sitter
        result['tree_sitter'] = 'imported'
    except ImportError as e:
        result['tree_sitter'] = f'ImportError: {e}'

    try:
        import tree_sitter_python
        result['tree_sitter_python'] = {
            'status': 'imported',
            'attributes': dir(tree_sitter_python)
        }
    except ImportError as e:
        result['tree_sitter_python'] = f'ImportError: {e}'

    return result
```

This would allow programmatic consumption of the import status.

---

## 9. Summary

`check_imports.py` is a minimal, self‑contained script that verifies the presence of the `tree_sitter` ecosystem in your Python environment and prints a quick snapshot of the `tree_sitter_python` module. It is useful for debugging, CI checks, or quick sanity tests before diving into Tree‑Sitter parsing work.