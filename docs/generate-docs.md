# generate-docs.py

*Auto-generated from `.github/scripts/generate-docs.py`*

# Advanced Auto‑Documentation Generator – `generate‑docs.py`

> **What this module does**  
> `generate‑docs.py` is a CI‑friendly script that automatically produces API documentation, changelog entries, and PR comments for any code files that have changed in a Git repository.  
> It works by:
> 1. Detecting which files changed (`changed_files.txt` is expected to be produced by a CI job).
> 2. Extracting symbols from each file with **PolyglotAnalyzer** (Python, Go, TS/JS, Rust, Java, C/C++ …).
> 3. Comparing the old and new versions to surface breaking changes.
> 4. Sending the file content (and a diff preview) to a Groq LLM to generate Markdown documentation.
> 5. Writing the docs to `docs/<file>.md`, updating `CHANGELOG.md`, and creating a PR comment (`doc_output.md`).

> **Key features**  
> * Diff‑aware documentation – only changed files are processed.  
> * Breaking‑change detection with auto‑labeling.  
> * Cross‑file impact analysis placeholder.  
> * Mermaid class diagram generation (via `diagram_generator`).  
> * Caching via `.github/doc_cache.json` to skip unchanged files.  
> * Configurable via `config/languages.json` and environment variables (`GROQ_API_KEY`, `LLM_MODEL`).  

---

## Exports

| Function | Purpose |
|----------|---------|
| `get_file_hash(content)` | Compute SHA‑256 hash of a file’s content. |
| `extract_symbols_detailed(content, file_path)` | Use `PolyglotAnalyzer` to extract a detailed symbol list (name, type, signature, exported flag, etc.). |
| `detect_breaking_changes(old_content, new_content, file_path)` | Compare two file versions and return a dict describing any breaking changes. |
| `get_git_diff(file_path)` | Run `git diff HEAD~1 HEAD <file>` and return the diff string. |
| `generate_documentation(file_context, file_path)` | Call the LLM to produce Markdown documentation for a file. |
| `generate_changelog_entry(file_path, old_content, new_content, breaking_info)` | Build a changelog snippet for a single file. |
| `update_changelog(entries)` | Merge new changelog entries into `CHANGELOG.md`. |
| `generate_smart_pr_comment(code_files, doc_files, breaking_changes, impacts, changelog_entries)` | Assemble a PR comment that summarizes breaking changes, docs, changelog, and recommended actions. |
| `main()` | Orchestrates the whole workflow. |

> **Note** – The script is intended to be executed directly (`python generate-docs.py`) rather than imported as a library.

---

## Function‑by‑Function Documentation

### `get_file_hash(content: str) -> str`

| Parameter | Type | Description |
|-----------|------|-------------|
| `content` | `str` | Raw file content. |

| Return | Type | Description |
|--------|------|-------------|
| `hash` | `str` | 64‑character hexadecimal SHA‑256 hash. |

> **Usage**  
> ```python
> from pathlib import Path
> content = Path('src/main.py').read_text()
> file_hash = get_file_hash(content)
> ```

---

### `extract_symbols_detailed(content: str, file_path: str) -> List[Dict]`

| Parameter | Type | Description |
|-----------|------|-------------|
| `content` | `str` | Raw file content. |
| `file_path` | `str` | Path to the file (used to determine extension). |

| Return | Type | Description |
|--------|------|-------------|
| `symbols` | `List[Dict]` | Each dict contains: <br>• `type` (`function`/`class`/…)<br>• `name`<br>• `params` (string placeholder “…”)<br>• `returns` (default “Any”)<br>• `exported` (`True`/`False`)<br>• `signature` (raw signature string)<br>• `lineno` (line number). |

> **Usage**  
> ```python
> symbols = extract_symbols_detailed(code, 'src/utils.py')
> for sym in symbols:
>     print(f"{sym['type']} {sym['name']} at line {sym['lineno']}")
> ```

---

### `detect_breaking_changes(old_content: str, new_content: str, file_path: str) -> Dict`

| Parameter | Type | Description |
|-----------|------|-------------|
| `old_content` | `str` | Previous version of the file. |
| `new_content` | `str` | Current version of the file. |
| `file_path` | `str` | Path to the file (used for symbol extraction). |

| Return | Type | Description |
|--------|------|-------------|
| `info` | `Dict` | `{'has_breaking': bool, 'changes': List[Dict]}`<br>Each change dict contains: <br>• `type` (`removed` or `signature_change`) <br>• `symbol` <br>• `severity` (`BREAKING`) <br>• `message` <br>• optional `old`/`new` signature strings. |

> **Usage**  
> ```python
> breaking = detect_breaking_changes(old_code, new_code, 'src/api.py')
> if breaking['has_breaking']:
>     for c in breaking['changes']:
>         print(c['message'])
> ```

---

### `get_git_diff(file_path: str) -> Optional[str]`

| Parameter | Type | Description |
|-----------|------|-------------|
| `file_path` | `str` | Path to the file. |

| Return | Type | Description |
|--------|------|-------------|
| `diff` | `Optional[str]` | Diff string from `git diff HEAD~1 HEAD <file>`, or `None` if an error occurs. |

> **Usage**  
> ```python
> diff = get_git_diff('src/main.py')
> if diff:
>     print(diff)
> ```

---

### `generate_documentation(file_context: str, file_path: str) -> str`

| Parameter | Type | Description |
|-----------|------|-------------|
| `file_context` | `str` | Markdown‑ready context that includes the file name, diff preview, and the full file content. |
| `file_path` | `str` | Path to the file (used only for logging). |

| Return | Type | Description |
|--------|------|-------------|
| `doc` | `str` | LLM‑generated Markdown documentation, or an error message string. |

> **Usage**  
> ```python
> context = f"## {Path(file_path).name}\n\n```typescript\n{content}\n```\n"
> doc_md = generate_documentation(context, file_path)
> ```

---

### `generate_changelog_entry(file_path: str, old_content: str, new_content: str, breaking_info: Dict) -> Optional[str]`

| Parameter | Type | Description |
|-----------|------|-------------|
| `file_path` | `str` | Path to the file. |
| `old_content` | `str` | Previous version. |
| `new_content` | `str` | Current version. |
| `breaking_info` | `Dict` | Output of `detect_breaking_changes`. |

| Return | Type | Description |
|--------|------|-------------|
| `entry` | `Optional[str]` | Markdown snippet for the changelog, or `None` if nothing changed. |

> **Usage**  
> ```python
> entry = generate_changelog_entry('src/api.py', old, new, breaking)
> if entry:
>     print(entry)
> ```

---

### `update_changelog(entries: List[Dict]) -> None`

| Parameter | Type | Description |
|-----------|------|-------------|
| `entries` | `List[Dict]` | Each dict must contain `file` (filename) and `content` (Markdown changelog snippet). |

| Return | Type | Description |
|--------|------|-------------|
| `None` | – | Updates or creates `CHANGELOG.md` in the repository root. |

> **Usage**  
> ```python
> update_changelog([{'file': 'api.py', 'content': entry}])
> ```

---

### `generate_smart_pr_comment(code_files: List[str], doc_files: List[str], breaking_changes: