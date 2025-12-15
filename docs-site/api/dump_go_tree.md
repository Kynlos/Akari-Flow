---
title: Dump_Go_Tree
layout: default
---

# dump_go_tree.py

*Auto-generated from `dump_go_tree.py`*

# dump_go_tree.py – API Documentation

> **NOTE**  
> This file is a small demo script that shows how to use the `PolyglotAnalyzer` class from the `polyglot_analyzer` package to parse Go source code and inspect the resulting syntax tree.  
> The script itself does **not** expose any public API – it simply imports, runs, and prints a value.  
> The documentation below focuses on the public API that the script relies on (`PolyglotAnalyzer.parse`) and on how the script can be used.

---

## 1. Overview

`dump_go_tree.py` demonstrates how to:

1. **Import** the `PolyglotAnalyzer` class from the `polyglot_analyzer` package.
2. **Instantiate** the analyzer.
3. **Parse** a Go source snippet (`.go` file content) into a syntax tree.
4. **Print** the root node of the parsed tree to the console.

The script is intended for quick experimentation or as a template for building more sophisticated language‑analysis tools.

---

## 2. Exports

| Export | Type | Description |
|--------|------|-------------|
| `PolyglotAnalyzer` | Class | The main entry point for parsing source code in multiple languages. |
| `parse` | Method | Parses a string of source code and returns a syntax tree. |

> *The script itself does not expose any functions or classes; it only uses the above API.*

---

## 3. Usage Examples

Below are practical examples that illustrate how to use the exported API in various contexts.

### 3.1. Basic Usage (as shown in the script)

```python
from polyglot_analyzer import PolyglotAnalyzer

analyzer = PolyglotAnalyzer()
go_code = """
package main
import "fmt"
import (
    "net/http"
)
"""
tree = analyzer.parse(go_code, '.go')
print(tree.root_node)   # Prints the root node of the Go syntax tree
```

### 3.2. Parsing Multiple Languages

```python
from polyglot_analyzer import PolyglotAnalyzer

analyzer = PolyglotAnalyzer()

python_code = """
def hello():
    print("Hello, world!")
"""
js_code = """
function hello() {
    console.log("Hello, world!");
}
"""

py_tree = analyzer.parse(python_code, '.py')
js_tree = analyzer.parse(js_code, '.js')

print(py_tree.root_node)
print(js_tree.root_node)
```

### 3.3. Inspecting the Tree

```python
from polyglot_analyzer import PolyglotAnalyzer

analyzer = PolyglotAnalyzer()
code = "package main\nfunc main() { fmt.Println(\"Hi\") }"
tree = analyzer.parse(code, '.go')

# Walk the tree and print node types
def walk(node, depth=0):
    print('  ' * depth + f"{node.type}: {node.text}")
    for child in node.children:
        walk(child, depth + 1)

walk(tree.root_node)
```

---

## 4. Parameters

### `PolyglotAnalyzer.parse`

| Parameter | Type | Description |
|-----------|------|-------------|
| `source_code` | `str` | The raw source code to parse. |
| `file_extension` | `str` | The file extension (e.g., `'.go'`, `'.py'`, `'.js'`) that determines the language grammar to use. |

> **Note**: The `file_extension` must match one of the languages supported by the underlying parser. If an unsupported extension is passed, the method may raise an exception or return `None`.

---

## 5. Return Values

### `PolyglotAnalyzer.parse`

| Return Type | Description |
|-------------|-------------|
| `Tree` | An object representing the parsed syntax tree. The tree exposes at least the following attributes: |
| `root_node` | The root node of the syntax tree. Each node typically has: |
| `type` | The node’s type (e.g., `"package_clause"`, `"import_declaration"`). |
| `text` | The raw text of the node. |
| `children` | A list of child nodes. |

> The exact shape of the `Tree` and node objects depends on the implementation of `polyglot_analyzer`. The examples above assume a simple tree API similar to that of the Tree‑Sitter library.

---

## 6. Error Handling

- If `polyglot_analyzer` cannot be imported, the script exits with status `1`.
- The `parse` method may raise a `ValueError` or custom exception if the source code is invalid or the language grammar is missing.

---

## 7. Extending the Demo

You can modify the script to:

- **Read source files** from disk instead of hard‑coded strings.
- **Write the tree** to a file (e.g., JSON or XML) for later analysis.
- **Integrate with a linter** or code‑formatting tool that uses the syntax tree.

---

### TL;DR

`dump_go_tree.py` is a minimal example that shows how to:

1. Import `PolyglotAnalyzer`.
2. Parse Go code with `parse(code, '.go')`.
3. Access the root node via `tree.root_node`.

Use the `parse` method to analyze any supported language by passing the appropriate file extension.
