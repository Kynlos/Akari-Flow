import sys
import os
sys.path.append(os.path.join(os.getcwd(), '.github', 'scripts', 'polyglot'))

try:
    from polyglot_analyzer import PolyglotAnalyzer
except ImportError:
    sys.exit(1)

analyzer = PolyglotAnalyzer()
code = """
class MyClass {}
interface MyInterface {}
"""
tree = analyzer.parse(code, '.ts')
print(tree.root_node)
