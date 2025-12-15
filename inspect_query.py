import tree_sitter
import tree_sitter_python

try:
    lang = tree_sitter.Language(tree_sitter_python.language())
    query_src = "(function_definition name: (identifier) @name.definition)"
    query = lang.query(query_src)
    
    print("Query object methods:")
    print(dir(query))
    
    parser = tree_sitter.Parser(lang)
    tree = parser.parse(b"def foo(): pass")
    
    # Try probable alternatives
    if hasattr(query, 'captures'):
        print("Has captures method")
    if hasattr(query, 'matches'):
        print("Has matches method")
        
except Exception as e:
    print(f"Inspection failed: {e}")
