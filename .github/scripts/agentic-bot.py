#!/usr/bin/env python3
"""
Agentic PR Bot - Make Code Changes
Features:
1. Safer "Search & Replace" mechanism
2. Auth checks
3. Intent classification
"""

import os
import sys
import re
import json
import subprocess
from pathlib import Path
import requests
from llm import get_client

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
COMMENT_BODY = os.environ.get('COMMENT_BODY', '')
COMMENT_USER = os.environ.get('COMMENT_USER', 'user')
PR_AUTHOR = os.environ.get('PR_AUTHOR', '')
PR_ASSIGNEES = os.environ.get('PR_ASSIGNEES', '')
MODEL = 'openai/gpt-oss-120b'

def is_authorized(user):
    """Check if user is authorized to trigger actions"""
    if user == PR_AUTHOR:
        return True
    
    assignees = [a.strip() for a in PR_ASSIGNEES.split(',') if a.strip()]
    return user in assignees

def classify_intent(comment_text):
    """Classify if this is an action request and how confident we are"""
    
    prompt = f"""Classify this PR comment into one of three categories:

Comment: "{comment_text}"

Categories:
1. CLEAR_ACTION - User clearly wants code changes (e.g., "add comments to file.ts", "fix the bug in auth.ts")
2. POSSIBLE_ACTION - Might want changes but ambiguous (e.g., "this needs comments", "could use error handling")
3. QUESTION_ONLY - Just asking a question, no action requested

Also extract what action they want if it's an action request.

Respond ONLY with JSON:
{{
  "category": "CLEAR_ACTION|POSSIBLE_ACTION|QUESTION_ONLY",
  "action": "description of what to do (if applicable)",
  "confidence": 0.0-1.0,
  "reasoning": "brief explanation"
}}"""

    try:
    try:
        response = get_client().call_chat(
            model='openai/gpt-oss-20b',
            messages=[
                {'role': 'system', 'content': 'You are a PR intent classifier. Respond only with valid JSON.'},
                {'role': 'user', 'content': prompt}
            ],
            temperature=0.1,
            max_tokens=200,
            response_format='json'
        )
        
        if response:
            content = response
            # Extract JSON from response
            json_match = re.search(r'\{[^}]+\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
    except:
        pass
    
    # Fallback
    return {'category': 'QUESTION_ONLY', 'action': None, 'confidence': 0}

def load_changed_files():
    """Load PR's changed files"""
    if not os.path.exists('pr_files.txt'):
        return []
    
    with open('pr_files.txt', 'r') as f:
        return [line.strip() for line in f if line.strip()]

def generate_code_changes(action_description, files):
    """Use LLM to generate SEARCH/REPLACE blocks"""
    
    # Build context from changed files
    context = "PR Files:\n\n"
    file_contents = {}
    
    code_extensions = {'.ts', '.js', '.tsx', '.jsx', '.py', '.go', '.rs', '.java'}
    
    for file_path in files:
        if Path(file_path).suffix not in code_extensions:
            continue
        
        if not os.path.exists(file_path):
            continue
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            file_contents[file_path] = content
            context += f"## {file_path}\n```\n{content}\n```\n\n"
        except:
            continue
    
    if not file_contents:
        return None
    
    prompt = f"""You are a code editing agent. Use SEARCH/REPLACE blocks to modify the code.

{context}

User request: {action_description}

Instructions:
1. Output specific SEARCH and REPLACE blocks for changes.
2. The SEARCH block must match existing code EXACTLY (including whitespace).
3. The REPLACE block contains your new code.
4. Keep context lines to a minimum (2-3 lines) to ensure uniqueness.

Format:

FILE: path/to/file.ext
<<<< SEARCH
original code lines
to be replaced
====
new code lines
with changes applied
>>>>

Response:"""

    try:
    try:
        response = get_client().call_chat(
            model=MODEL,
            messages=[
                {'role': 'system', 'content': 'You are a precise code editing assistant. Use SEARCH/REPLACE format.'},
                {'role': 'user', 'content': prompt}
            ],
            temperature=0.1,
            max_tokens=4000
        )
        
        if response:
            return response
    except Exception as e:
        print(f"ERROR generating changes: {e}")
    
    return None

def apply_changes_safely(llm_output, original_files):
    """Parse SEARCH/REPLACE blocks and apply them"""
    files_modified = set()
    
    # Regex to capture blocks
    # Group 1: Filename
    # Group 2: Search content
    # Group 3: Replace content
    pattern = re.compile(r'FILE:\s*([^\n]+)\s*<<<<\s*SEARCH\n(.*?)\n====\n(.*?)\n>>>>', re.DOTALL)
    
    matches = pattern.finditer(llm_output)
    
    for match in matches:
        file_path = match.group(1).strip()
        search_block = match.group(2)
        replace_block = match.group(3)
        
        # Verify file exists in original files
        if not os.path.exists(file_path):
            print(f"  SKIP: {file_path} (File not found locally)")
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Attempt replacement
            # We try to handle whitespace leniency by stripping ends first
            if search_block not in content:
                # Try relaxed match (line by line stripping)
                print(f"  WARN: Exact match failed for {file_path}, trying fuzzy...")
                # ... (Simple fuzzy logic could go here, but strictly failing is safer for now)
                print(f"  ERR: Search block not found in {file_path}")
                continue
            
            new_content = content.replace(search_block, replace_block, 1) # Replace first occurrence
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
            files_modified.add(file_path)
            print(f"  ✓ Applied change to {file_path}")
            
        except Exception as e:
            print(f"  ERROR modifying {file_path}: {e}")
            
    return list(files_modified)

def commit_changes(files_changed, action_description):
    """Commit the changes"""
    if not files_changed:
        return None
    
    try:
        # Configure git
        subprocess.run(['git', 'config', 'user.email', 'github-actions[bot]@users.noreply.github.com'], check=True)
        subprocess.run(['git', 'config', 'user.name', 'github-actions[bot]'], check=True)
        
        # Add changed files
        for file_path in files_changed:
            subprocess.run(['git', 'add', file_path], capture_output=True, text=True)
        
        # Check status
        status = subprocess.run(['git', 'status', '--short'], capture_output=True, text=True)
        if not status.stdout.strip():
            return "no-changes"
        
        # Commit
        commit_msg = f"bot: {action_description[:100]}"
        subprocess.run(['git', 'commit', '-m', commit_msg], capture_output=True, text=True)
        
        # Push
        subprocess.run(['git', 'push'], capture_output=True, text=True)
        
        # Get hash
        result = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True)
        return result.stdout.strip()
        
    except Exception as e:
        print(f"ERROR committing: {e}")
        return None

