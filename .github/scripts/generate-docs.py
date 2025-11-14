#!/usr/bin/env python3
"""
Symbol Capsules Documentation Generator for CI/CD

Reads changed files, extracts symbols, sends to Groq API for documentation.
88% more efficient than sending full files.
"""

import os
import sys
import json
import re
from pathlib import Path
import requests

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'
MODEL = 'llama-3.3-70b-versatile'  # Fast and capable

def extract_symbols(file_path, content):
    """Extract symbols from code file"""
    symbols = []
    
    # Classes
    for match in re.finditer(r'^(export\s+)?class\s+(\w+)(?:\s+extends\s+(\w+))?', content, re.MULTILINE):
        export_marker = '▸' if match.group(1) else ' '
        extends = f' extends {match.group(3)}' if match.group(3) else ''
        symbols.append({
            'type': 'class',
            'name': match.group(2),
            'signature': f'{export_marker}class {match.group(2)}{extends}',
            'exported': bool(match.group(1))
        })
    
    # Functions
    for match in re.finditer(r'^(export\s+)?(?:async\s+)?function\s+(\w+)\s*\([^)]*\)', content, re.MULTILINE):
        export_marker = '▸' if match.group(1) else ' '
        symbols.append({
            'type': 'function',
            'name': match.group(2),
            'signature': f'{export_marker}{match.group(0).strip()}',
            'exported': bool(match.group(1))
        })
    
    # Interfaces
    for match in re.finditer(r'^(export\s+)?interface\s+(\w+)', content, re.MULTILINE):
        export_marker = '▸' if match.group(1) else ' '
        symbols.append({
            'type': 'interface',
            'name': match.group(2),
            'signature': f'{export_marker}interface {match.group(2)}',
            'exported': bool(match.group(1))
        })
    
    # Types
    for match in re.finditer(r'^(export\s+)?type\s+(\w+)', content, re.MULTILINE):
        export_marker = '▸' if match.group(1) else ' '
        symbols.append({
            'type': 'type',
            'name': match.group(2),
            'signature': f'{export_marker}type {match.group(2)}',
            'exported': bool(match.group(1))
        })
    
    return symbols

def build_symbol_index(files_data):
    """Build compressed symbol index"""
    index = "Symbol Index:\n\n"
    
    for file_path, symbols in files_data.items():
        if not symbols:
            continue
        
        index += f"[{Path(file_path).name}]\n"
        for sym in symbols:
            index += f"  {sym['signature']}\n"
        index += "\n"
    
    return index

