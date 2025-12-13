import unittest
import sys
import os
from pathlib import Path

# Add scripts to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '.github', 'scripts'))

import importlib.util

# Load code-analyzer.py
spec = importlib.util.spec_from_file_location("code_analyzer", os.path.join(os.path.dirname(__file__), '..', '.github', 'scripts', 'code-analyzer.py'))
code_analyzer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(code_analyzer)

ASTAnalyzer = code_analyzer.ASTAnalyzer
CodeAnalyzer = code_analyzer.CodeAnalyzer

class TestASTAnalyzer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load config once
        try:
            code_analyzer.load_config()
        except:
            pass # Config might fail if paths are wrong in test env, but default empty global is fine for AST checks largely

    def setUp(self):
        self.python_code = """
def hello():
    print("Hello world")

class MyClass:
    def method(self):
        pass

def complex_func():
    if True:
        try:
            pass
        except:
            pass
"""

    def test_symbol_extraction(self):
        analyzer = ASTAnalyzer(self.python_code)
        stats = analyzer.analyze()
        
        # hello, method, complex_func -> method is inside class, so ASTAnalyzer visits FunctionDef twice?
        # Let's check visit_FunctionDef logic in code-analyzer.py
        # It visits FunctionDef. It does not check if it's inside a class.
        # So "hello" (1), "method" (1), "complex_func" (1) = 3 functions.
        self.assertEqual(len(stats['functions']), 3) 
        self.assertEqual(len(stats['classes']), 1)

    def test_complexity(self):
        code = """
def complex():
    if a:
        if b:
            pass
    for i in range(10):
        pass
"""
        analyzer = ASTAnalyzer(code)
        stats = analyzer.analyze()
        # 2 ifs + 1 for = 3 decision points
        self.assertEqual(stats['decision_points'], 3)

if __name__ == '__main__':
    unittest.main()
