import sys
import os
sys.path.append(os.path.join(os.getcwd(), '.github', 'scripts', 'polyglot'))

try:
    from polyglot_analyzer import PolyglotAnalyzer
except ImportError:
    sys.exit(1)

analyzer = PolyglotAnalyzer()
code = """
package main
import "fmt"
import (
    "net/http"
)
"""
tree = analyzer.parse(code, '.go')
print(tree.root_node)
