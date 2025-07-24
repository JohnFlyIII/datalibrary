#!/usr/bin/env python3
"""
Static Analysis Script for Legal Knowledge Platform

Performs syntax checking and basic static analysis on all Python files.
"""

import ast
import os
import sys
from pathlib import Path
from typing import List, Tuple, Dict

def check_python_syntax(file_path: str) -> Tuple[bool, str]:
    """Check if a Python file has valid syntax"""
    try:
        with open(file_path, 'r') as f:
            source = f.read()
        ast.parse(source)
        return True, "OK"
    except SyntaxError as e:
        return False, f"SyntaxError at line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def check_imports(file_path: str) -> List[str]:
    """Extract and validate imports"""
    issues = []
    try:
        with open(file_path, 'r') as f:
            source = f.read()
        tree = ast.parse(source)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module and '..' in node.module:
                    # Relative imports
                    level = node.level
                    if level > 3:
                        issues.append(f"Deep relative import: {'.'*level}{node.module}")
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.startswith('_'):
                        issues.append(f"Importing private module: {alias.name}")
                        
    except Exception as e:
        issues.append(f"Failed to analyze imports: {str(e)}")
    
    return issues

def find_undefined_names(file_path: str) -> List[str]:
    """Find potentially undefined names"""
    undefined = []
    try:
        with open(file_path, 'r') as f:
            source = f.read()
        tree = ast.parse(source)
        
        # This is a simplified check - a full implementation would need scope analysis
        defined_names = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                defined_names.add(node.name)
            elif isinstance(node, ast.ClassDef):
                defined_names.add(node.name)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        defined_names.add(target.id)
                        
    except Exception:
        pass
    
    return undefined

def analyze_file(file_path: str) -> Dict[str, any]:
    """Perform static analysis on a single file"""
    relative_path = os.path.relpath(file_path)
    
    # Check syntax
    syntax_valid, syntax_msg = check_python_syntax(file_path)
    
    # Check imports
    import_issues = check_imports(file_path) if syntax_valid else []
    
    # Count lines
    try:
        with open(file_path, 'r') as f:
            lines = len(f.readlines())
    except:
        lines = 0
    
    return {
        'file': relative_path,
        'syntax_valid': syntax_valid,
        'syntax_msg': syntax_msg,
        'import_issues': import_issues,
        'lines': lines
    }

def main():
    """Run static analysis on all Python files"""
    print("Legal Knowledge Platform - Static Analysis")
    print("=" * 60)
    
    # Find all Python files
    python_files = []
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and __pycache__
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    print(f"Found {len(python_files)} Python files")
    print()
    
    # Analyze each file
    syntax_errors = []
    import_issues_total = []
    total_lines = 0
    
    for file_path in sorted(python_files):
        result = analyze_file(file_path)
        total_lines += result['lines']
        
        if not result['syntax_valid']:
            syntax_errors.append(result)
            print(f"❌ {result['file']}: {result['syntax_msg']}")
        elif result['import_issues']:
            import_issues_total.append(result)
            print(f"⚠️  {result['file']}: {len(result['import_issues'])} import issues")
        else:
            print(f"✅ {result['file']}: OK ({result['lines']} lines)")
    
    # Summary
    print()
    print("=" * 60)
    print("Summary:")
    print(f"Total files: {len(python_files)}")
    print(f"Total lines: {total_lines:,}")
    print(f"Syntax errors: {len(syntax_errors)}")
    print(f"Files with import issues: {len(import_issues_total)}")
    
    if syntax_errors:
        print("\nSyntax Errors:")
        for error in syntax_errors:
            print(f"  - {error['file']}: {error['syntax_msg']}")
    
    if import_issues_total:
        print("\nImport Issues:")
        for file_result in import_issues_total:
            print(f"  - {file_result['file']}:")
            for issue in file_result['import_issues']:
                print(f"    * {issue}")
    
    # Exit with error code if issues found
    if syntax_errors:
        sys.exit(1)
    else:
        print("\n✅ All files have valid syntax!")
        sys.exit(0)

if __name__ == "__main__":
    main()