---
title: Code Analyzer
layout: default
---

# code-analyzer.py

*Auto-generated from `.github/scripts/code-analyzer.py`*

# Advanced Code Analyzer – API Documentation

> **Location**: `.github/scripts/code-analyzer.py`  
> **Python version**: 3.8+ (uses `ast`, `pathlib`, `typing`, `datetime`)  
> **Dependencies**: `json`, `re`, `sys`, `os`, `ast`, `pathlib`, `typing`, `datetime`

---

## 1. Overview

The **Advanced Code Analyzer** is a CI‑friendly tool that performs a multi‑faceted analysis of source code changes:

| Feature | What it does |
|---------|--------------|
| **Quality Scoring** | Calculates a 0‑100 score based on documentation coverage, cyclomatic complexity, and maintainability. |
| **Security Scanning** | Detects known insecure patterns (e.g. SQL injection, command injection) via regex. |
| **Performance Detection** | Flags potential performance regressions such as large functions or inefficient loops. |
| **AST‑Enhanced** | For Python files, it uses the `ast` module to get accurate metrics (functions, classes, docstrings, decision points). |
| **CI Integration** | Reads a list of changed files (`changed_files.txt`), runs the analysis, and writes a JSON report to `code-analysis/<timestamp>_<sha>/results.json`. |

The module is intentionally lightweight and can be dropped into any GitHub Actions workflow or run locally.

---

## 2. Exports

| Export | Type | Description |
|--------|------|-------------|
| `load_config()` | `None` | Loads global configuration from `config/languages.json`. |
| `ASTAnalyzer` | Class | Parses Python source and returns metrics. |
| `CodeAnalyzer` | Class | Main analyzer that supports multiple languages. |
| `analyze_file(file_path: str) -> Optional[Dict]` | Function | Convenience wrapper that reads a file, runs `CodeAnalyzer`, and returns a structured result. |
| `main()` | Function | CLI entry point; orchestrates the whole analysis pipeline. |

> **Note**: The module also defines a handful of global dictionaries (`LANGUAGE_CONFIG`, `SECURITY_PATTERNS`, `PERFORMANCE_PATTERNS`) that are populated by `load_config()`.

---

## 3. Usage Examples

### 3.1 Running the CLI (GitHub Actions)

```bash
# In your workflow
- name: Run Advanced Code Analyzer
  run: |
    python .github/scripts/code-analyzer.py
```

The script expects a file named `changed_files.txt` in the repository root containing a newline‑separated list of changed file paths.  
The output will be a JSON file under `code-analysis/<timestamp>_<sha>/results.json`.

### 3.2 Using the API from Python

```python
from pathlib import Path
from .github_scripts.code_analyzer import load_config, analyze_file

# Load config once
load_config()

# Analyze a single file
result = analyze_file('src/utils/helpers.py')
print(result['quality_score']['total'])
print(result['security_vulnerabilities'])
print(result['performance_issues'])
```

### 3.3 Inspecting the AST metrics (Python only)

```python
from .github_scripts.code_analyzer import ASTAnalyzer

with open('src/utils/helpers.py', 'r', encoding='utf-8') as f:
    content = f.read()

ast_stats = ASTAnalyzer(content).analyze()
print(ast_stats['functions'])
print(ast_stats['decision_points'])
```

### 3.4 Customizing the Configuration

Create `config/languages.json`:

```json
{
  "languages": {
    "python": {
      "extensions": [".py"],
      "comment_single": ["#"],
      "complexity_keywords": ["if", "for", "while", "except", "elif"],
      "function_pattern": "def\\s+\\w+\\s*\\("
    },
    "javascript": {
      "extensions": [".js", ".jsx"],
      "comment_single": ["//"],
      "complexity_keywords": ["if", "for", "while", "switch", "catch"],
      "function_pattern": "function\\s+\\w+\\s*\\("
    }
  },
  "security_patterns": {
    "sql_injection": [
      ["(?i)\\bSELECT\\b.*\\bFROM\\b", "Potential SQL injection via string concatenation"]
    ],
    "command_injection": [
      ["(?i)\\bexec\\b\\s*\\(", "Potential command injection via exec()"]
    ]
  },
  "performance_patterns": {
    "nested_loops": "(?m)^\\s*(for|while)\\b.*\\n\\s*(for|while)\\b",
    "inefficient_filter": "(?i)\\.filter\\s*\\("
  }
}
```

> **Tip**: The regex patterns are applied with `re.IGNORECASE | re.MULTILINE`.

---

## 4
