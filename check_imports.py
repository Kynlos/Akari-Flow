try:
    import tree_sitter
    print("tree_sitter imported")
    import tree_sitter_python
    print("tree_sitter_python imported")
    print(dir(tree_sitter_python))
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Error: {e}")
