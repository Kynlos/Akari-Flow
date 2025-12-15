import sys
import os
from pathlib import Path

# Add scripts path
sys.path.append(os.path.join(os.getcwd(), '.github', 'scripts'))

try:
    # Import as module
    # We need to handle the fact that generate-docs.py has a hyphen.
    # We can use importlib
    import importlib.util
    spec = importlib.util.spec_from_file_location("generate_docs", ".github/scripts/generate-docs.py")
    generate_docs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(generate_docs)
    
    extract_symbols = generate_docs.extract_symbols_detailed
except ImportError as e:
    print(f"Import failed: {e}")
    sys.exit(1)

code = """
def hello_world():
    print("Hello")

class MyClass:
    def method(self):
        pass
"""

print("Testing Extraction...")
symbols = extract_symbols(code, "test.py")
print("Symbols found:", len(symbols))
for s in symbols:
    print(f"- {s['type']}: {s['name']} (line {s['lineno']})")
    print(f"  Signature: {s['signature']}")
