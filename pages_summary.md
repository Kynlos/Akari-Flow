# GitHub Pages Update Summary

**Changes Made:** 38

### code-analyzer.ts -> api/code-analyzer.md
- **Action:** CREATE
- **Reasoning:** The code-analyzer script introduces a new multi‑language static analysis tool with its own API and CLI, which is not covered by any existing documentation pages, so it should have a dedicated page.

### code-analyzer.ts -> modules/code-analyzer.md
- **Action:** CREATE
- **Reasoning:** The code-analyzer module is not currently documented in any existing page, so a dedicated documentation page is needed.

### code-analyzer.ts -> features/code-analyzer.md
- **Action:** CREATE
- **Reasoning:** There is no existing documentation page covering the Code Analyzer feature; a dedicated page is needed to expose its API, usage, and configuration.

### generate-docs.ts -> api/generate-docs.md
- **Action:** CREATE
- **Reasoning:** The generate-docs.ts script introduces a distinct CI/CD helper functionality not covered by existing API pages, warranting a dedicated documentation page.

### generate-docs.ts -> modules/generate-docs.md
- **Action:** CREATE
- **Reasoning:** The generate-docs script introduces a new CI/CD documentation generation capability not covered by any existing module pages, so a dedicated page is needed.

### generate-docs.ts -> features/auto-docs-generator.md
- **Action:** CREATE
- **Reasoning:** The generate-docs script introduces a distinct capability—automated documentation, changelog, and PR comment generation— that is not covered by existing pages. Adding a dedicated feature page best highlights its purpose, usage, and integration in the CI/CD workflow.

### __init__.ts -> modules/polyglot_analysis.md
- **Action:** CREATE
- **Reasoning:** The package initializer __init__.py has no existing documentation page; creating a dedicated page documents the package overview and usage without cluttering other module pages.

### __init__.ts -> features/polyglot-analysis.md
- **Action:** CREATE
- **Reasoning:** The __init__ file offers a package‑level overview and has no existing documentation page; a dedicated page introduces the Polyglot Analysis package, its purpose, and usage guidance.

### dependency_mapper.ts -> api/dependency-mapper.md
- **Action:** CREATE
- **Reasoning:** The DependencyMapper utility is a distinct component not covered by any existing documentation pages, so a dedicated page is needed to expose its API, usage, and class details.

### dependency_mapper.ts -> modules/dependency-mapper.md
- **Action:** CREATE
- **Reasoning:** The DependencyMapper utility is a new cross‑language dependency graph builder not covered by any existing module page, so a dedicated documentation page should be created.

### dependency_mapper.ts -> features/dependency-mapper.md
- **Action:** CREATE
- **Reasoning:** The DependencyMapper utility introduces a distinct feature (multi‑language dependency graph generation) that is not covered by any existing feature pages, so a dedicated documentation page is needed.

### polyglot_analyzer.ts -> api/polyglot-analyzer.md
- **Action:** CREATE
- **Reasoning:** The polyglot analyzer is a distinct, self‑contained module not covered by any existing documentation pages. Adding a dedicated page preserves modularity and makes it discoverable alongside other API references.

### polyglot_analyzer.ts -> features/polyglot-analyzer.md
- **Action:** CREATE
- **Reasoning:** The polyglot analyzer is a distinct, self‑contained feature not covered by any existing documentation pages, so a dedicated page should be added.

### polyglot_analyzer.ts -> modules/polyglot-analyzer.md
- **Action:** CREATE
- **Reasoning:** The polyglot analyzer provides a unique source‑code analysis capability not covered by any existing module pages, so a dedicated documentation page is required.

### check_imports.ts -> features/debug_import.md
- **Action:** APPEND
- **Reasoning:** The check_imports script is a diagnostic utility that fits the existing Debug Import feature, so it should be added as a new section to that page rather than creating a separate page.

### debug_api.ts -> features/debug-api.md
- **Action:** CREATE
- **Reasoning:** The generated documentation for `debug_api.ts` introduces a distinct demo script not covered by any existing feature pages, so a dedicated page is needed.

### debug_api.ts -> api/debug_api.md
- **Action:** CREATE
- **Reasoning:** The debug_api script is a standalone demo not covered by any existing API pages, so a dedicated documentation page is needed.

### debug_api_cursor.ts -> features/debug-api-cursor.md
- **Action:** CREATE
- **Reasoning:** The script demonstrates Tree‑Sitter QueryCursor usage and is not covered by any existing feature page, so a dedicated documentation page is needed.

### debug_polyglot.ts -> features/debug-polyglot.md
- **Action:** CREATE
- **Reasoning:** The debug_polyglot script is a standalone debugging helper for the PolyglotAnalyzer and does not fit into any existing feature pages, so a new documentation page is needed.

