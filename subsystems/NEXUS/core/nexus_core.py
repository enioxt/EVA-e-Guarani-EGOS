#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
NEXUS (Neural Evolution and Xenial Unified System) Core Logic
=============================================================

Core implementation of the modular analysis system for EGOS.
Provides capabilities for code analysis, dependency mapping, and improvement suggestions.

Version: 1.0.0 (Migrated)
"""

import logging
from typing import Dict, List, Optional, Any, Tuple, Set
from datetime import datetime
import json
import os
from pathlib import Path
# import numpy as np  # Removed unused import
# import pandas as pd # Removed unused import
# from sklearn.feature_extraction.text import TfidfVectorizer # Removed unused import
# from sklearn.metrics.pairwise import cosine_similarity # Removed unused import
import ast

from .ast_visitor import analyze_code as ast_analyze_code

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NEXUSCore:
    """Core class for NEXUS analysis and cartography.
    
    Provides functionalities to analyze Python code files, map dependencies
    within a workspace, suggest improvements based on metrics, and export
    analysis results.
    """
    
    def __init__(self, config: Dict[str, Any], logger: logging.Logger, project_root: Path):
        """Initialize NEXUS core.

        Args:
            config (Dict[str, Any]): Configuration dictionary, potentially including
                                     thresholds for suggestions.
            logger (logging.Logger): Logger instance for logging messages.
            project_root (Path): The absolute path to the root of the project being analyzed.
        """
        self.config = config
        self.logger = logger
        self.project_root = project_root
        self.logger.info("NEXUS Core initialized.")
        
    def analyze_code(self, file_path: str) -> Optional[Dict]:
        """Analyze a single Python code file using AST.

        Extracts metrics like line count, complexity, imports, functions, and classes.

        Args:
            file_path (str): The absolute or relative path to the Python file.

        Returns:
            Optional[Dict]: A dictionary containing analysis metrics, or None if the
                            file is not found. Returns a dict with an 'error' key
                            if analysis fails.
        """
        self.logger.debug(f"Analyzing file: {file_path}")
        try:
            # Basic check if file exists
            if not Path(file_path).is_file():
                 self.logger.error(f"File not found for analysis: {file_path}")
                 return None
                 
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Use AST-based analysis
            ast_metrics = ast_analyze_code(content, self.logger)
            if 'error' in ast_metrics:
                self.logger.error(f"AST analysis error for {file_path}: {ast_metrics['error']}")
                return ast_metrics
                
            metrics = {
                'lines': len(content.splitlines()),
                'chars': len(content),
                'complexity': {
                    'cognitive_load': ast_metrics['cognitive_load']
                },
                'imports': [
                    f"{'from ' + imp['module'] + ' ' if imp['is_from_import'] else ''}"
                    f"import {', '.join(imp['names']) if imp['names'] else imp['module']}"
                    f"{' as ' + imp['alias'] if imp['alias'] else ''}"
                    for imp in ast_metrics['imports']
                ],
                'functions': [
                    {
                        'name': func['name'],
                        'params': func['args'],
                        'doc': func['docstring'] or 'No docstring',
                        'line': func['start_line'],
                        'end_line': func['end_line'],
                        'is_async': func['is_async'],
                        'decorators': func['decorators']
                    }
                    for func in ast_metrics['functions']
                ],
                'classes': [
                    {
                        'name': cls['name'],
                        'inheritance': ', '.join(cls['bases']),
                        'doc': cls['docstring'] or 'No docstring',
                        'line': cls['start_line'],
                        'end_line': cls['end_line'],
                        'decorators': cls['decorators'],
                        'methods': [
                            {
                                'name': method['name'],
                                'params': method['args'],
                                'doc': method['docstring'] or 'No docstring',
                                'line': method['start_line'],
                                'end_line': method['end_line'],
                                'is_async': method['is_async'],
                                'decorators': method['decorators']
                            }
                            for method in cls['methods']
                        ]
                    }
                    for cls in ast_metrics['classes']
                ]
            }
            
            self.logger.info(f"Analyzed file: {file_path} - {metrics['lines']} lines")
            return metrics
        except FileNotFoundError:
             self.logger.error(f"File not found during analysis: {file_path}")
             return None
        except Exception as e:
            self.logger.exception(f"Error analyzing file {file_path}: {e}")
            return {"error": f"Failed to analyze {file_path}: {e}"}
            
    def analyze_dependencies(self, python_files: List[str]) -> Dict:
        """Analyze dependencies between a list of Python files.

        Parses import statements using AST, resolves relative/absolute paths,
        and builds a map of which files import others.

        Args:
            python_files (List[str]): A list of absolute or relative paths to Python
                                      files within the project.

        Returns:
            Dict: A dictionary where keys are file paths. Each value is a dict with:
                  - 'imports' (List[str]): Formatted import statements found.
                  - 'imported_by' (List[str]): List of files importing this key file.
                  An 'error' key may be present if AST parsing failed for a file.
        """
        self.logger.info("Analyzing dependencies...")
        
        dependencies: Dict[str, Dict[str, List[str]]] = {}
        module_to_path: Dict[str, str] = {}
        all_import_details: Dict[str, List[Dict[str, Any]]] = {} # file_path -> list of import details
        
        # First pass: Initialize dictionary, map module names to paths, and parse AST for import details
        for file_path in python_files:
            dependencies[file_path] = {
                'imports': [],
                'imported_by': []
            }
            all_import_details[file_path] = []
            module_name = self._path_to_module_str(file_path)
            if module_name:
                module_to_path[module_name] = file_path

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                tree = ast.parse(content)
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            all_import_details[file_path].append({
                                'is_from_import': False,
                                'module': alias.name,
                                'names': [],
                                'alias': alias.asname,
                                'level': 0
                            })
                    elif isinstance(node, ast.ImportFrom):
                        imported_names = [alias.name for alias in node.names]
                        imported_aliases = {alias.name: alias.asname for alias in node.names if alias.asname}
                        all_import_details[file_path].append({
                            'is_from_import': True,
                            'module': node.module or '', # Can be None for relative imports like `from . import foo`
                            'names': imported_names,
                            'aliases': imported_aliases, # Store aliases separately if needed
                            'level': node.level
                        })
            except Exception as e:
                self.logger.error(f"Error analyzing dependencies AST in {file_path}: {str(e)}", exc_info=True)
                # Continue to next file, but mark this one as having potential issues?
                dependencies[file_path]['error'] = f"AST parsing error: {str(e)}" # Add an error key
                continue
        
        # Second pass: Format imports and build reverse dependencies
        for file_path, import_details_list in all_import_details.items():
            if 'error' in dependencies[file_path]: continue # Skip files with parsing errors
            
            formatted_imports: List[str] = []
            imported_module_sources: Set[str] = set() # Keep track of source modules for reverse deps
            current_file_module_name = self._path_to_module_str(file_path) 

            for imp in import_details_list:
                # Format the import string
                if imp['is_from_import']:
                    import_str = f"from {'.' * imp['level']}{imp['module'] if imp['module'] else ''} import {', '.join(imp['names'])}"
                    # TODO: Add alias handling if necessary for the string format
                else:
                    import_str = f"import {imp['module']}"
                    if imp['alias']:
                        import_str += f" as {imp['alias']}"
                formatted_imports.append(import_str)

                # Determine the source module for dependency tracking
                source_module = imp['module']
                resolved_source_module = source_module # Use a different variable for the resolved name
                is_relative = imp['is_from_import'] and imp['level'] > 0

                if is_relative and current_file_module_name:
                    # Resolve relative import path
                    base_parts = current_file_module_name.split('.')
                    if len(base_parts) >= imp['level']:
                        prefix = '.'.join(base_parts[:-imp['level']])
                        if source_module: 
                            resolved_source_module = f"{prefix}.{source_module}" if prefix else source_module
                        elif imp['names']: 
                            resolved_source_module = f"{prefix}.{imp['names'][0]}" if prefix else imp['names'][0]
                        else:
                            self.logger.warning(f"Cannot precisely resolve relative import 'from {'.' * imp['level']} import ...' in {file_path}")
                            resolved_source_module = None 
                    else:
                        self.logger.warning(f"Could not resolve relative import level {imp['level']} for module '{source_module}' in {file_path}")
                        resolved_source_module = None 
                
                # Handle potential 'src.' prefix from absolute imports
                if resolved_source_module and not is_relative and resolved_source_module.startswith('src.'):
                     resolved_source_module = resolved_source_module[4:] # Remove 'src.' prefix

                if resolved_source_module:
                    imported_module_sources.add(resolved_source_module)

            dependencies[file_path]['imports'] = sorted(formatted_imports)

            # Build reverse dependencies using the resolved source modules
            for imported_module_name in imported_module_sources:
                imported_file_path = module_to_path.get(imported_module_name)
                if imported_file_path and imported_file_path != file_path: 
                    if imported_file_path in dependencies:
                        if file_path not in dependencies[imported_file_path]['imported_by']:
                            dependencies[imported_file_path]['imported_by'].append(file_path)
        
        self.logger.info("Dependency analysis complete.")
        return dependencies
            
    def _path_to_module_str(self, file_path_str: str) -> Optional[str]:
        """Convert a file path string to a Python module string relative to project root.
        
        Removes the project root, `.py` extension, and handles `__init__.py`.
        Excludes 'src' directory from the module path.

        Args:
            file_path_str (str): The file path.

        Returns:
            Optional[str]: The dot-separated module string (e.g., 'subsystems.NEXUS.core')
                           or None if conversion fails.
        """
        try:
            p = Path(file_path_str)
            relative_to_root = p.relative_to(self.project_root)
            module_parts = []
            
            for part in relative_to_root.with_suffix('').parts:
                if part == 'src':
                    continue
                if part == '__init__':
                    continue
                module_parts.append(part)
                
            return '.'.join(module_parts)
        except Exception:
            return None
        
    def analyze_workspace(self) -> Dict:
        """Analyze the entire Python workspace defined by project_root.

        Collects all .py files (excluding .venv, __pycache__), analyzes each one,
        calculates aggregate metrics, and analyzes inter-file dependencies.

        Returns:
            Dict: A nested dictionary containing:
                  - 'metrics': Aggregated workspace metrics (file count, lines, etc.).
                  - 'files': Analysis dictionary for each file (from analyze_code).
                  - 'dependencies': Dependency map (from analyze_dependencies).
        """
        self.logger.info("Starting workspace analysis...")
        
        # Collect Python files
        python_files = []
        for root, _, files in os.walk(self.project_root):
            if '.venv' in root or '__pycache__' in root:
                continue
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
                    
        # Analyze each file
        analysis = {
            'metrics': {
                'total_files': len(python_files),
                'total_lines': 0,
                'total_functions': 0,
                'total_classes': 0,
                'avg_complexity': 0.0
            },
            'files': {},
            'dependencies': None
        }
        
        complexities = []
        
        for file_path in python_files:
            file_analysis = self.analyze_code(file_path)
            if file_analysis and 'error' not in file_analysis:
                analysis['files'][file_path] = file_analysis
                analysis['metrics']['total_lines'] += file_analysis['lines']
                analysis['metrics']['total_functions'] += len(file_analysis['functions'])
                analysis['metrics']['total_classes'] += len(file_analysis['classes'])
                complexities.append(file_analysis['complexity']['cognitive_load'])
                    
        if complexities:
            analysis['metrics']['avg_complexity'] = sum(complexities) / len(complexities)
            
        # Analyze dependencies
        analysis['dependencies'] = self.analyze_dependencies(python_files)
        
        self.logger.info("Workspace analysis complete.")
        return analysis
            
    def suggest_improvements(self, workspace_analysis: Dict) -> List[Dict]:
        """Generate improvement suggestions based on workspace analysis.

        Checks metrics like cognitive load, import count, dependency count,
        and docstring coverage against configurable thresholds.

        Args:
            workspace_analysis (Dict): The dictionary returned by analyze_workspace().

        Returns:
            List[Dict]: A list of suggestion dictionaries, each containing 'type',
                        'file', 'severity', and 'message'.
        """
        suggestions = []
        thresholds = self.config.get('analysis', {}).get('suggestions', {})
        
        for file_path, analysis in workspace_analysis.get('files', {}).items():
            # Check cognitive load
            cognitive_load = analysis.get('complexity', {}).get('cognitive_load', 0)
            if cognitive_load > thresholds.get('cognitive_load_threshold_high', 50):
                suggestions.append({
                    'type': 'complexity',
                    'file': file_path,
                    'severity': 'high',
                    'message': f'High cognitive load ({cognitive_load:.1f}). Consider breaking down into smaller functions.'
                })
                
            # Check import count
            import_count = len(analysis.get('imports', []))
            if import_count > thresholds.get('imports_threshold', 15):
                suggestions.append({
                    'type': 'imports',
                    'file': file_path,
                    'severity': 'medium',
                    'message': f'High number of imports ({import_count}). Consider modularizing or using composition.'
                })
                
            # Check dependency count
            if workspace_analysis.get('dependencies'):
                imported_by = workspace_analysis['dependencies'].get(file_path, {}).get('imported_by', [])
                if len(imported_by) > thresholds.get('imported_by_threshold', 10):
                    suggestions.append({
                        'type': 'dependencies',
                        'file': file_path,
                        'severity': 'medium',
                        'message': f'Module is imported by {len(imported_by)} files. Consider if it should be split into smaller, more focused modules.'
                    })
                    
            # Check docstring coverage
            for func in analysis.get('functions', []):
                if func.get('doc') in ['No docstring', None, '']:
                    suggestions.append({
                        'type': 'documentation',
                        'file': file_path,
                        'severity': 'low',
                        'message': f'Function {func["name"]} lacks a docstring.'
                    })
                    
            for cls in analysis.get('classes', []):
                if cls.get('doc') in ['No docstring', None, '']:
                    suggestions.append({
                        'type': 'documentation',
                        'file': file_path,
                        'severity': 'low',
                        'message': f'Class {cls["name"]} lacks a docstring.'
                    })
                for method in cls.get('methods', []):
                    if method.get('doc') in ['No docstring', None, '']:
                        suggestions.append({
                            'type': 'documentation',
                            'file': file_path,
                            'severity': 'low',
                            'message': f'Method {cls["name"]}.{method["name"]} lacks a docstring.'
                        })
                
        return suggestions

    def export_analysis(self, data: Dict, format: str = 'json') -> Optional[str]:
        """Export analysis results in the specified format (JSON or Markdown).

        Args:
            data (Dict): The analysis data dictionary (e.g., from analyze_workspace).
            format (str, optional): The desired output format ('json' or 'md'). 
                                     Defaults to 'json'.

        Returns:
            Optional[str]: A string containing the exported data in the specified format,
                           or None if an error occurs or format is unsupported.
        """
        self.logger.debug(f"Exporting analysis data in format: {format}")
        try:
            if format == 'json':
                return json.dumps(data, indent=2, default=str)
            elif format == 'md':
                return self._convert_to_markdown(data)
            else:
                self.logger.error(f"Unsupported export format requested: {format}")
                raise ValueError(f"Unsupported export format: {format}")
        except Exception as e:
            self.logger.exception(f"Error exporting analysis: {e}")
            return None
            
    def _convert_to_markdown(self, data: Dict) -> str:
        """Convert analysis data dictionary to a Markdown formatted string.
        
        Args:
            data (Dict): The analysis data dictionary.

        Returns:
            str: A Markdown formatted report string.
        """
        md = ["# NEXUS Analysis Report\n"]
        # self.logger.debug(f"Starting Markdown conversion. Data keys: {list(data.keys())}") # REMOVED DEBUG
        
        if 'metrics' in data:
            md.append("## Overall Metrics\n")
            for key, value in data.get('metrics', {}).items():
                md.append(f"- **{key.replace('_', ' ').title()}**: {value}\n")
                
        if 'files' in data:
            md.append("\n## File Analysis\n")
            for file_path, analysis in data['files'].items():
                # Use basename for File Analysis headers too for consistency
                filename = os.path.basename(file_path)
                md.append(f"\n### `{filename}`\n")
                md.append(f"- Full Path: `{file_path}`\n") # Optionally add full path
                md.append(f"- Lines: {analysis['lines']}\n")
                md.append(f"- Cognitive Load: {analysis['complexity']['cognitive_load']:.1f}\n")
                
                if analysis.get('imports'):
                    md.append("\n#### Imports\n")
                    for imp in analysis['imports']:
                        md.append(f"- `{imp}`\n")
                        
                if analysis.get('classes'):
                    md.append("\n#### Classes\n")
                    for cls in analysis['classes']:
                        md.append(f"\n##### `{cls['name']}`\n")
                        if cls['inheritance']:
                            md.append(f"Inherits from: `{cls['inheritance']}`\n")
                        if cls['doc'] != 'No docstring':
                            md.append(f"\n{cls['doc']}\n")
                        if cls['methods']:
                            md.append("\nMethods:\n")
                            for method in cls['methods']:
                                md.append(f"- `{method['name']}({', '.join(method['params'])})`\n")
                                
                if analysis.get('functions'):
                    md.append("\n#### Functions\n")
                    for func in analysis['functions']:
                        md.append(f"\n##### `{func['name']}`\n")
                        md.append(f"```python\ndef {func['name']}({', '.join(func['params'])})\n```\n")
                        if func['doc'] != 'No docstring':
                            md.append(f"\n{func['doc']}\n")
                            
        if 'dependencies' in data and data['dependencies']:
            md.append("\n## Dependencies\n")
            # self.logger.debug(f"Processing dependencies section. Keys: {list(data['dependencies'].keys())}\") # REMOVED DEBUG
            for file_path, deps in data['dependencies'].items():
                # Use basename for Dependencies headers
                filename = os.path.basename(file_path)
                # --- DEBUG LOGGING REMOVED --- 
                # self.logger.debug(f"  Dep Path: {file_path}, Basename: {filename}, Expected: module_a.py")
                # ---------------------------
                md.append(f"\n### `{filename}`\n")
                md.append(f"- Full Path: `{file_path}`\n") # Optionally add full path
                if deps.get('imports'):
                    md.append("\nImports:\n")
                    for imp in deps['imports']:
                        md.append(f"- `{imp}`\n")
                if deps.get('imported_by'):
                    md.append("\nImported by:\n")
                    for imp_by_path in deps['imported_by']:
                        imp_by_filename = os.path.basename(imp_by_path)
                        md.append(f"- `{imp_by_filename}` (`{imp_by_path}`)\n") 
                        
        # self.logger.debug("Finished Markdown conversion.") # REMOVED DEBUG
        return ''.join(md) 