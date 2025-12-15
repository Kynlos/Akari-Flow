import sys
import os
sys.path.append(os.path.join(os.getcwd(), '.github', 'scripts', 'polyglot'))

try:
    from polyglot_analyzer import PolyglotAnalyzer
except ImportError as e:
    print(f"Import failed: {e}")
    sys.exit(1)

analyzer = PolyglotAnalyzer()
code = """
function add(a: number, b: number): number {
    return a + b;
}
"""
print("Testing TS extraction...")
try:
    symbols = analyzer.extract_symbols(code, '.ts')
    print("Symbols:", symbols)
except Exception as e:
    print(f"TS Extraction Failed: {e}")
    import traceback
    traceback.print_exc()
