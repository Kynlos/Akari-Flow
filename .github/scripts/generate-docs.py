#!/usr/bin/env python3
"""
Advanced Auto Documentation Generator for CI/CD

Features:
1. Breaking change detection with auto-labeling
2. Changelog generation
3. Diff-aware documentation (only changed code)
4. Cross-file impact analysis
5. Smart PR comments
6. AST-based parsing (Python)
7. Content Hashing (Caching)
"""

import os
import sys
import json
import re
import ast
import hashlib
from pathlib import Path
from datetime import datetime
import requests

# Load Config
CONFIG_PATH = Path(__file__).parent.parent / 'config' / 'languages.json'
LANGUAGE_CONFIG = {}

if CONFIG_PATH.exists():
    try:
        with open(CONFIG_PATH, 'r') as f:
            LANGUAGE_CONFIG = json.load(f).get('languages', {})
    except:
        pass

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'
MODEL = 'openai/gpt-oss-20b'

def get_file_hash(content):
    """Generate SHA256 hash of content"""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def extract_symbols_detailed(content, file_path):
    """Extract symbols with detailed information using AST for Python, Regex for others"""
    symbols = []
    ext = Path(file_path).suffix.lower()
    
    # Python AST Parsing
    if ext == '.py':
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    params = ', '.join(arg.arg for arg in node.args.args)
                    symbols.append({
                        'type': 'function',
                        'name': node.name,
                        'params': params,
                        'returns': 'Any', # AST doesn't always have easy return type inference without type hints
                        'exported': not node.name.startswith('_'),
                        'signature': f"def {node.name}({params})",
                        'lineno': node.lineno
                    })
                elif isinstance(node, ast.ClassDef):
                     symbols.append({
                        'type': 'class',
                        'name': node.name,
                        'exported': not node.name.startswith('_'),
                        'signature': f"class {node.name}",
                        'lineno': node.lineno
                    })
            return symbols
        except:
             pass # Fallback to regex if parsing fails (e.g. syntax error in PR)

    # Regex Parsing (Fallback & Other Langs)
    # Functions
    for match in re.finditer(r'^(export\s+)?(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)(?:\s*:\s*([^{;]+))?', content, re.MULTILINE):
        symbols.append({
            'type': 'function',
            'name': match.group(2),
            'params': match.group(3).strip() if match.group(3) else '',
            'returns': match.group(4).strip() if match.group(4) else 'void',
            'exported': bool(match.group(1)),
            'signature': match.group(0).strip()
        })
    
    # Classes
    for match in re.finditer(r'^(export\s+)?class\s+(\w+)', content, re.MULTILINE):
        symbols.append({
            'type': 'class',
            'name': match.group(2),
            'exported': bool(match.group(1)),
            'signature': match.group(0).strip()
        })
    
    return symbols

def detect_breaking_changes(old_content, new_content, file_path):
    """Detect breaking changes between versions"""
    if not old_content:
        return {'has_breaking': False, 'changes': []}
    
    old_symbols = {s['name']: s for s in extract_symbols_detailed(old_content, file_path)}
    new_symbols = {s['name']: s for s in extract_symbols_detailed(new_content, file_path)}
    
    breaking_changes = []
    
    # Removed exports
    for name, sym in old_symbols.items():
        if sym['exported'] and name not in new_symbols:
            breaking_changes.append({
                'type': 'removed',
                'symbol': name,
                'severity': 'BREAKING',
                'message': f"Removed exported {sym['type']}: {name}"
            })
    
    # Modified signatures
    for name in set(old_symbols.keys()) & set(new_symbols.keys()):
        old_sym = old_symbols[name]
        new_sym = new_symbols[name]
        
        if old_sym['exported'] and old_sym['signature'] != new_sym['signature']:
             # Simple heuristic: if signature string changed, potentially breaking
             # In a real AST world, we'd compare args more deeply
             breaking_changes.append({
                'type': 'signature_change',
                'symbol': name,
                'severity': 'BREAKING',
                'message': f"Modified signature of {name}",
                'old': old_sym['signature'],
                'new': new_sym['signature']
            })
    
    return {
        'has_breaking': len(breaking_changes) > 0,
        'changes': breaking_changes
    }

def get_git_diff(file_path):
    """Get git diff for a file"""
    import subprocess
    try:
        result = subprocess.run(
            ['git', 'diff', 'HEAD~1', 'HEAD', file_path],
            capture_output=True,
            text=True
        )
        return result.stdout
    except:
        return None

