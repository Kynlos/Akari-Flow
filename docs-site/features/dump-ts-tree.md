---
title: Dump Ts Tree
layout: default
---

# dump_ts_tree.py

*Auto-generated from `dump_ts_tree.py`*

# dump_ts_tree.py – TypeScript AST Dump Utility

## Overview
`dump_ts_tree.py` is a lightweight demonstration script that shows how to use the **PolyglotAnalyzer** library to parse TypeScript source code and inspect its abstract syntax tree (AST).  
The script:

1. Adds the Polyglot helper directory to `sys.path`.
2. Imports `PolyglotAnalyzer` from `polyglot_analyzer`.
3. Instantiates the analyzer.
4. Parses a hard‑coded TypeScript snippet.
5. Prints the root node of the resulting parse tree.

Because it is a script, it does not expose any public API of its own; instead, it serves as an example of how to use the `PolyglotAnalyzer` class.

---

## Exports
| Export | Type | Description |
|--------|------|-------------|
| **PolyglotAnalyzer** | Class (from `polyglot_analyzer`) | The core parser that can handle multiple languages (TypeScript, JavaScript, etc.). |
| **parse** | Method of `PolyglotAnalyzer` | Parses source code and returns a parse tree. |

> **Note**: The script itself does not define any functions or classes that are exported for external use.

---

## Usage Examples

### 1. Running the Script Directly
```bash
python dump_ts_tree.py
```
Output will be the string representation of the root node of the parsed TypeScript AST.

### 2. Using `PolyglotAnalyzer` in Your Own Code
```python
from polyglot_analyzer import PolyglotAnalyzer

analyzer = PolyglotAnalyzer()

ts_code = """
class MyClass {}
interface MyInterface {}
"""

# Parse the code as TypeScript
tree = analyzer.parse(ts_code, '.ts')

# Inspect the root node
print(tree.root_node)
```

### 3. Parsing Multiple Files
```python
import glob
from polyglot_analyzer import PolyglotAnalyzer

analyzer = PolyglotAnalyzer()

for ts_file in glob.glob('src/**/*.ts', recursive=True):
    with open(ts_file, 'r', encoding='utf-8') as f:
        code = f.read()
    tree = analyzer.parse(code, os.path.splitext(ts_file)[1])
    print(f'AST root for {ts_file}:', tree.root_node)
```

---

## Parameters

### `PolyglotAnalyzer.parse(code: str, file_extension: str) -> Tree`
| Parameter | Type | Description |
|-----------|------|-------------|
| `code` | `str` | The source code to parse. |
| `file_extension` | `str` | File extension indicating the language (e.g., `'.ts'`, `'.js'`). The analyzer uses this to select the correct parser. |

> **Tip**: The `file_extension` should include the leading dot (`.`). If omitted, the parser may default to a generic language or fail.

---

## Return Values

| Return | Type | Description |
|--------|------|-------------|
| `Tree` | Object | A parse tree object that contains a `root_node` property. The `root_node` is the entry point of the AST and can be traversed or inspected further. |

> The exact structure of the `Tree` object depends on the underlying parser implementation. Typically, it exposes methods such as `children`, `type`, and `text` for each node.

---

## Error Handling

- If `polyglot_analyzer` cannot be imported, the script exits with status code `1` and prints nothing.  
- The `parse` method may raise exceptions if the code is syntactically invalid or if the language is unsupported. Wrap calls in `try/except` blocks as needed.

---

## Dependencies

- **polyglot_analyzer** – The library that provides the `PolyglotAnalyzer` class.  
- **tree-sitter** (or similar) – Underlying parser engine used by `polyglot_analyzer`.  
- Standard Python libraries: `sys`, `os`.

---

## Summary

`dump_ts_tree.py` is a minimal, self‑contained example that demonstrates how to:

1. Import and instantiate `PolyglotAnalyzer`.
2. Parse TypeScript code.
3. Access the root node of the resulting AST.

Use the script as a starting point for building tooling that needs to analyze or transform TypeScript (or other language) source files.
