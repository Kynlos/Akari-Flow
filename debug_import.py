import sys
import os
import traceback

try:
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '.github', 'scripts'))
    print(f"Adding path: {path}")
    sys.path.append(path)
    
    import diagram_generator
    print("Import successful!")
except Exception:
    traceback.print_exc()
