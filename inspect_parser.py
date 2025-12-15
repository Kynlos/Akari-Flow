import tree_sitter
print(dir(tree_sitter.Parser))
try:
    p = tree_sitter.Parser()
    print("Parser instantiated without args")
    print(dir(p))
except Exception as e:
    print(f"Parser() failed: {e}")
