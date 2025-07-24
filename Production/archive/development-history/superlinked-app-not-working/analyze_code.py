#!/usr/bin/env python3
"""
Enhanced Static Analysis for Legal Knowledge Platform

Performs deeper static analysis including:
- Import cycle detection
- Unused imports
- Duplicate definitions
- Code complexity metrics
"""

import ast
import os
from collections import defaultdict
from typing import Dict, List, Set, Tuple

class CodeAnalyzer(ast.NodeVisitor):
    """AST visitor for code analysis"""
    
    def __init__(self, filename: str):
        self.filename = filename
        self.imports = []
        self.from_imports = []
        self.functions = []
        self.classes = []
        self.globals = []
        self.used_names = set()
        
    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append({
                'module': alias.name,
                'alias': alias.asname,
                'line': node.lineno
            })
        self.generic_visit(node)
        
    def visit_ImportFrom(self, node):
        self.from_imports.append({
            'module': node.module,
            'names': [(n.name, n.asname) for n in node.names],
            'level': node.level,
            'line': node.lineno
        })
        self.generic_visit(node)
        
    def visit_FunctionDef(self, node):
        self.functions.append({
            'name': node.name,
            'line': node.lineno,
            'args': len(node.args.args),
            'decorators': len(node.decorator_list),
            'lines': node.end_lineno - node.lineno + 1 if hasattr(node, 'end_lineno') else 0
        })
        self.generic_visit(node)
        
    def visit_ClassDef(self, node):
        self.classes.append({
            'name': node.name,
            'line': node.lineno,
            'bases': len(node.bases),
            'decorators': len(node.decorator_list)
        })
        self.generic_visit(node)
        
    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.used_names.add(node.id)
        elif isinstance(node.ctx, ast.Store) and isinstance(node.ctx, ast.Store):
            self.globals.append(node.id)
        self.generic_visit(node)

def analyze_imports(files: List[str]) -> Dict[str, List[str]]:
    """Build import dependency graph"""
    import_graph = defaultdict(set)
    
    for file in files:
        try:
            with open(file, 'r') as f:
                tree = ast.parse(f.read())
                
            analyzer = CodeAnalyzer(file)
            analyzer.visit(tree)
            
            # Build import relationships
            for imp in analyzer.from_imports:
                if imp['module'] and imp['module'].startswith('.'):
                    # Relative import
                    from_dir = os.path.dirname(file)
                    level = imp['level']
                    
                    # Navigate up directories based on level
                    for _ in range(level - 1):
                        from_dir = os.path.dirname(from_dir)
                        
                    if imp['module']:
                        module_path = imp['module'].replace('.', '/')
                        target = os.path.join(from_dir, module_path)
                    else:
                        target = from_dir
                        
                    import_graph[file].add(target)
                    
        except Exception as e:
            print(f"Error analyzing {file}: {e}")
            
    return import_graph

def find_cycles(graph: Dict[str, Set[str]]) -> List[List[str]]:
    """Find import cycles using DFS"""
    cycles = []
    visited = set()
    rec_stack = set()
    
    def dfs(node: str, path: List[str]) -> None:
        visited.add(node)
        rec_stack.add(node)
        path.append(node)
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor, path[:])
            elif neighbor in rec_stack:
                # Found a cycle
                cycle_start = path.index(neighbor)
                cycle = path[cycle_start:] + [neighbor]
                if len(cycle) > 2:  # Ignore self-loops
                    cycles.append(cycle)
                    
        rec_stack.remove(node)
        
    for node in graph:
        if node not in visited:
            dfs(node, [])
            
    return cycles

def check_duplicate_definitions(files: List[str]) -> Dict[str, List[str]]:
    """Check for duplicate function/class definitions across files"""
    definitions = defaultdict(list)
    
    for file in files:
        try:
            with open(file, 'r') as f:
                tree = ast.parse(f.read())
                
            analyzer = CodeAnalyzer(file)
            analyzer.visit(tree)
            
            for func in analyzer.functions:
                definitions[func['name']].append(file)
                
            for cls in analyzer.classes:
                definitions[cls['name']].append(file)
                
        except Exception:
            pass
            
    # Find duplicates
    duplicates = {
        name: files 
        for name, files in definitions.items() 
        if len(files) > 1 and not name.startswith('_')
    }
    
    return duplicates

