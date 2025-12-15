import tree_sitter
import tree_sitter_python

try:
    lang = tree_sitter.Language(tree_sitter_python.language())
    query = tree_sitter.Query(lang, "(function_definition) @func")
    parser = tree_sitter.Parser(lang)
    tree = parser.parse(b"def foo(): pass")
    
    print("Testing QueryCursor(query)...")
    try:
        cursor = tree_sitter.QueryCursor(query)
        print("Cursor created with query arg")
        captures = cursor.captures(tree.root_node)
        print(f"Captures type: {type(captures)}")
        # Check first item
        matches = list(captures)
        print(f"Match count: {len(matches)}")
        if matches:
            print(f"First match type: {type(matches[0])}")
            print(f"First match content: {matches[0]}")
    except Exception as e:
        print(f"QueryCursor(query) failed: {e}")
        
    print("Testing QueryCursor() without args...")
    try:
        cursor2 = tree_sitter.QueryCursor()
        print("Cursor created without args")
    except Exception as e:
        print(f"QueryCursor() failed: {e}")

except Exception as e:
    print(f"General Error: {e}")
