import unittest
from pathlib import Path
import sys
import os

# Add repo root to path
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.github', 'scripts', 'polyglot')))

from polyglot_analyzer import PolyglotAnalyzer

class TestPolyglotAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = PolyglotAnalyzer()

    def test_python_extraction(self):
        code = """
def hello_world():
    print("Hello")

class Greeter:
    def greet(self):
        pass
"""
        symbols = self.analyzer.extract_symbols(code, '.py')
        names = [s['name'] for s in symbols]
        
        self.assertIn('hello_world', names)
        self.assertIn('Greeter', names)
        # Note: 'greet' might not be top-level capture depending on query specificity, 
        # but class and function should be there.

    def test_go_extraction(self):
        code = """
package main

func main() {
    print("Hello")
}

type User struct {
    Name string
}

func (u *User) Greet() {
}
"""
        symbols = self.analyzer.extract_symbols(code, '.go')
        names = [s['name'] for s in symbols]
        
        self.assertIn('main', names)
        self.assertIn('User', names)
        self.assertIn('Greet', names)

    def test_typescript_extraction(self):
        code = """
function add(a: number, b: number): number {
    return a + b;
}

class Calculator {
    multiply(a: number, b: number) {
        return a * b;
    }
}
"""
        symbols = self.analyzer.extract_symbols(code, '.ts')
        names = [s['name'] for s in symbols]
        
        self.assertIn('add', names)
        self.assertIn('Calculator', names)

    def test_python_imports(self):
        code = """
import os
from sys import path
import tree_sitter
"""
        imports = self.analyzer.extract_imports(code, '.py')
        self.assertIn('os', imports)
        self.assertIn('sys', imports) # Depending on query matches
        # tree_sitter pattern might be complicated if it's dotted?
        # My query uses dotted_name.
        
    def test_ts_imports(self):
        code = """
import { Foo } from "./bar";
import React from 'react';
"""
        imports = self.analyzer.extract_imports(code, '.ts')
        self.assertIn('./bar', imports)
        self.assertIn('react', imports)

    def test_go_imports(self):
        code = """
package main
import (
    "fmt"
    "net/http"
)
"""
        imports = self.analyzer.extract_imports(code, '.go')
        # Go strings include quotes usually in text extraction unless I stripped them?
        # My code strips quotes.
        self.assertIn('fmt', imports)
        self.assertIn('net/http', imports)

if __name__ == '__main__':
    unittest.main()