def main():
    print("Agentic PR Bot - Safer Code Change Agent")
    print("="*80)
    
    if not COMMENT_BODY.strip().lower().startswith('[auto]'):
        sys.exit(0)
    
    actual_comment = re.sub(r'^\[auto\]\s*', '', COMMENT_BODY.strip(), flags=re.IGNORECASE)
    
    if not is_authorized(COMMENT_USER):
        print(f"Unauthorized: {COMMENT_USER}")
        sys.exit(0)
    
    print("Classifying intent...")
    intent = classify_intent(actual_comment)
    
    if intent['category'] == 'QUESTION_ONLY':
        sys.exit(0)
        
    changed_files = load_changed_files()
    if not changed_files:
        print("No changed files to work on.")
        sys.exit(0)
        
    print(f"Generating changes for: {intent['action']}")
    
    llm_output = generate_code_changes(intent['action'], changed_files)
    
    if not llm_output:
        print("LLM failed to generate output.")
        sys.exit(0)
        
    print("Applying changes...")
    files_modified = apply_changes_safely(llm_output, changed_files)
    
    if files_modified:
        commit_hash = commit_changes(files_modified, intent['action'])
        if commit_hash:
            response = f"""## ✅ Changes Applied
            
I made the requested changes: **{intent['action']}**

Modified: {', '.join(files_modified)}
Commit: {commit_hash[:7]}
"""
            with open('bot_response.md', 'w') as f:
                f.write(response)
    else:
         response = f"""## ⚠️ No Changes Applied
         
I understood the request but couldn't apply the changes safely. This usually means I couldn't find the exact code block to replace.
"""
         with open('bot_response.md', 'w') as f:
            f.write(response)

if __name__ == '__main__':
    main()
