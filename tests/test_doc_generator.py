import unittest
import sys
import os

# Add scripts to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '.github', 'scripts'))

# Import as module - might need to adjust if scripts are not modules
# For now we assume we can import specific functions if we refactored enough, 
# or we test the logic we duplicated if we can't import easily.
# Since we refactored, let's try importing.

# Note: generate-docs.py uses hyphens which is hard to import.
# We will use importlib
import importlib.util
spec = importlib.util.spec_from_file_location("generate_docs", os.path.join(os.path.dirname(__file__), '..', '.github', 'scripts', 'generate-docs.py'))
gen_docs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen_docs)

class TestDocGenerator(unittest.TestCase):
    def test_extract_symbols_python(self):
        code = """
def my_func(a, b):
    return a + b

class MyClass:
    pass
"""
        symbols = gen_docs.extract_symbols_detailed(code, 'test.py')
        func = next((s for s in symbols if s['name'] == 'my_func'), None)
        cls = next((s for s in symbols if s['name'] == 'MyClass'), None)
        
        self.assertIsNotNone(func)
        self.assertIsNotNone(cls)
        self.assertEqual(func['type'], 'function')
        
    def test_breaking_change_removal(self):
        old_code = "def old_func(): pass"
        new_code = "def new_func(): pass"
        
        # Must ensure it thinks old_func was exported. 
        # In Python everything is "exported" by default in our simple logic unless _ prefix
        
        result = gen_docs.detect_breaking_changes(old_code, new_code, 'test.py')
        self.assertTrue(result['has_breaking'])
        self.assertEqual(result['changes'][0]['type'], 'removed')
        self.assertEqual(result['changes'][0]['symbol'], 'old_func')

    def test_breaking_change_signature(self):
        old_code = """
def calc(a, b):
    pass
"""
        new_code = """
def calc(a, b, c): # Added required arg
    pass
"""
        # Note: Our simple AST parser currently just joins args.
        # old: "a, b"
        # new: "a, b, c"
        # This should trigger a signature change
        
        result = gen_docs.detect_breaking_changes(old_code, new_code, 'test.py')
        self.assertTrue(result['has_breaking'])
        self.assertEqual(result['changes'][0]['type'], 'signature_change')

if __name__ == '__main__':
    unittest.main()
