import os
from pathlib import Path
from .polyglot_analyzer import PolyglotAnalyzer

class DependencyMapper:
    def __init__(self, workspace_root):
        self.root = Path(workspace_root)
        self.analyzer = PolyglotAnalyzer()
        self.file_map = {} # path -> symbols/imports
        self.dependency_graph = {} # path -> [dependencies]

    def scan_workspace(self):
        """Scan all supported files in workspace"""
        for root, _, files in os.walk(self.root):
            for file in files:
                ext = os.path.splitext(file)[1]
                if ext in ['.py', '.js', '.ts', '.tsx', '.go', '.rs', '.java']:
                    full_path = Path(root) / file
                    self.analyze_file(full_path)

    def analyze_file(self, file_path: Path):
        """Analyze a single file for content"""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            rel_path = file_path.relative_to(self.root).as_posix() # Normalize to forward slashes
            ext = file_path.suffix
            
            imports = self.analyzer.extract_imports(content, ext)
            symbols = self.analyzer.extract_symbols(content, ext)
            
            self.file_map[rel_path] = {
                'imports': imports,
                'symbols': [s['name'] for s in symbols],
                'path': str(file_path)
            }
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")

    def build_graph(self):
        """Build dependency graph from analyzed files"""
        for source_file, data in self.file_map.items():
            deps = []
            for imp in data['imports']:
                # Basic Resolution Logic
                resolved = self._resolve_import(imp, source_file)
                if resolved:
                    deps.append(resolved)
            self.dependency_graph[source_file] = deps
            
        return self.dependency_graph

    def _resolve_import(self, import_str, source_file):
        """Try to resolve an import string to a file in file_map"""
        # source_file is a key in file_map (posix relative path)
        
        # 1. Exact match (rare)
        if import_str in self.file_map:
            return import_str
            
        # 2. Python module resolution (dots to slashes)
        # simplistic
        py_path = import_str.replace('.', '/') + '.py'
        if py_path in self.file_map:
            return py_path
            
        # 3. TS/JS local resolution
        if import_str.startswith('.'):
            # relative path from source_file
            # source_file is e.g. "src/app.ts"
            source_dir = Path(source_file).parent # This uses OS sep if source_file string is passed to Path?
            # Wait, Path("src/app.ts") works on Windows.
            
            # Construct full relative path
            # import "./components/foo" from "app.ts" -> "components/foo"
            try:
                # Use / for join since inputs are posix-ish or import strings
                # Just use Path logic then as_posix
                base = Path(source_file).parent
                target = (base / import_str).resolve() 
                # resolve() makes it absolute based on CWD if not careful, 
                # but we are dealing with relative paths abstractly?
                # NO. Path("app.ts") is relative. (Path("app.ts") / "./foo").resolve() is absolute CWD/foo...
                # We want purely relative math.
                
                # Simpler relative math without resolve (which hits filesystem)
                # "app.ts" -> dir "". "" + "./comp" -> "comp".
                # "src/app.ts" -> dir "src". "src" + "../utils" -> "utils".
                
                # Let's use posixpath for string manipulation correctness
                import posixpath
                source_dir = posixpath.dirname(source_file)
                target_base = posixpath.normpath(posixpath.join(source_dir, import_str))
                
                # Try extensions
                for ext in ['.ts', '.tsx', '.js', '.jsx']:
                    candidate = target_base + ext
                    if candidate in self.file_map:
                        return candidate
                        
                    # Also try index files? skipping for now
            except Exception:
                pass

        # Search by basename (fuzzy fallback)
        for f in self.file_map:
            if import_str in f:
                return f
                
        return None
