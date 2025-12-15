import os
import tree_sitter
from pathlib import Path

# Import language bindings
try:
    import tree_sitter_python
    import tree_sitter_javascript
    import tree_sitter_typescript
    import tree_sitter_go
    import tree_sitter_rust
    import tree_sitter_java
except ImportError as e:
    print(f"Warning: Tree-sitter bindings missing: {e}")

class PolyglotAnalyzer:
    def __init__(self):
        self.parsers = {}
        self.languages = {}
        self._initialize_languages()
        
    def _initialize_languages(self):
        """Initialize parsers for supported languages"""
        try:
            # Python
            self.languages['py'] = tree_sitter.Language(tree_sitter_python.language())
            self.parsers['py'] = tree_sitter.Parser(self.languages['py'])
            
            # JavaScript
            self.languages['js'] = tree_sitter.Language(tree_sitter_javascript.language())
            self.parsers['js'] = tree_sitter.Parser(self.languages['js'])
            
            # TypeScript
            ts_lang = tree_sitter.Language(tree_sitter_typescript.language_typescript())
            self.languages['ts'] = ts_lang
            self.languages['tsx'] = tree_sitter.Language(tree_sitter_typescript.language_tsx())
            
            self.parsers['ts'] = tree_sitter.Parser(self.languages['ts'])
            self.parsers['tsx'] = tree_sitter.Parser(self.languages['tsx'])
            
            # Go
            self.languages['go'] = tree_sitter.Language(tree_sitter_go.language())
            self.parsers['go'] = tree_sitter.Parser(self.languages['go'])
            
            # Rust
            self.languages['rs'] = tree_sitter.Language(tree_sitter_rust.language())
            self.parsers['rs'] = tree_sitter.Parser(self.languages['rs'])
            
            # Java
            self.languages['java'] = tree_sitter.Language(tree_sitter_java.language())
            self.parsers['java'] = tree_sitter.Parser(self.languages['java'])
            
        except Exception as e:
            print(f"Error initializing Tree-sitter parsers: {e}")

    def parse(self, content: str, extension: str):
        """Parse content and return tree"""
        ext = extension.lstrip('.').lower()
        parser = self.parsers.get(ext)
        if not parser:
            return None
        
        return parser.parse(bytes(content, "utf8"))

    def extract_symbols(self, content: str, extension: str):
        """Extract functions and classes using Tree-sitter queries"""
        ext = extension.lstrip('.').lower()
        tree = self.parse(content, extension)
        if not tree:
            return []
            
        lang = self.languages.get(ext)
        if not lang:
            return []
            
        query_scm = self._get_query_for_lang(ext)
        if not query_scm:
            return []
            
        query = tree_sitter.Query(lang, query_scm)
        cursor = tree_sitter.QueryCursor(query)
        captures = cursor.captures(tree.root_node)
        
        symbols = []
        # captures is a dict: { 'name.definition': [Node, Node] } or similar
        for tag_name, nodes in captures.items():
             # Ensure nodes is a list (API consistency check)
            if not isinstance(nodes, list):
                nodes = [nodes]
                
            for node in nodes:
                if tag_name == 'name.definition':
                    # Determine type based on parent
                    kind = 'variable'
                    parent_type = node.parent.type
                    
                    if 'function' in parent_type or 'method' in parent_type or 'func' in parent_type:
                        kind = 'function'
                    elif 'class' in parent_type or 'struct' in parent_type or 'interface' in parent_type:
                        kind = 'class'
                    
                    # Get signature (simplification)
                    signature = content[node.parent.start_byte:node.parent.end_byte].split('\n')[0]
                    
                    symbols.append({
                        'name': content[node.start_byte:node.end_byte],
                        'kind': kind,
                        'line': node.start_point[0] + 1,
                        'end_line': node.end_point[0] + 1,
                        'signature': signature
                    })
                
        return symbols

    def extract_imports(self, content: str, extension: str):
        """Extract imported modules/files"""
        ext = extension.lstrip('.').lower()
        tree = self.parse(content, extension)
        if not tree:
            return []
            
        lang = self.languages.get(ext)
        if not lang:
            return []
            
        query_scm = self._get_import_query_for_lang(ext)
        if not query_scm:
            return []
            
        query = tree_sitter.Query(lang, query_scm)
        cursor = tree_sitter.QueryCursor(query)
        captures = cursor.captures(tree.root_node)
        
        imports = []
        for tag_name, nodes in captures.items():
            if not isinstance(nodes, list):
                nodes = [nodes]
            for node in nodes:
                 # Extract raw text for now
                 text = content[node.start_byte:node.end_byte].strip('"\'')
                 imports.append(text)
                 
        return imports

    def _get_query_for_lang(self, ext):
        """Return Tree-sitter mapping query for symbols"""
        # Generic-ish queries
        if ext == 'py':
            return """
            (function_definition name: (identifier) @name.definition)
            (class_definition name: (identifier) @name.definition)
            """
        elif ext in ['ts', 'tsx', 'js', 'jsx']:
            return """
            (function_declaration name: (identifier) @name.definition)
            (class_declaration name: (type_identifier) @name.definition)
            (interface_declaration name: (type_identifier) @name.definition)
            (method_definition name: (property_identifier) @name.definition)
            """
        elif ext == 'go':
            return """
            (function_declaration name: (identifier) @name.definition)
            (method_declaration name: (field_identifier) @name.definition)
            (type_declaration (type_spec name: (type_identifier) @name.definition))
            """
        elif ext == 'rs':
            return """
            (function_item name: (identifier) @name.definition)
            (struct_item name: (type_identifier) @name.definition)
            (impl_item . (type_identifier) @name.definition)
            """
        elif ext == 'java':
            return """
            (method_declaration name: (identifier) @name.definition)
            (class_declaration name: (identifier) @name.definition)
            (interface_declaration name: (identifier) @name.definition)
            """
        return None

    def _get_import_query_for_lang(self, ext):
        if ext == 'py':
            return """
            (import_from_statement module_name: (dotted_name) @import)
            (import_statement name: (dotted_name) @import)
            """
        elif ext in ['ts', 'tsx', 'js', 'jsx']:
            return """
            (import_statement source: (string (string_fragment) @import))
            """
        elif ext == 'go':
            return """
            (import_spec path: (_) @import)
            """
        return None
