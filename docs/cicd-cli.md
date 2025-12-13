# cicd-cli.py

*Auto-generated from `cicd-cli.py`*

# cicd‑cli.py – Unified CI/CD CLI Tool

A lightweight command‑line interface that orchestrates the core CI/CD stages of the project.  
It runs the following scripts located in the `.github/scripts` directory:

| Stage | Script |
|-------|--------|
| Code Analysis | `code-analyzer.py` |
| Documentation | `generate-docs.py` |
| Site Generation | `site_generator.py` |

The CLI supports four sub‑commands:

1. **`analyze`** – Run the code analyzer on a single file (or all changed files).  
2. **`gen-docs`** – Generate documentation for a single file (or all changed files).  
3. **`build-site`** – Build the static documentation site.  
4. **`full-run`** – Execute the entire pipeline locally, simulating a CI run.

> **Why this file?**  
> The tool is intentionally minimal: it delegates heavy lifting to the scripts in `.github/scripts` while providing a convenient, single‑entry point for developers and CI jobs.

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `SCRIPTS_DIR` | `Path` | Path to the directory containing the CI scripts. |
| `run_script` | `function` | Executes a script from `SCRIPTS_DIR`. |
| `main` | `function` | Entry point that parses CLI arguments and dispatches to the appropriate stage. |

> **Note:** The module is designed to be executed directly (`python cicd-cli.py …`). Importing it in other Python code is possible but not required.

---

## Functions

### `run_script(script_name: str, args: list[str] = []) -> None`

Runs a script located in `SCRIPTS_DIR`.

| Parameter | Type | Description |
|-----------|------|-------------|
| `script_name` | `str` | File name of the script to run (e.g., `"code-analyzer.py"`). |
| `args` | `list[str]` | Optional list of command‑line arguments to pass to the script. Defaults to an empty list. |

**Return Value**  
`None`. The function prints status messages and invokes the script via `subprocess.run`. If the script file does not exist, it prints an error message and returns early.

**Side‑Effects**

- Prints a “Running …” message.
- Executes the script with the current Python interpreter (`sys.executable`).
- Does **not** capture or return the script’s output; it inherits the child process’s stdout/stderr.

**Usage Example**

```python
# Run the analyzer with a custom argument
run_script('code-analyzer.py', ['--verbose'])
```

---

### `main() -> None`

Parses command‑line arguments and dispatches to the appropriate CI stage.

| Parameter | Type | Description |
|-----------|------|-------------|
| None | – | The function reads `sys.argv` via `argparse`. |

**Return Value**  
`None`. The function prints help or runs the chosen stage.

**Side‑Effects**

- Creates a temporary `changed_files.txt` file when a single file is supplied to `analyze` or `gen-docs`.  
- Calls `run_script` for each stage.  
- Prints a progress banner for `full-run`.

**Usage Example**

```bash
# Run a single file through the analyzer
python cicd-cli.py analyze src/main.py

# Generate docs for a specific file
python cicd-cli.py gen-docs docs/README.md

# Build the entire documentation site
python cicd-cli.py build-site

# Simulate a full CI pipeline locally
python cicd-cli.py full-run
```

---

## Usage Examples

Below are practical examples that demonstrate each command in isolation.

### 1. Analyze a Single File

```bash
python cicd-cli.py analyze src/utils/helpers.py
```

*What happens?*  
- `changed_files.txt` is created with the path `src/utils/helpers.py`.  
- `code-analyzer.py` is executed, reading the file list from `changed_files.txt`.

### 2. Generate Documentation for a File

```bash
python cicd-cli.py gen-docs docs/api.md
```

*What happens?*  
- `changed_files.txt` is created with `docs/api.md`.  
- `generate-docs.py` runs and generates documentation for that file.

### 3. Build the Documentation Site

```bash
python cicd-cli.py build-site
```

*What happens?*  
- `site_generator.py` is executed, producing the static site in the configured output directory.

### 4. Full Pipeline Simulation

```bash
python cicd-cli.py full-run
```

*What happens?*  
- The tool sequentially runs `code-analyzer.py`, `generate-docs.py`, and `site_generator.py`.  
- Each stage prints a banner and status messages.  
- The final message `✅ Pipeline Complete` signals success.

---

## Parameter & Return Value Summary

| Function | Parameters | Return Value | Notes |
|----------|------------|--------------|-------|
| `run_script` | `script_name: str`, `args: list[str]` | `None` | Prints status, runs script, handles missing file. |
| `main` | None | `None` | Parses CLI, writes `changed_files.txt` if needed, dispatches to `run_script`. |

---

## Extending the CLI

If you add new scripts to `.github/scripts`, simply add a new sub‑parser in `main()` and call `run_script` with the script name.  
Example:

```python
# New sub‑command: lint
lint_parser = subparsers.add_parser('lint', help='Run linter')
lint_parser.add_argument('file', nargs='?', help='File to lint')

# In the dispatch block
elif args.command == 'lint':
    if args.file:
        with open('changed_files.txt', 'w') as f: f.write(args.file)
    run_script('run-linter.py')
```

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| `Error: <script> not found` | Script missing or wrong path | Ensure the script exists in `.github/scripts`. |
| No output from a script | Script writes to stdout but `subprocess.run` inherits stdout | Verify the script prints to console; otherwise capture output. |
| `changed_files.txt` not created | `args.file` is `None` | Provide a file path or modify the script to read from environment. |

---

## License & Credits

This file is part of the **Unified CI/CD Toolkit**.  
© 2025 The Open Source Contributors.  
MIT License.