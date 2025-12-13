#!/usr/bin/env python3
"""
Diagram Generator
Generates Mermaid.js class diagrams and flowcharts from code analysis.
"""

import os
import re
import ast
import sys
from pathlib import Path
from typing import Dict, List, Optional

class DiagramGenerator:
    def __init__(self):
        self.classes = {} # name -> {inherits: [], methods: [], props: []}
        self.relationships = [] # (from, to, type)

    def parse_file(self, file_path: str, content: str):
        """Parse file content to extract structure"""
        ext = Path(file_path).suffix.lower()
        if ext == '.py':
            self._parse_python(content)
        elif ext in ['.ts', '.js', '.java', '.cs', '.cpp', '.hpp']:
            self._parse_regex(content)

    def _parse_python(self, content: str):
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_name = node.name
                    inherits = []
                    for base in node.bases:
                        if isinstance(base, ast.Name):
                            inherits.append(base.id)
                    
                    methods = []
                    props = []
                    
                    for item in node.body:
                        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            # Check if private
                            prefix = '-' if item.name.startswith('_') else '+'
                            methods.append(f"{prefix}{item.name}()")
                        elif isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                             props.append(f"+{item.target.id}")

                    self.classes[class_name] = {
                        'inherits': inherits,
                        'methods': methods,
                        'props': props
                    }
                    
                    for base in inherits:
                        if base not in self.classes:
                            self.classes[base] = {'inherits': [], 'methods': [], 'props': []}
                        self.relationships.append((base, class_name, '<|--'))
                        
        except Exception as e:
            print(f"Error parsing Python AST: {e}")

    def _parse_regex(self, content: str):
        # Basic regex parsing for other languages
        # Matches: class ClassName extends BaseClass {
        class_pattern = r'class\s+(\w+)(?:\s+(?:extends|:)\s+(\w+))?'
        
        for match in re.finditer(class_pattern, content):
            class_name = match.group(1)
            base_class = match.group(2)
            
            if class_name not in self.classes:
                self.classes[class_name] = {'inherits': [], 'methods': [], 'props': []}
            
            if base_class:
                if base_class not in self.classes:
                    self.classes[base_class] = {'inherits': [], 'methods': [], 'props': []}
                
                self.classes[class_name]['inherits'].append(base_class)
                self.relationships.append((base_class, class_name, '<|--'))

        # Methods (rough heuristic)
        # functionName(...) { or void functionName(...)
        method_pattern = r'(?:public|private|protected)?\s*(?:static)?\s*[\w<>\[\]]+\s+(\w+)\s*\('
        # This is very loose, mainly for demo purposes on static typed langs like Java/TS
        
        # Refined pattern for method-like structures inside classes would require content slicing
        # For now, we leave methods empty for regex-based langs to avoid noise

    def generate_class_diagram(self) -> str:
        if not self.classes:
            return ""
            
        lines = ["classDiagram"]
        
        for cls, data in self.classes.items():
            lines.append(f"    class {cls} {{")
            for prop in data['props'][:5]: # Limit to 5
                lines.append(f"        {prop}")
            for method in data['methods'][:5]: # Limit to 5
                lines.append(f"        {method}")
            lines.append("    }")
        
        for src, dst, rel in self.relationships:
            # Only add relationship if both nodes exist (to avoid clutter)
            if src in self.classes and dst in self.classes:
                lines.append(f"    {src} {rel} {dst}")
                
        return "\n".join(lines)

def main():
    if len(sys.argv) < 2:
        print("Usage: diagram-generator.py <file_path>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        sys.exit(0)
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    generator = DiagramGenerator()
    generator.parse_file(file_path, content)
    diagram = generator.generate_class_diagram()
    
    if diagram:
        print(diagram)

if __name__ == '__main__':
    main()
