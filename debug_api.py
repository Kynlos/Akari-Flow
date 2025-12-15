import tree_sitter
import tree_sitter_python

try:
    print("Testing API usage...")
    lang = tree_sitter.Language(tree_sitter_python.language())
    print("Language created")
    
    parser = tree_sitter.Parser(lang)
    print("Parser created via constructor")
    
    # Try parsing
    tree = parser.parse(b"def foo(): pass")
    print("Parsed successfully via constructor")
    print(tree.root_node)
    
except Exception as e:
    print(f"Constructor failed: {e}")
    try:
        parser = tree_sitter.Parser()
        parser.language = lang
        print("Parser language set via property")
        
        tree = parser.parse(b"def foo(): pass")
        print("Parsed successfully via property")
    except Exception as e2:
        print(f"Property failed: {e2}")
