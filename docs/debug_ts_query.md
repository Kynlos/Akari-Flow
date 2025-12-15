# debug_ts_query.py

*Auto-generated from `debug_ts_query.py`*

# debug_ts_query.py

> A lightweight test harness that verifies a set of Tree‑Sitter query patterns against the TypeScript grammar.  
> The script is intentionally minimal – it imports the grammar, compiles each pattern, and prints whether the compilation succeeded or failed.

---

## Overview

* **Purpose** – Quickly confirm that a set of Tree‑Sitter query strings are syntactically valid for the TypeScript language.  
* **How it works** –  
  1. Loads the TypeScript grammar via `tree_sitter_typescript`.  
  2. Defines a list of query patterns that capture various TypeScript constructs (`function`, `class`, `interface`, `method`).  
  3. Iterates over the patterns, attempting to compile each one with `tree_sitter.Query`.  
  4. Prints a concise success/failure message for each pattern.

The module does **not** expose any public API; it is intended to be executed as a script.

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| **None** | – | The file contains only top‑level code; nothing is exported for import by other modules. |

---

## Usage Examples

### 1. Run the script directly

```bash
python debug_ts_query.py
```

**Expected output**

```
Testing TS patterns...
Pattern 0 OK: (function_declaration name: (identifier) @name.definition)
Pattern 1 OK: (class_declaration name: (identifier) @name.definition)
Pattern 2 OK: (interface_declaration name: (identifier) @name.definition)
Pattern 3 OK: (method_definition name: (property_identifier) @name.definition)
```

If a pattern is malformed, the output will contain an error message, e.g.:

```
Pattern 2 FAILED: (interface_declaration name: (identifier) @name.definition) -> SyntaxError: ...
```

### 2. Import the script in another module (not recommended)

```python
# In another Python file
import debug_ts_query  # This will execute the script and print the results
```

> **Note**: Importing the module will immediately run the test harness. If you only want to use the patterns, copy the `patterns` list into your own code.

### 3. Use the patterns programmatically

```python
import tree_sitter
import tree_sitter_typescript

lang = tree_sitter.Language(tree_sitter_typescript.language_typescript())
patterns = [
    "(function_declaration name: (identifier) @name.definition)",
    "(class_declaration name: (identifier) @name.definition)",
    "(interface_declaration name: (identifier) @name.definition)",
    "(method_definition name: (property_identifier) @name.definition)"
]

queries = [tree_sitter.Query(lang, p) for p in patterns]
# Now `queries` contains compiled Query objects you can use with a Parser
```

---

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `lang` | `tree_sitter.Language` | The compiled TypeScript language definition loaded from `tree_sitter_typescript`. |
| `patterns` | `List[str]` | A list of Tree‑Sitter query strings that match specific TypeScript syntax nodes. |
| `pattern` | `str` | Individual query string being compiled in the loop. |
| `i` | `int` | Zero‑based index of the current pattern (used only for logging). |

---

## Return Values

| Function | Return Type | Description |
|----------|-------------|-------------|
| `tree_sitter.Query(lang, pattern)` | `tree_sitter.Query` | Returns a compiled query object if the pattern is syntactically correct. Raises an exception (e.g., `SyntaxError`) if the pattern is invalid. |
| `print()` | `None` | The script uses `print` for side‑effect logging; it does not return a value. |

---

## Additional Notes

* **Error handling** – The script catches *any* exception during query compilation and prints the error message. This is useful for debugging malformed patterns.  
* **Extending the pattern list** – Add or remove patterns as needed; the loop will automatically report their status.  
* **Dependencies** – Requires `tree_sitter` and `tree_sitter_typescript` to be installed in the Python environment.  
* **Running in CI** – This script can be added to a CI pipeline to ensure that query patterns remain valid after grammar updates.  

---