### debug_ts.ts -> api/debug_ts.md
- **Action:** CREATE
- **Reasoning:** The debug_ts script is a new demo utility not covered by any existing API pages, so a dedicated documentation page is required.

### debug_ts.ts -> features/debug-ts.md
- **Action:** CREATE
- **Reasoning:** The documentation describes a standalone demo script for TypeScript symbol extraction, which is not covered by any existing feature page. Adding a dedicated page introduces this new topic and makes the guide discoverable.

### debug_ts_query.ts -> features/debug-ts-query.md
- **Action:** CREATE
- **Reasoning:** The script provides a unique debugging utility for Tree‑Sitter TypeScript queries and does not fit into any existing feature pages, so a dedicated documentation page is needed.

### dump_go_tree.ts -> api/dump_go_tree.md
- **Action:** CREATE
- **Reasoning:** The script is a standalone demo of the PolyglotAnalyzer Go parsing API and does not belong to any existing documentation page, so a new page should be created to capture its usage and examples.

### dump_go_tree.ts -> features/polyglot-analyzer.md
- **Action:** CREATE
- **Reasoning:** The dump_go_tree script introduces the PolyglotAnalyzer API for parsing Go code, which is not covered by any existing feature pages. Creating a dedicated page documents this new capability and provides usage examples for users.

### dump_ts_tree.ts -> features/dump-ts-tree.md
- **Action:** CREATE
- **Reasoning:** The AST dump utility is a standalone script not covered by existing feature pages, so a dedicated documentation page is needed.

### inspect_parser.ts -> features/inspect-parser.md
- **Action:** CREATE
- **Reasoning:** The inspect_parser script is a distinct debugging/introspection utility not covered by any existing feature pages. Creating a dedicated page provides clear, focused documentation and keeps related content organized.

### inspect_query.ts -> features/tree-sitter-query.md
- **Action:** CREATE
- **Reasoning:** The script introduces a unique Tree‑Sitter query introspection feature not covered by any existing documentation pages, warranting a dedicated feature page.

### inspect_query.ts -> modules/inspect-query.md
- **Action:** CREATE
- **Reasoning:** The script provides a distinct utility for Tree‑Sitter query introspection and is not covered by any existing module pages. Creating a dedicated page keeps documentation organized and makes the utility discoverable.

### inspect_ts_binding.ts -> api/inspect-ts-binding.md
- **Action:** CREATE
- **Reasoning:** The script provides a unique demo of the tree_sitter_typescript binding and is not covered by any existing API page, so a dedicated documentation page is needed.

### inspect_ts_binding.ts -> features/inspect-ts-binding.md
- **Action:** CREATE
- **Reasoning:** The script provides a standalone utility for inspecting the tree_sitter_typescript binding, which is not covered by existing feature pages. Creating a dedicated page keeps documentation organized and discoverable.

### inspect_ts_module.ts -> features/inspect-ts-module.md
- **Action:** CREATE
- **Reasoning:** The script is a standalone demo for Tree‑Sitter introspection and does not fit any existing feature pages, so a dedicated documentation page should be created.

### inspect_ts_module.ts -> modules/inspect_ts_module.md
- **Action:** CREATE
- **Reasoning:** The script is a standalone demo for Tree‑Sitter introspection and does not belong to any existing module documentation. Creating a dedicated page keeps the documentation organized and discoverable.

### test_doc_integration.ts -> features/test-doc-integration.md
- **Action:** CREATE
- **Reasoning:** The script is a new internal integration test not covered elsewhere; creating a dedicated page documents its purpose and usage for developers.

### test_doc_integration.ts -> modules/test-doc-integration.md
- **Action:** CREATE
- **Reasoning:** The integration test script is a standalone utility not covered by existing module pages; creating a dedicated page documents its purpose and usage without cluttering other modules.

### test_dependency_mapper.ts -> api/test_dependency_mapper.md
- **Action:** CREATE
- **Reasoning:** The test module introduces a new documentation topic (unit‑test suite for DependencyMapper) that does not exist in the current API docs, so a dedicated page should be created.

### test_polyglot.ts -> api/test_polyglot.md
- **Action:** CREATE
- **Reasoning:** The file is a unit‑test suite for PolyglotAnalyzer, not part of the public library API. It should be documented separately to keep functional module pages focused on production code while still providing developers insight into test coverage.

### test_polyglot.ts -> modules/test-polyglot.md
- **Action:** CREATE
- **Reasoning:** The generated documentation describes a unit‑test suite for PolyglotAnalyzer and does not belong to any existing module page. Creating a dedicated page keeps test documentation separate and discoverable.

### test_polyglot.ts -> features/polyglot-analyzer-tests.md
- **Action:** CREATE
- **Reasoning:** The test suite for PolyglotAnalyzer is a distinct unit‑test module not covered by any existing feature page, so a dedicated documentation page should be created to describe its purpose, structure, and usage.

