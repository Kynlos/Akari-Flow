import tree_sitter
import tree_sitter_typescript

lang = tree_sitter.Language(tree_sitter_typescript.language_typescript())

patterns = [
    "(function_declaration name: (identifier) @name.definition)",
    "(class_declaration name: (identifier) @name.definition)",
    "(interface_declaration name: (identifier) @name.definition)",
    "(method_definition name: (property_identifier) @name.definition)"
]

print("Testing TS patterns...")
for i, pattern in enumerate(patterns):
    try:
        q = tree_sitter.Query(lang, pattern)
        print(f"Pattern {i} OK: {pattern.strip()}")
    except Exception as e:
        print(f"Pattern {i} FAILED: {pattern.strip()} -> {e}")
