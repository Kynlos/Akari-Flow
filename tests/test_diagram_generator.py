import unittest
import sys
import os
from pathlib import Path

# Fix paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.github', 'scripts')))

from diagram_generator import DiagramGenerator

class TestDiagramGenerator(unittest.TestCase):
    def test_python_class_diagram(self):
        code = """
class Animal:
    def speak(self): pass

class Dog(Animal):
    def speak(self): pass
    def bark(self): pass
"""
        gen = DiagramGenerator()
        gen._parse_python(code)
        diagram = gen.generate_class_diagram()
        
        self.assertIn("class Animal", diagram)
        self.assertIn("class Dog", diagram)
        self.assertIn("Animal <|-- Dog", diagram)
        self.assertIn("+speak()", diagram)

    def test_regex_diagram(self):
        code = """
class User extends BaseEntity {
    public void login() {}
}
"""
        gen = DiagramGenerator()
        gen._parse_regex(code)
        diagram = gen.generate_class_diagram()
        
        self.assertIn("class User", diagram)
        self.assertIn("BaseEntity <|-- User", diagram)

if __name__ == '__main__':
    unittest.main()
