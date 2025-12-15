import tree_sitter_typescript
print(dir(tree_sitter_typescript))
try:
    print("TypeScript type:", type(tree_sitter_typescript.language_typescript()))
except Exception as e:
    print(f"TS Error: {e}")

try:
    print("TSX type:", type(tree_sitter_typescript.language_tsx()))
except Exception as e:
    print(f"TSX Error: {e}")