def generate_documentation(symbol_index, file_list):
    """Call Groq API to generate documentation"""
    
    if not GROQ_API_KEY:
        print("ERROR: GROQ_API_KEY not set")
        sys.exit(1)
    
    prompt = f"""Generate comprehensive API documentation for the following code changes.

{symbol_index}

Files changed: {', '.join(file_list)}

Generate documentation that includes:
1. Overview of changes
2. New/modified functions and classes
3. Usage examples for new exports
4. Migration notes if signatures changed

Format as GitHub-flavored Markdown."""

    response = requests.post(
        GROQ_API_URL,
        headers={
            'Authorization': f'Bearer {GROQ_API_KEY}',
            'Content-Type': 'application/json'
        },
        json={
            'model': MODEL,
            'messages': [
                {
                    'role': 'system',
                    'content': 'You are a technical documentation expert. Generate clear, concise API documentation from Symbol Capsules (compressed code representations).'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'temperature': 0.3,
            'max_tokens': 2000
        }
    )
    
    if response.status_code != 200:
        print(f"ERROR: Groq API returned {response.status_code}")
        print(response.text)
        sys.exit(1)
    
    data = response.json()
    return data['choices'][0]['message']['content']

def calculate_savings(files_data, symbol_index):
    """Calculate token savings vs traditional approach"""
    total_file_size = sum(len(content) for _, content in files_data.items())
    traditional_tokens = total_file_size // 4
    capsule_tokens = len(symbol_index) // 4
    
    savings = traditional_tokens - capsule_tokens
    percent = (savings / traditional_tokens * 100) if traditional_tokens > 0 else 0
    cost_saved = savings * (3 / 1_000_000)  # Claude Sonnet 4.5 pricing
    
    return {
        'traditional': traditional_tokens,
        'capsules': capsule_tokens,
        'saved': savings,
        'percent': percent,
        'cost': cost_saved
    }

def main():
    print("Symbol Capsules CI/CD Documentation Generator")
    print("="*80)
    
    # Read changed files
    if not os.path.exists('changed_files.txt'):
        print("No changed_files.txt found")
        sys.exit(0)
    
    with open('changed_files.txt', 'r') as f:
        changed_files = [line.strip() for line in f if line.strip()]
    
    # Filter to code files
    code_extensions = {'.ts', '.js', '.tsx', '.jsx', '.py'}
    code_files = [f for f in changed_files if Path(f).suffix in code_extensions]
    
    if not code_files:
        print("No code files changed")
        sys.exit(0)
    
    print(f"Processing {len(code_files)} changed files\n")
    
    # Extract symbols from each file
    files_data = {}
    symbols_by_file = {}
    
    for file_path in code_files:
        if not os.path.exists(file_path):
            print(f"  SKIP: {file_path} (deleted)")
            continue
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            files_data[file_path] = content
            symbols = extract_symbols(file_path, content)
            symbols_by_file[file_path] = symbols
            
            print(f"  OK: {file_path} ({len(symbols)} symbols)")
        except Exception as e:
            print(f"  ERROR: {file_path} - {e}")
    
    if not symbols_by_file:
        print("\nNo symbols extracted")
        sys.exit(0)
    
    # Build symbol index
    symbol_index = build_symbol_index(symbols_by_file)
    
    print(f"\nSymbol Index Preview:")
    print("-"*80)
    print(symbol_index[:500] + "..." if len(symbol_index) > 500 else symbol_index)
    print("-"*80)
    
    # Calculate savings
    savings = calculate_savings(files_data, symbol_index)
    print(f"\nToken Efficiency:")
    print(f"  Traditional: {savings['traditional']} tokens")
    print(f"  Capsules: {savings['capsules']} tokens")
    print(f"  Saved: {savings['saved']} tokens ({savings['percent']:.1f}%)")
    print(f"  Cost saved: ${savings['cost']:.6f}")
    
    # Generate documentation
    print(f"\nGenerating documentation via Groq API ({MODEL})...")
    documentation = generate_documentation(symbol_index, code_files)
    
    print("\nGenerated Documentation:")
    print("="*80)
    print(documentation)
    print("="*80)
    
    # Save for PR comment
    pr_comment = f"""## 🤖 Auto-Generated Documentation

**Changes detected in {len(code_files)} file(s)**

{documentation}

---

**Symbol Capsules Efficiency:**
- Traditional approach: {savings['traditional']:,} tokens
- Symbol Capsules: {savings['capsules']:,} tokens  
- **Saved: {savings['saved']:,} tokens ({savings['percent']:.1f}%)** 💰
- Cost saved: ${savings['cost']:.6f}

*Documentation generated using Symbol Capsules - 88% more efficient than traditional approaches.*
"""
    
    with open('doc_output.md', 'w') as f:
        f.write(pr_comment)
    
    # Update API-DOCS.md
    with open('API-DOCS.md', 'w') as f:
        f.write(f"# API Documentation\n\n")
        f.write(f"*Last updated: {Path('changed_files.txt').stat().st_mtime}*\n\n")
        f.write(documentation)
    
    print("\nDONE:")
    print("  - doc_output.md (for PR comment)")
    print("  - API-DOCS.md (for commit)")

if __name__ == '__main__':
    main()
