import sys
import os
# Add the specific directory to sys.path
sys.path.append(os.path.join(os.getcwd(), '.github', 'scripts', 'polyglot'))

try:
    from polyglot_analyzer import PolyglotAnalyzer
except ImportError as e:
    print(f"Still failed to import: {e}")
    sys.exit(1)

print("Instantiating PolyglotAnalyzer...")
try:
    analyzer = PolyglotAnalyzer()
    print("Analyzer instantiated.")
except Exception as e:
    print(f"Failed to instantiate: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

code = """
def hello():
    pass
"""
print("Testing extract_symbols...")
try:
    symbols = analyzer.extract_symbols(code, '.py')
    print(f"Symbols found: {symbols}")
except Exception as e:
    print(f"Error extracting symbols: {e}")
    import traceback
    traceback.print_exc()
