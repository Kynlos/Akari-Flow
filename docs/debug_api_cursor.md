# debug_api_cursor.py

*Auto-generated from `debug_api_cursor.py`*

# debug_api_cursor.py – API Documentation

> **NOTE**  
> This file is a *demo* script that exercises the `tree_sitter.QueryCursor` API.  
> It is **not** a library that exports reusable functions or classes.  
> The documentation below explains the module’s behavior, the public API of
> `tree_sitter.QueryCursor` that the script uses, and how you can adapt the
> examples for your own projects.

---

## 1. Overview

`debug_api_cursor.py` demonstrates how to:

1. Load the Python grammar for `tree_sitter`.
2. Create a `Query` that matches function definitions.
3. Parse a small Python snippet (`def foo(): pass`).
4. Use `QueryCursor` to find all captures of the query in the parse tree.
5. Show the difference between constructing a cursor with a query
   versus constructing it without arguments.

The script prints diagnostic information to the console, making it useful for
debugging or learning how `tree_sitter`’s cursor API works.

---

## 2. Exports

The module does **not** export any functions, classes, or interfaces.  
All symbols are used internally and the script runs when executed.

---

## 3. Usage Examples

Below are practical snippets that illustrate how to use the key `tree_sitter`
components that the script relies on.  
Feel free to copy/paste them into your own code.

### 3.1. Basic QueryCursor usage (with a query)

```python
import tree_sitter
import tree_sitter_python

# 1. Load the language and create a parser
lang = tree_sitter.Language(tree_sitter_python.language())
parser = tree_sitter.Parser(lang)

# 2. Parse some source code
source = b"def foo(): pass"
tree = parser.parse(source)

# 3. Build a query that captures function definitions
query = tree_sitter.Query(lang, "(function_definition) @func")

# 4. Create a cursor bound to that query
cursor = tree_sitter.QueryCursor(query)

# 5. Retrieve captures from the root node
captures = cursor.captures(tree.root_node)

# 6. Iterate over the captures
for node, capture_name in captures:
    print(f"Found {capture_name} at {node.start_point}-{node.end_point}")
```

### 3.2. QueryCursor without an initial query

```python
# Create an empty cursor
cursor = tree_sitter.QueryCursor()

# Later, set a query
cursor.set_query(query)

# Now you can use it as before
captures = cursor.captures(tree.root_node)
```

### 3.3. Using `captures` with a custom query

```python
# Query that captures both function definitions and class definitions
query = tree_sitter.Query(
    lang,
    """
    (function_definition) @func
    (class_definition) @class
    """
)

cursor = tree_sitter.QueryCursor(query)
captures = cursor.captures(tree.root_node)

for node, name in captures:
    print(f"{name}: {node.type} at {node.start_point}-{node.end_point}")
```

---

## 4. Parameters

| Function/Method | Parameter | Type | Description |
|-----------------|-----------|------|-------------|
| `tree_sitter.QueryCursor.__init__` | `query` (optional) | `tree_sitter.Query` | The query to bind to the cursor. If omitted, the cursor starts empty and must be set later with `set_query`. |
| `tree_sitter.QueryCursor.set_query` | `query` | `tree_sitter.Query` | Assigns or replaces the cursor’s query. |
| `tree_sitter.QueryCursor.captures` | `node` | `tree_sitter.Node` | The root node of the tree to search. |
| `tree_sitter.Query` | `language` | `tree_sitter.Language` | The language for which the query is valid. |
| `tree_sitter.Query` | `query_string` | `str` | The Tree-sitter query string. |
| `tree_sitter.Parser.parse` | `source` | `bytes` | Source code to parse. |
| `tree_sitter.Parser.set_language` | `language` | `tree_sitter.Language` | Sets the language for the parser. |

---

## 5. Return Values

| Function/Method | Return Type | Description |
|-----------------|-------------|-------------|
| `tree_sitter.QueryCursor.__init__` | `tree_sitter.QueryCursor` | The newly created cursor instance. |
| `tree_sitter.QueryCursor.set_query` | `None` | No return value. |
| `tree_sitter.QueryCursor.captures` | `List[Tuple[tree_sitter.Node, str]]` | A list of tuples. Each tuple contains a node that matches a capture and the capture name (e.g., `"func"`). |
| `tree_sitter.Query` | `tree_sitter.Query` | The query object. |
| `tree_sitter.Parser.parse` | `tree_sitter.Tree` | The parse tree for the given source. |
| `tree_sitter.Parser.set_language` | `None` | No return value. |

---

## 6. Quick Reference – `tree_sitter.QueryCursor`

| Method | Signature | Notes |
|--------|-----------|-------|
| `__init__(self, query: Optional[Query] = None)` | Create a cursor, optionally bound to a query. |
| `set_query(self, query: Query)` | Bind or replace the cursor’s query. |
| `captures(self, node: Node)` | Return all captures for the given node. |

> **Tip**: The `captures` method returns *all* matches in the tree, not just the first.  
> If you only need the first match, iterate over the list or use `next(captures)`.

---

## 7. Running the Demo

```bash
$ python debug_api_cursor.py
Testing QueryCursor(query)...
Cursor created with query arg
Captures type: <class 'list'>
Match count: 1
First match type: <class 'tuple'>
First match content: (<tree_sitter.Node object at 0x...>, 'func')
Testing QueryCursor() without args...
Cursor created without args
```

The output confirms that:

* A cursor created with a query can capture nodes.
* A cursor created without a query can still be instantiated (though it cannot capture until a query is set).

---

## 8. Common Pitfalls

| Issue | Cause | Fix |
|-------|-------|-----|
| `tree_sitter.QueryCursor()` throws `TypeError` | Using an older `tree_sitter` version that requires a query | Upgrade to the latest `tree_sitter` (≥ 0.20) or pass a query at construction. |
| `captures` returns empty list | Query string syntax error or wrong language | Verify the query string and that the language matches the source code. |
| `tree_sitter.Language` fails | `tree_sitter_python` not installed or incompatible | Install `tree_sitter_python` via `pip install tree_sitter_python` and ensure it matches your `tree_sitter` version. |

---

## 9. Further Reading

* [Tree‑Sitter Documentation](https://tree-sitter.github.io/tree-sitter/)
* [Python bindings for Tree‑Sitter](https://github.com/tree-sitter/tree-sitter-python)
* [Query Language Reference](https://tree-sitter.github.io/tree-sitter/using-parsers#query-language)

---