def analyze_complexity(file: str) -> Dict[str, any]:
    """Analyze code complexity metrics"""
    try:
        with open(file, 'r') as f:
            content = f.read()
            tree = ast.parse(content)
            
        analyzer = CodeAnalyzer(file)
        analyzer.visit(tree)
        
        # Calculate metrics
        lines = content.count('\n') + 1
        imports_count = len(analyzer.imports) + len(analyzer.from_imports)
        
        # Cyclomatic complexity (simplified)
        complexity = 1  # Base complexity
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
                
        return {
            'lines': lines,
            'imports': imports_count,
            'functions': len(analyzer.functions),
            'classes': len(analyzer.classes),
            'complexity': complexity,
            'avg_function_length': sum(f['lines'] for f in analyzer.functions) / len(analyzer.functions) if analyzer.functions else 0
        }
        
    except Exception as e:
        return {'error': str(e)}

def main():
    """Run enhanced static analysis"""
    print("Legal Knowledge Platform - Enhanced Static Analysis")
    print("=" * 60)
    
    # Find all Python files
    python_files = []
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    # Check for import cycles
    print("\n1. Checking for import cycles...")
    import_graph = analyze_imports(python_files)
    cycles = find_cycles(import_graph)
    
    if cycles:
        print(f"   ⚠️  Found {len(cycles)} import cycles:")
        for cycle in cycles:
            print(f"      {' -> '.join(cycle)}")
    else:
        print("   ✅ No import cycles found")
    
    # Check for duplicate definitions
    print("\n2. Checking for duplicate definitions...")
    duplicates = check_duplicate_definitions(python_files)
    
    if duplicates:
        print(f"   ⚠️  Found {len(duplicates)} duplicate definitions:")
        for name, files in duplicates.items():
            print(f"      '{name}' defined in:")
            for file in files:
                print(f"         - {file}")
    else:
        print("   ✅ No duplicate definitions found")
    
    # Analyze complexity
    print("\n3. Code complexity analysis...")
    high_complexity_files = []
    total_metrics = defaultdict(int)
    
    for file in python_files:
        metrics = analyze_complexity(file)
        if 'error' not in metrics:
            total_metrics['lines'] += metrics['lines']
            total_metrics['functions'] += metrics['functions']
            total_metrics['classes'] += metrics['classes']
            
            if metrics['complexity'] > 10:
                high_complexity_files.append((file, metrics))
    
    print(f"   Total lines of code: {total_metrics['lines']:,}")
    print(f"   Total functions: {total_metrics['functions']}")
    print(f"   Total classes: {total_metrics['classes']}")
    
    if high_complexity_files:
        print(f"\n   ⚠️  Files with high complexity (>10):")
        for file, metrics in sorted(high_complexity_files, key=lambda x: x[1]['complexity'], reverse=True)[:5]:
            print(f"      {file}: complexity={metrics['complexity']}")
    
    # Check specific patterns
    print("\n4. Checking code patterns...")
    issues = []
    
    for file in python_files:
        if file.endswith('spaces.py'):
            try:
                with open(file, 'r') as f:
                    content = f.read()
                    
                # Check for hardcoded model names
                if 'sentence-transformers/' in content and 'config' not in content:
                    issues.append(f"{file}: Hardcoded model name (should use config)")
                    
                # Check for missing error handling
                if 'try:' not in content and 'Space' in content:
                    issues.append(f"{file}: Space creation without error handling")
                    
            except Exception:
                pass
    
    if issues:
        print("   ⚠️  Found potential issues:")
        for issue in issues:
            print(f"      - {issue}")
    else:
        print("   ✅ No pattern issues found")
    
    print("\n" + "=" * 60)
    print("Analysis complete!")

if __name__ == "__main__":
    main()