import unittest
import shutil
import tempfile
import sys
import os
from pathlib import Path

# Add repo root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.github', 'scripts', 'polyglot')))

# Trick imports if needed, or rely on sys.path allowing direct import
try:
    from dependency_mapper import DependencyMapper
except ImportError:
    # If polyglot is package
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.github', 'scripts')))
    from polyglot.dependency_mapper import DependencyMapper

class TestDependencyMapper(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.root = Path(self.test_dir)
        
        # Create structure
        # main.py
        (self.root / "main.py").write_text("import utils\nfrom sub import lib", encoding="utf-8")
        
        # utils.py
        (self.root / "utils.py").write_text("def helper(): pass", encoding="utf-8")
        
        # sub/lib.py
        (self.root / "sub").mkdir()
        (self.root / "sub" / "lib.py").write_text("class Lib: pass", encoding="utf-8")
        
        # app.ts
        (self.root / "app.ts").write_text("import { foo } from './components/foo';", encoding="utf-8")
        
        # components/foo.ts
        (self.root / "components").mkdir()
        (self.root / "components" / "foo.ts").write_text("export const foo = 1;", encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_scan_and_link(self):
        mapper = DependencyMapper(self.test_dir)
        mapper.scan_workspace()
        
        graph = mapper.build_graph()
        
        print("Dependency Graph:", graph)
        print("File Map Keys:", mapper.file_map.keys())
        
        # Check Python links
        # main.py -> utils.py
        # main.py -> sub/lib.py
        
        # Note: keys are relative strings? My code uses rel_path in analyze_file.
        # Let's see what analyze_file does: 'rel_path = str(file_path.relative_to(self.root))'
        
        main_deps = graph.get('main.py', [])
        self.assertTrue(any('utils.py' in d for d in main_deps), f"utils.py not found in {main_deps}")
        self.assertTrue(any('sub' in d and 'lib' in d for d in main_deps), f"sub/lib not found in {main_deps}")
        
        # Check TS link
        # app.ts -> (implied ./components/foo)
        app_deps = graph.get('app.ts', [])
        # My resolver is fuzzy fallback, might verify 'foo' in name
        self.assertTrue(any('foo' in d for d in app_deps), f"foo component not linked in {app_deps}")

if __name__ == '__main__':
    unittest.main()