def generate_documentation(file_context, file_path):
    """Generate documentation using Groq API"""
    if not GROQ_API_KEY:
        print("ERROR: GROQ_API_KEY not set")
        return "Documentation generation failed: No API key"
    
    prompt = f"""Generate comprehensive API documentation for this code file.

{file_context}

Include:
1. Overview - What this module does
2. Exports - All exported functions, classes, interfaces
3. Usage Examples - Practical examples for each export
4. Parameters - Describe each parameter
5. Return Values - What each function returns

Be thorough but concise. Format as GitHub-flavored Markdown."""

    try:
        response = requests.post(
            GROQ_API_URL,
            headers={
                'Authorization': f'Bearer {GROQ_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': MODEL,
                'messages': [
                    {'role': 'system', 'content': 'You are a technical documentation expert.'},
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.3,
                'max_tokens': 2000
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Error generating docs: {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

def generate_changelog_entry(file_path, old_content, new_content, breaking_info):
    """Generate changelog entry for this change"""
    old_symbols = {s['name']: s for s in extract_symbols_detailed(old_content, file_path)} if old_content else {}
    new_symbols = {s['name']: s for s in extract_symbols_detailed(new_content, file_path)}
    
    added = [name for name in new_symbols if name not in old_symbols and new_symbols[name]['exported']]
    removed = [name for name in old_symbols if name not in new_symbols and old_symbols[name]['exported']]
    modified = []
    
    for name in set(old_symbols.keys()) & set(new_symbols.keys()):
        if old_symbols[name]['signature'] != new_symbols[name]['signature']:
            modified.append(name)
    
    entry = []
    
    if breaking_info['has_breaking']:
        entry.append(f"### ⚠️ BREAKING CHANGES")
        for change in breaking_info['changes']:
            entry.append(f"- {change['message']}")
    
    if added:
        entry.append(f"### ✨ Added")
        for name in added:
            entry.append(f"- `{name}` ({new_symbols[name]['type']})")
    
    if modified and not breaking_info['has_breaking']:
        entry.append(f"### 🔄 Changed")
        for name in modified:
            entry.append(f"- `{name}` signature updated")
    
    if removed:
        entry.append(f"### 🗑️ Removed")
        for name in removed:
            entry.append(f"- `{name}` ({old_symbols[name]['type']})")
    
    return '\n'.join(entry) if entry else None

def update_changelog(entries):
    """Update or create CHANGELOG.md"""
    changelog_path = Path('CHANGELOG.md')
    
    # Read existing changelog
    if changelog_path.exists():
        with open(changelog_path, 'r') as f:
            existing = f.read()
    else:
        existing = "# Changelog\n\nAll notable changes to this project will be documented in this file.\n\n"
    
    # Create new entry
    today = datetime.now().strftime('%Y-%m-%d')
    new_entry = f"## [{today}]\n\n"
    
    for entry in entries:
        new_entry += f"### {entry['file']}\n\n"
        new_entry += entry['content'] + "\n\n"
    
    # Insert after header
    lines = existing.split('\n')
    header_end = 0
    for i, line in enumerate(lines):
        if line.startswith('## '):
            header_end = i
            break
    
    if header_end == 0:
        # No existing entries
        updated = existing + "\n" + new_entry
    else:
        # Insert before first entry
        updated = '\n'.join(lines[:header_end]) + '\n' + new_entry + '\n'.join(lines[header_end:])
    
    with open(changelog_path, 'w') as f:
        f.write(updated)
    
    print(f"  ✓ CHANGELOG.md updated with {len(entries)} entries")

def generate_smart_pr_comment(code_files, doc_files, breaking_changes, impacts, changelog_entries):
    """Generate comprehensive PR comment"""
    
    comment = "## 🤖 Auto-Generated Documentation & Analysis\n\n"
    
    # Breaking changes warning
    if breaking_changes:
        comment += "### ⚠️ BREAKING CHANGES DETECTED\n\n"
        comment += "This PR contains breaking changes that may affect users:\n\n"
        for change in breaking_changes:
            comment += f"- **{change['symbol']}**: {change['message']}\n"
            if 'old' in change and 'new' in change:
                comment += f"  ```diff\n  - {change['old']}\n  + {change['new']}\n  ```\n"
        comment += "\n"
    
    # Changed files summary
    comment += f"### 📝 Files Changed ({len(code_files)})\n\n"
    for file in code_files:
        comment += f"- `{Path(file).name}`\n"
    comment += "\n"
    
    # Changelog preview
    if changelog_entries:
        comment += "### 📋 Changelog Entries\n\n"
        for entry in changelog_entries:
            comment += f"**{entry['file']}**\n\n"
            comment += entry['content'] + "\n\n"
    
    # Impact analysis (Placeholder for now as logic wasn't fully refactored)
    if impacts:
        comment += "### 🔗 Cross-File Impact Analysis\n\n"
        comment += "*(Impact analysis logic pending update)*\n\n"
    
    # Documentation links
    comment += "### 📚 Documentation Generated\n\n"
    for doc_file in doc_files:
        comment += f"- [`{Path(doc_file).name}`]({doc_file})\n"
    comment += "\n"
    
    # Actions required
    comment += "### ✅ Recommended Actions\n\n"
    if breaking_changes:
        comment += "- [ ] Update major version number\n"
        comment += "- [ ] Create migration guide\n"
        comment += "- [ ] Notify users of breaking changes\n"
    else:
        comment += "- [ ] Review generated documentation\n"
        comment += "- [ ] Update CHANGELOG.md if needed\n"
    
    comment += "\n---\n\n"
    comment += "*Documentation automatically generated. Ask questions about these changes below!*\n"
    
    return comment

def main():
    print("Advanced Auto Documentation Generator")
    print("="*80)
    
    # Read changed files
    if not os.path.exists('changed_files.txt'):
        print("No changed files detected")
        sys.exit(0)
    
    with open('changed_files.txt', 'r') as f:
        changed_files = [line.strip() for line in f if line.strip()]
    
    # Filter supported files
    supported_exts = set()
    for conf in LANGUAGE_CONFIG.values():
        supported_exts.update(conf['extensions'])
        
    # Legacy fallback if config empty
    if not supported_exts:
        supported_exts = {'.ts', '.js', '.tsx', '.jsx', '.py', '.go', '.rs', '.java', '.cpp', '.cc', '.c', '.h', '.hpp'}

    code_files = [f for f in changed_files if Path(f).suffix in supported_exts]
    
    if not code_files:
        print("No code files changed")
        sys.exit(0)
    
    print(f"Processing {len(code_files)} changed files\n")
    
    # Cache Check
    CACHE_FILE = Path('.github/doc_cache.json')
    doc_cache = {}
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, 'r') as f: doc_cache = json.load(f)
        except: pass

    # Read files and get diffs
    files_data = {}
    file_diffs = {}
    old_contents = {}
    
    for file_path in code_files:
        if not os.path.exists(file_path): continue
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check Hash
            curr_hash = get_file_hash(content)
            if doc_cache.get(file_path) == curr_hash:
                print(f"  SKIP: {file_path} (Unchanged content)")
                continue

            doc_cache[file_path] = curr_hash
            files_data[file_path] = content
            file_diffs[file_path] = get_git_diff(file_path)
            
            # Get old version
            import subprocess
            try:
                old = subprocess.run(['git', 'show', f'HEAD~1:{file_path}'], capture_output=True, text=True)
                old_contents[file_path] = old.stdout if old.returncode == 0 else ""
            except:
                old_contents[file_path] = ""
            
            print(f"  OK: {file_path}")
        except Exception as e:
            print(f"  ERROR: {file_path} - {e}")
    
    if not files_data:
        print("\nNo new content to process")
        # Save cache anyway
        with open(CACHE_FILE, 'w') as f: json.dump(doc_cache, f)
        sys.exit(0)

    # Process Docs
    docs_dir = Path('docs')
    docs_dir.mkdir(exist_ok=True)
    
    doc_files_created = []
    changelog_entries = []
    all_breaking_changes = []
    
    for file_path, content in files_data.items():
        print(f"\n📝 {Path(file_path).name}...")
        
        old_content = old_contents.get(file_path, '')
        breaking_info = detect_breaking_changes(old_content, content, file_path)
        
        if breaking_info['has_breaking']:
            all_breaking_changes.extend(breaking_info['changes'])

        # Create Context
        diff_context = f"## {Path(file_path).name}\n\n"
        if old_content:
            diff_context += "### What Changed\n"
            diff = file_diffs.get(file_path, '')
            if diff: diff_context += f"```diff\n{diff[:1500]}\n```\n\n" # Increased limit slightly
        
        diff_context += f"```typescript\n{content}\n```\n\n"
        
        # Generate
        doc_content = generate_documentation(diff_context, file_path)
        
        # Save
        doc_filename = Path(file_path).stem + '.md'
        doc_path = docs_dir / doc_filename
        
        with open(doc_path, 'w') as f:
             f.write(f"# {Path(file_path).name}\n\n")
             f.write(f"*Auto-generated from `{file_path}`*\n\n")
             if breaking_info['has_breaking']:
                 f.write("## ⚠️ Breaking Changes\n\n")
                 for change in breaking_info['changes']:
                     f.write(f"- **{change['type'].upper()}**: {change['message']}\n")
             f.write(doc_content)
             
        doc_files_created.append(str(doc_path))
        print(f"   ✓ Created {doc_path}")

         # Generate changelog entry
        changelog = generate_changelog_entry(file_path, old_content, content, breaking_info)
        if changelog:
            changelog_entries.append({
                'file': Path(file_path).name,
                'content': changelog
            })

    # Update Changelog
    update_changelog(changelog_entries)

    # Generate PR Comment
    comment = generate_smart_pr_comment(
        code_files,
        doc_files_created,
        all_breaking_changes,
        [], # Impacts skipped for now
        changelog_entries
    )

    with open('doc_output.md', 'w') as f:
        f.write(comment)

    # Save Cache
    with open(CACHE_FILE, 'w') as f: json.dump(doc_cache, f)
    
    print("\n" + "="*80)
    print("COMPLETE")
    print("="*80)
    print(f"  ✓ {len(doc_files_created)} documentation files generated")

if __name__ == '__main__':
    main()
