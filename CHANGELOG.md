# Changelog

All notable changes to this project will be documented in this file.


## [2025-12-15]

## [2025-12-15]

### code-analyzer.py

### ⚠️ BREAKING CHANGES
- Removed exported class: ASTAnalyzer
- Removed exported function: visit_AsyncFunctionDef
- Removed exported function: visit_FunctionDef
- Removed exported function: visit_ClassDef
- Removed exported function: visit_If
- Removed exported function: visit_For
- Removed exported function: visit_While
- Removed exported function: analyze
- Removed exported function: visit_Try
- Removed exported function: visit_ExceptHandler
### 🗑️ Removed
- `visit_Try` (function)
- `visit_ExceptHandler` (function)
- `analyze` (function)
- `visit_FunctionDef` (function)
- `visit_AsyncFunctionDef` (function)
- `ASTAnalyzer` (class)
- `visit_ClassDef` (function)
- `visit_If` (function)
- `visit_For` (function)
- `visit_While` (function)

### dependency_mapper.py

### ✨ Added
- `DependencyMapper` (class)
- `analyze_file` (function)
- `build_graph` (function)
- `scan_workspace` (function)

### polyglot_analyzer.py

### ✨ Added
- `PolyglotAnalyzer` (class)
- `extract_symbols` (function)
- `parse` (function)
- `extract_imports` (function)

### test_dependency_mapper.py

### ✨ Added
- `TestDependencyMapper` (class)
- `test_scan_and_link` (function)
- `setUp` (function)
- `tearDown` (function)

### test_polyglot.py

### ✨ Added
- `TestPolyglotAnalyzer` (class)
- `test_typescript_extraction` (function)
- `test_python_extraction` (function)
- `test_go_extraction` (function)
- `setUp` (function)
- `test_python_imports` (function)
- `test_ts_imports` (function)
- `test_go_imports` (function)

## [2025-12-13]

## [2025-12-13]

## [2025-12-13]

### diagram_generator.py

### ✨ Added
- `DiagramGenerator` (class)
- `main` (function)
- `parse_file` (function)
- `generate_class_diagram` (function)

### site_generator.py

### ✨ Added
- `build_site` (function)

### cicd-cli.py

### ✨ Added
- `run_script` (function)
- `main` (function)

### test_diagram_generator.py

### ✨ Added
- `TestDiagramGenerator` (class)
- `test_python_class_diagram` (function)
- `test_regex_diagram` (function)

## [2025-12-13]

### code-analyzer.py

### ✨ Added
- `load_config` (function)
- `analyze_file` (function)
- `main` (function)
- `visit_FunctionDef` (function)
- `visit_AsyncFunctionDef` (function)
- `visit_ClassDef` (function)
- `visit_If` (function)
- `visit_For` (function)
- `visit_While` (function)
- `visit_Try` (function)
- `visit_ExceptHandler` (function)
- `analyze` (function)
- `calculate_quality_score` (function)
- `scan_security_vulnerabilities` (function)
- `detect_performance_issues` (function)

## [2025-11-16]

## [2025-11-16]

## [2025-11-16]

## [2025-11-16]

## [2025-11-16]

## [2025-11-16]

## [2025-11-16]

## [2025-11-16]

## [2025-11-16]

## [2025-11-16]

## [2025-11-16]

## [2025-11-16]

## [2025-11-16]

## [2025-11-16]

## [2025-11-16]

## [2025-11-16]

## [2025-11-15]

## [2025-11-15]

## [2025-11-15]

## [2025-11-15]

## [2025-11-15]

## [2025-11-15]

## [2025-11-15]

## [2025-11-15]

## [2025-11-15]

## [2025-11-15]

## [2025-11-15]

## [2025-11-15]

## [2025-11-15]

## [2025-11-15]

## [2025-11-15]

## [2025-11-15]

## [2025-11-15]

## [2025-11-15]

## [2025-11-15]

## [2025-11-15]

## [2025-11-15]

## [2025-11-15]

## [2025-11-15]

## [2025-11-15]

## [2025-11-14]

### email-service.ts

### ✨ Added
- `sendEmail` (function)
- `sendBulkEmails` (function)
- `EmailOptions` (interface)
- `Attachment` (interface)
- `EmailResult` (interface)

## [2025-11-14]

## [2025-11-14]

## [2025-11-14]

## [2025-11-14]

## [2025-11-14]

