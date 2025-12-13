#!/usr/bin/env python3
"""
Unified CI/CD CLI Tool
Usage:
  python cicd-cli.py analyze <file>
  python cicd-cli.py gen-docs <file>
  python cicd-cli.py build-site
  python cicd-cli.py full-run
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path

SCRIPTS_DIR = Path('.github/scripts')

def run_script(script_name, args=[]):
    script_path = SCRIPTS_DIR / script_name
    if not script_path.exists():
        print(f"Error: {script_name} not found")
        return
    
    cmd = [sys.executable, str(script_path)] + args
    print(f"Running {script_name}...")
    subprocess.run(cmd)

def main():
    parser = argparse.ArgumentParser(description="CI/CD Toolkit")
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Analyze
    analyze_parser = subparsers.add_parser('analyze', help='Run code analysis')
    analyze_parser.add_argument('file', nargs='?', help='File to analyze')
    
    # Gen Docs
    docs_parser = subparsers.add_parser('gen-docs', help='Generate documentation')
    docs_parser.add_argument('file', nargs='?', help='File to document')
    
    # Build Site
    subparsers.add_parser('build-site', help='Build documentation site')
    
    # Full Run
    subparsers.add_parser('full-run', help='Run full pipeline (local simulation)')

    args = parser.parse_args()
    
    if args.command == 'analyze':
        # For local test we need to mock changed_files.txt if file provided
        if args.file:
            with open('changed_files.txt', 'w') as f: f.write(args.file)
        run_script('code-analyzer.py')
        
    elif args.command == 'gen-docs':
        if args.file:
            with open('changed_files.txt', 'w') as f: f.write(args.file)
        run_script('generate-docs.py')
        
    elif args.command == 'build-site':
        run_script('site_generator.py')
        
    elif args.command == 'full-run':
        print("🚀 Starting Full Pipeline Simulation")
        print("-" * 50)
        
        # 1. Analyze
        print("\n[Stage 1] Code Analysis")
        run_script('code-analyzer.py')
        
        # 2. Docs
        print("\n[Stage 2] Documentation")
        run_script('generate-docs.py')
        
        # 3. Site
        print("\n[Stage 3] Web Portal")
        run_script('site_generator.py')
        
        print("\n✅ Pipeline Complete")
        
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
