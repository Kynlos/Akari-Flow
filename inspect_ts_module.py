import tree_sitter
import tree_sitter_python

print("tree_sitter dir:", dir(tree_sitter))

try:
    if hasattr(tree_sitter, 'QueryCursor'):
        print("Has QueryCursor")
        print(dir(tree_sitter.QueryCursor))
    
    lang = tree_sitter.Language(tree_sitter_python.language())
    query = tree_sitter.Query(lang, "(function_definition) @func")
    print("Query created via constructor")
    print(dir(query))
    
except Exception as e:
    print(f"Error: {e}")
