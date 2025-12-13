#!/usr/bin/env python3
"""
Advanced Code Analyzer
Includes: Quality scoring, Security scanning, Performance regression detection
"""
"""

# Trigger CI
import os
import os
import re
import sys
import json
import ast
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime

# Globals to be loaded from config
LANGUAGE_CONFIG = {}
SECURITY_PATTERNS = {}
PERFORMANCE_PATTERNS = {}

def load_config():
    """Load configuration from JSON file"""
    global LANGUAGE_CONFIG, SECURITY_PATTERNS, PERFORMANCE_PATTERNS
    
    config_path = Path(__file__).parent.parent / 'config' / 'languages.json'
    
    if not config_path.exists():
        print(f"Error: Config file not found at {config_path}")
        sys.exit(1)
        
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            LANGUAGE_CONFIG = config.get('languages', {})
            SECURITY_PATTERNS = config.get('security_patterns', {})
            PERFORMANCE_PATTERNS = config.get('performance_patterns', {})
    except Exception as e:
        print(f"Error loading config: {e}")
        sys.exit(1)

class ASTAnalyzer(ast.NodeVisitor):
    """AST-based analyzer for Python"""
    def __init__(self, content: str):
        self.stats = {
            'functions': [],
            'classes': [],
            'complexity': 0,
            'docstrings': 0,
            'imports': [],
            'decision_points': 0
        }
        self.tree = ast.parse(content)
        self.content = content
        self.lines = content.split('\n')
        
    def visit_FunctionDef(self, node):
        self.stats['functions'].append({
            'name': node.name,
            'lineno': node.lineno,
            'end_lineno': node.end_lineno,
            'docstring': ast.get_docstring(node) is not None
        })
        if ast.get_docstring(node):
            self.stats['docstrings'] += 1
        self.generic_visit(node)
        
    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)
        
    def visit_ClassDef(self, node):
        self.stats['classes'].append({
            'name': node.name,
            'lineno': node.lineno,
            'docstring': ast.get_docstring(node) is not None
        })
        if ast.get_docstring(node):
            self.stats['docstrings'] += 1
        self.generic_visit(node)
        
    def visit_If(self, node):
        self.stats['decision_points'] += 1
        self.generic_visit(node)
        
    def visit_For(self, node):
        self.stats['decision_points'] += 1
        self.generic_visit(node)
        
    def visit_While(self, node):
        self.stats['decision_points'] += 1
        self.generic_visit(node)
        
    def visit_Try(self, node):
        self.stats['decision_points'] += 1
        self.generic_visit(node)
        
    def visit_ExceptHandler(self, node):
        self.stats['decision_points'] += 1
        self.generic_visit(node)
            
    def analyze(self):
        self.visit(self.tree)
        return self.stats

class CodeAnalyzer:
    def __init__(self, file_path: str, content: str):
        self.file_path = file_path
        self.content = content
        self.language_key = self._detect_language()
        self.config = LANGUAGE_CONFIG.get(self.language_key, {})
        self.lines = content.split('\n')
        self.ast_stats = None
        
        # Run AST analysis if Python
        if self.language_key == 'python':
            try:
                self.ast_stats = ASTAnalyzer(content).analyze()
            except Exception as e:
                print(f"AST Parse Error for {file_path}: {e}")
        
    def _detect_language(self) -> str:
        """Detect programming language from file extension"""
        ext = Path(self.file_path).suffix.lower()
        for lang, conf in LANGUAGE_CONFIG.items():
            if ext in conf.get('extensions', []):
                return lang
        return 'unknown'
    
    def calculate_quality_score(self) -> Dict:
        """Calculate comprehensive quality score"""
        scores = {
            'total': 0,
            'documentation': 0,
            'complexity': 0,
            'maintainability': 0,
            'breakdown': {}
        }
        
        # Documentation score
        doc_score = self._calculate_documentation_score()
        scores['documentation'] = doc_score
        scores['breakdown']['documentation'] = {
            'score': doc_score,
            'max': 30,
            'details': self._get_documentation_details()
        }
        
        # Complexity score
        complexity_score = self._calculate_complexity_score()
        scores['complexity'] = complexity_score
        scores['breakdown']['complexity'] = {
            'score': complexity_score,
            'max': 30,
            'details': self._get_complexity_details()
        }
        
        # Maintainability score
        maint_score = self._calculate_maintainability_score()
        scores['maintainability'] = maint_score
        scores['breakdown']['maintainability'] = {
            'score': maint_score,
            'max': 40,
            'details': self._get_maintainability_details()
        }
        
        scores['total'] = doc_score + complexity_score + maint_score
        scores['grade'] = self._get_grade(scores['total'])
        
        return scores
    
    def _calculate_documentation_score(self) -> int:
        """Score based on documentation coverage"""
        if self.ast_stats:
            # Python AST based scoring
            total_items = len(self.ast_stats['functions']) + len(self.ast_stats['classes'])
            if total_items == 0:
                return 30 # No items to document
            doc_items = self.ast_stats['docstrings']
            coverage = (doc_items / total_items) * 100
        else:
            # Regex/Line based approximation
            total_lines = len(self.lines)
            if total_lines == 0: return 0
            
            comment_single = self.config.get('comment_single', ['//', '#'])
            if isinstance(comment_single, str): comment_single = [comment_single]
            
            comment_lines = 0
            for line in self.lines:
                sline = line.strip()
                for marker in comment_single:
                    if sline.startswith(marker):
                        comment_lines += 1
                        break
                        
            coverage = (comment_lines / total_lines) * 100 if total_lines > 0 else 0
            # Boost score slightly for non-AST languages as finding actual defs is harder
            coverage = coverage * 1.5 
        
        if coverage >= 80: return 30
        if coverage >= 60: return 25
        if coverage >= 40: return 20
        if coverage >= 20: return 15
        return int(coverage / 2)
    
    def _calculate_complexity_score(self) -> int:
        """Score based on complexity"""
        decision_points = 0
        
        if self.ast_stats:
            decision_points = self.ast_stats['decision_points']
        else:
            keywords = self.config.get('complexity_keywords', [])
            decision_points = sum(
                sum(1 for _ in re.finditer(rf'\b{kw}\b', self.content)) 
                for kw in keywords
            )
        
        lines = len(self.lines)
        if lines == 0: return 30
        
        complexity_per_line = decision_points / lines
        
        if complexity_per_line <= 0.05: return 30
        if complexity_per_line <= 0.10: return 25
        if complexity_per_line <= 0.15: return 20
        if complexity_per_line <= 0.20: return 15
        return 10
    
    def _calculate_maintainability_score(self) -> int:
        """Score based on maintainability factors"""
        score = 40
        
        # Line length
        long_lines = sum(1 for line in self.lines if len(line) > 120)
        if long_lines > len(self.lines) * 0.2: score -= 10
        elif long_lines > len(self.lines) * 0.1: score -= 5
        
        # Function length
        avg_len = self._get_average_function_length()
        if avg_len > 50: score -= 10
        elif avg_len > 30: score -= 5
        
        return max(0, score)
    
    def _get_average_function_length(self) -> float:
        if self.ast_stats:
            funcs = self.ast_stats['functions']
            if not funcs: return 0
            total_len = sum(f['end_lineno'] - f['lineno'] for f in funcs)
            return total_len / len(funcs)
        
        pattern = self.config.get('function_pattern')
        if not pattern: return 0
        
        try:
            matches = [m.start() for m in re.finditer(pattern, self.content)]
            if not matches: return 0
            
            # Rough estimation
            return len(self.lines) / len(matches) / 2 # Assume funcs take up half the file
        except:
            return 0

    def _get_documentation_details(self) -> str:
        if self.ast_stats:
             total = len(self.ast_stats['functions']) + len(self.ast_stats['classes'])
             documented = self.ast_stats['docstrings']
             return f"{documented}/{total} items documented"
        return "Based on comment density"

    def _get_complexity_details(self) -> str:
        if self.ast_stats:
            return f"{self.ast_stats['decision_points']} decision points (AST)"
        return "Based on keyword count"

    def _get_maintainability_details(self) -> str:
        long_lines = sum(1 for line in self.lines if len(line) > 120)
        return f"{long_lines} long lines detected"

    def _get_grade(self, score: int) -> str:
        if score >= 90: return 'A+'
        if score >= 85: return 'A'
        if score >= 80: return 'A-'
        if score >= 75: return 'B+'
        if score >= 70: return 'B'
        if score >= 65: return 'B-'
        if score >= 60: return 'C+'
        if score >= 55: return 'C'
        if score >= 50: return 'C-'
        return 'D'

    def scan_security_vulnerabilities(self) -> List[Dict]:
        """Scan for security vulnerabilities"""
        vulnerabilities = []
        
        for category, patterns in SECURITY_PATTERNS.items():
            for pattern_def in patterns:
                pattern, description = pattern_def
                try:
                    for match in re.finditer(pattern, self.content, re.IGNORECASE | re.MULTILINE):
                        line_num = self.content[:match.start()].count('\n') + 1
                        vulnerabilities.append({
                            'category': category,
                            'severity': 'HIGH' if category in ['sql_injection', 'command_injection'] else 'MEDIUM',
                            'description': description,
                            'line': line_num,
                            'code': self.lines[line_num - 1].strip() if line_num <= len(self.lines) else ''
                        })
                except re.error:
                    pass
                    
        return vulnerabilities

    def detect_performance_issues(self) -> List[Dict]:
        """Detect performance issues"""
        issues = []
        
        # Regex based patterns
        for key, pattern in PERFORMANCE_PATTERNS.items():
            try:
                for match in re.finditer(pattern, self.content, re.MULTILINE):
                    line_num = self.content[:match.start()].count('\n') + 1
                    issues.append({
                        'type': key,
                        'severity': 'MEDIUM',
                        'description': f"Potential {key} performance issue",
                        'line': line_num,
                        'suggestion': 'Review algorithmic complexity'
                    })
            except:
                pass
                
        # AST based large function detection
        if self.ast_stats:
            for func in self.ast_stats['functions']:
                length = func['end_lineno'] - func['lineno']
                if length > 100:
                     issues.append({
                        'type': 'large_function',
                        'severity': 'LOW',
                        'description': f'Large function "{func["name"]}" ({length} lines)',
                        'line': func['lineno'],
                        'suggestion': 'Break into smaller functions'
                    })
                    
        return issues

def analyze_file(file_path: str) -> Optional[Dict]:
    """Analyze a single file"""
    if not os.path.exists(file_path):
        return None
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None
    
    analyzer = CodeAnalyzer(file_path, content)
    
    return {
        'file': file_path,
        'language': analyzer.language_key,
        'quality_score': analyzer.calculate_quality_score(),
        'security_vulnerabilities': analyzer.scan_security_vulnerabilities(),
        'performance_issues': analyzer.detect_performance_issues()
    }

def main():
    load_config()
    print("="*80)
    print("ADVANCED CODE ANALYZER (AST ENHANCED)")
    print("="*80)
    
    # Get commit info
    commit_sha = os.environ.get('GITHUB_SHA', 'unknown')[:7]
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    
    analysis_dir = Path('code-analysis') / f"{timestamp}_{commit_sha}"
    analysis_dir.mkdir(parents=True, exist_ok=True)
    
    # Read changed files
    if not os.path.exists('changed_files.txt'):
        print("No changed files detected")
        sys.exit(0)
    
    with open('changed_files.txt', 'r') as f:
        changed_files = [line.strip() for line in f if line.strip()]
    
    results = []
    
    # Filter for supported extensions
    supported_exts = set()
    for conf in LANGUAGE_CONFIG.values():
        supported_exts.update(conf['extensions'])

    for file_path in changed_files:
        if Path(file_path).suffix in supported_exts:
            print(f"📊 Analyzing: {file_path}")
            result = analyze_file(file_path)
            if result:
                results.append(result)
                score = result['quality_score']
                print(f"   Quality: {score['total']}/100 ({score['grade']})")
                
                vulns = result['security_vulnerabilities']
                if vulns: print(f"   ⚠️  {len(vulns)} security issue(s)")
                
                perf = result['performance_issues']
                if perf: print(f"   🐌 {len(perf)} performance issue(s)")
                print()

    # Save results
    results_file = analysis_dir / 'results.json'
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
        
    print(f"Analysis complete. Results at {results_file}")

if __name__ == '__main__':
    main()
