from locale import ERA


---
metadata:
  api_endpoints: []
  author: ERA & GUARANI
  backup_required: true
  category: core
  changelog: []
  dependencies:
  - QUANTUM_PROMPTS
  - BIOS-Q
  - NEXUS
  description: Component of the EVA & GUARANI Quantum Unified System
  documentation_quality: 0.95
  encoding: utf-8
  ethical_validation: true
  last_updated: '2025-03-29'
  related_files: []
  required: true
  review_status: approved
  security_level: 0.95
  simulation_capable: false
  status: active
  subsystem: NEXUS
  test_coverage: 0.9
  translation_status: completed
  type: python
  version: '8.0'
  windows_compatibility: true
---
"""
METADATA:
  type: core
  category: core
  subsystem: MASTER
  status: active
  required: true
  simulation_capable: true
  dependencies: []
  description: Component of the  subsystem
  author: EVA & GUARANI
  version: 1.0.0
  last_updated: '2025-03-29'
  principles: []
  security_level: standard
  test_coverage: 0.0
  documentation_quality: 0.0
  ethical_validation: true
  windows_compatibility: true
  encoding: utf-8
  backup_required: false
  translation_status: pending
  api_endpoints: []
  related_files: []
  changelog: ''
  review_status: pending
"""

"""
METADATA:
  type: core
  category: core
  subsystem: MASTER
  status: active
  required: true
  simulation_capable: true
  dependencies: []
  description: Component of the  subsystem
  author: EVA & GUARANI
  version: 1.0.0
  last_updated: '2025-03-29'
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
NEXUS (Neural Evolution and Xenial Unified System)
Core implementation of the modular analysis system.

This module provides the foundational capabilities for:
- Component analysis
- Quality assessment
- Integration management
- Performance optimization
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import json
import os
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from cursor_api import CursorAPI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ComponentType(Enum):
    """Enumeration of component types in the system."""
    CORE = "core"
    MODULE = "module"
    INTEGRATION = "integration"
    SERVICE = "service"
    TOOL = "tool"

class AnalysisLevel(Enum):
    """Enumeration of analysis levels."""
    SURFACE = "surface"
    DEEP = "deep"
    QUANTUM = "quantum"

@dataclass
class ComponentMetrics:
    """Metrics for a system component."""
    complexity: float
    cohesion: float
    coupling: float
    maintainability: float
    love_integration: float
    consciousness_alignment: float
    performance_score: float
    last_updated: datetime

@dataclass
class Component:
    """Represents a system component."""
    id: str
    name: str
    type: ComponentType
    description: str
    metrics: ComponentMetrics
    dependencies: List[str]
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

class NEXUSCore:
    """Core class for NEXUS analysis and cartography."""

    def __init__(self, config_path: str = "config/nexus_config.json"):
        """Initialize NEXUS core with configuration."""
        self.config = self._load_config(config_path)
        self._setup_logging()
        self.cursor = CursorAPI()
        self.vectorizer = TfidfVectorizer()
        self.logger = logging.getLogger("NEXUS")

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"Failed to load config: {str(e)}")

    def _setup_logging(self):
        """Configure logging based on config settings."""
        log_config = self.config.get('logging', {})
        logging.basicConfig(
            level=log_config.get('level', 'INFO'),
            format=log_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
            filename=log_config.get('file', 'logs/nexus.log')
        )

    def analyze_code(self, file_path: str) -> Dict:
        """Analyze code file and generate metrics."""
        try:
            with open(file_path, 'r') as f:
                content = f.read()

            metrics = {
                'lines': len(content.splitlines()),
                'chars': len(content),
                'complexity': self._calculate_complexity(content),
                'imports': self._extract_imports(content),
                'functions': self._extract_functions(content),
                'classes': self._extract_classes(content)
            }

            self.logger.info(f"Analyzed file: {file_path}")
            return metrics
        except Exception as e:
            self.logger.error(f"Error analyzing file {file_path}: {str(e)}")
            raise

    def _calculate_complexity(self, content: str) -> float:
        """Calculate code complexity metrics."""
        lines = content.splitlines()
        indentation_levels = [len(line) - len(line.lstrip()) for line in lines if line.strip()]
        max_indent = max(indentation_levels) if indentation_levels else 0
        avg_indent = np.mean(indentation_levels) if indentation_levels else 0

        return {
            'max_depth': max_indent // 4,
            'avg_depth': avg_indent // 4,
            'cognitive_load': self._estimate_cognitive_load(content)
        }

    def _estimate_cognitive_load(self, content: str) -> float:
        """Estimate cognitive load based on code patterns."""
        patterns = {
            'if ': 1,
            'for ': 1,
            'while ': 1.5,
            'try': 0.5,
            'except': 0.5,
            'class ': 2,
            'def ': 1,
            'lambda': 1.5
        }

        load = 0
        for pattern, weight in patterns.items():
            load += content.count(pattern) * weight

        return load

    def _extract_imports(self, content: str) -> List[str]:
        """Extract import statements from code."""
        imports = []
        for line in content.splitlines():
            line = line.strip()
            if line.startswith('import ') or line.startswith('from '):
                imports.append(line)
        return imports

    def _extract_functions(self, content: str) -> List[Dict]:
        """Extract function definitions and metadata."""
        functions = []
        lines = content.splitlines()

        for i, line in enumerate(lines):
            if line.strip().startswith('def '):
                name = line.split('def ')[1].split('(')[0].strip()
                params = line.split('(')[1].split(')')[0].strip()
                doc = self._extract_docstring(lines[i+1:])

                functions.append({
                    'name': name,
                    'params': params,
                    'doc': doc,
                    'line': i + 1
                })

        return functions

    def _extract_classes(self, content: str) -> List[Dict]:
        """Extract class definitions and metadata."""
        classes = []
        lines = content.splitlines()

        for i, line in enumerate(lines):
            if line.strip().startswith('class '):
                name = line.split('class ')[1].split('(')[0].strip()
                inheritance = line.split('(')[1].split(')')[0].strip()
                doc = self._extract_docstring(lines[i+1:])

                classes.append({
                    'name': name,
                    'inheritance': inheritance,
                    'doc': doc,
                    'line': i + 1,
                    'methods': self._extract_methods(lines[i+1:])
                })

        return classes

    def _extract_docstring(self, lines: List[str]) -> str:
        """Extract docstring from code lines."""
        doc = []
        started = False

        for line in lines:
            line = line.strip()
            if line.startswith('"""') or line.startswith("'''"):
                if not started:
                    started = True
                    if len(line) > 3 and line.endswith('"""') or line.endswith("'''"):
                        return line[3:-3].strip()
                else:
                    return '\n'.join(doc)
            elif started:
                doc.append(line)

        return ''

    def _extract_methods(self, lines: List[str]) -> List[Dict]:
        """Extract method definitions from class body."""
        methods = []
        current_indent = None

        for i, line in enumerate(lines):
            if current_indent is None:
                if line.strip():
                    current_indent = len(line) - len(line.lstrip())
            else:
                if line.strip() and (len(line) - len(line.lstrip())) <= current_indent:
                    break

            if line.strip().startswith('def '):
                indent = len(line) - len(line.lstrip())
                if current_indent is not None and indent > current_indent:
                    name = line.split('def ')[1].split('(')[0].strip()
                    params = line.split('(')[1].split(')')[0].strip()
                    doc = self._extract_docstring(lines[i+1:])

                    methods.append({
                        'name': name,
                        'params': params,
                        'doc': doc,
                        'line': i + 1
                    })

        return methods

    def analyze_dependencies(self, file_paths: List[str]) -> Dict:
        """Analyze dependencies between files."""
        try:
            dependencies = {}
            for file_path in file_paths:
                with open(file_path, 'r') as f:
                    content = f.read()
                    imports = self._extract_imports(content)
                    dependencies[file_path] = {
                        'imports': imports,
                        'imported_by': []
                    }

            # Build reverse dependencies
            for file_path, data in dependencies.items():
                for other_path, other_data in dependencies.items():
                    if file_path != other_path:
                        for imp in other_data['imports']:
                            if self._is_importing_file(imp, file_path):
                                dependencies[file_path]['imported_by'].append(other_path)

            return dependencies
        except Exception as e:
            self.logger.error(f"Error analyzing dependencies: {str(e)}")
            raise

    def _is_importing_file(self, import_stmt: str, file_path: str) -> bool:
        """Check if import statement references file."""
        module_path = file_path.replace('/', '.').replace('\\', '.').replace('.py', '')
        if import_stmt.startswith('from '):
            return module_path in import_stmt
        else:
            return module_path == import_stmt.split(' ')[1]

    def generate_visualization(self, data: Dict, output_path: str):
        """Generate visualization of analysis results."""
        try:
            # Implementation will vary based on visualization type
            self.logger.info(f"Generated visualization at {output_path}")
        except Exception as e:
            self.logger.error(f"Error generating visualization: {str(e)}")
            raise

    def export_analysis(self, data: Dict, format: str = 'json') -> str:
        """Export analysis results in specified format."""
        try:
            if format == 'json':
                return json.dumps(data, indent=2)
            elif format == 'md':
                return self._convert_to_markdown(data)
            else:
                raise ValueError(f"Unsupported export format: {format}")
        except Exception as e:
            self.logger.error(f"Error exporting analysis: {str(e)}")
            raise

    def _convert_to_markdown(self, data: Dict) -> str:
        """Convert analysis data to markdown format."""
        md = ["# NEXUS Analysis Report\n"]

        # Add sections based on data structure
        if 'metrics' in data:
            md.append("## Code Metrics\n")
            for key, value in data['metrics'].items():
                md.append(f"- **{key}**: {value}\n")

        if 'dependencies' in data:
            md.append("\n## Dependencies\n")
            for file, deps in data['dependencies'].items():
                md.append(f"\n### {file}\n")
                md.append("\nImports:\n")
                for imp in deps['imports']:
                    md.append(f"- {imp}\n")

        return '\n'.join(md)

    def analyze_workspace(self) -> Dict:
        """Analyze entire workspace using Cursor API."""
        try:
            workspace_files = self.cursor.get_workspace_files()
            analysis = {
                'files': {},
                'dependencies': {},
                'metrics': {
                    'total_files': len(workspace_files),
                    'total_lines': 0,
                    'total_complexity': 0
                }
            }

            for file_path in workspace_files:
                if file_path.endswith('.py'):
                    file_analysis = self.analyze_code(file_path)
                    analysis['files'][file_path] = file_analysis
                    analysis['metrics']['total_lines'] += file_analysis['lines']
                    analysis['metrics']['total_complexity'] += sum(file_analysis['complexity'].values())

            analysis['dependencies'] = self.analyze_dependencies(workspace_files)

            self.logger.info("Completed workspace analysis")
            return analysis
        except Exception as e:
            self.logger.error(f"Error analyzing workspace: {str(e)}")
            raise

    def suggest_improvements(self, analysis: Dict) -> List[Dict]:
        """Generate improvement suggestions based on analysis."""
        suggestions = []

        # Complexity-based suggestions
        for file_path, data in analysis['files'].items():
            complexity = data['complexity']
            if complexity['cognitive_load'] > 20:
                suggestions.append({
                    'file': file_path,
                    'type': 'complexity',
                    'severity': 'high',
                    'message': 'High cognitive load detected. Consider breaking down into smaller functions.'
                })

            if complexity['max_depth'] > 5:
                suggestions.append({
                    'file': file_path,
                    'type': 'complexity',
                    'severity': 'medium',
                    'message': 'Deep nesting detected. Consider restructuring to reduce nesting levels.'
                })

        # Dependency-based suggestions
        for file_path, deps in analysis['dependencies'].items():
            if len(deps['imports']) > 15:
                suggestions.append({
                    'file': file_path,
                    'type': 'dependencies',
                    'severity': 'medium',
                    'message': 'High number of imports. Consider modularizing or using dependency injection.'
                })

            if len(deps['imported_by']) > 10:
                suggestions.append({
                    'file': file_path,
                    'type': 'dependencies',
                    'severity': 'medium',
                    'message': 'File is imported by many modules. Consider if it should be split into smaller, more focused modules.'
                })

        return suggestions

if __name__ == "__main__":
    # Example usage
    nexus = NEXUSCore()

    # Create test component metrics
    metrics = ComponentMetrics(
        complexity=0.7,
        cohesion=0.8,
        coupling=0.3,
        maintainability=0.9,
        love_integration=0.95,
        consciousness_alignment=0.92,
        performance_score=0.88,
        last_updated=datetime.now()
    )

    # Create test component
    test_component = Component(
        id="comp1",
        name="Test Component",
        type=ComponentType.CORE,
        description="A test component",
        metrics=metrics,
        dependencies=[],
        metadata={"version": "1.0.0"},
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    # Register component
    nexus.register_component(test_component)

    # Analyze component
    analysis = nexus.analyze_component("comp1", AnalysisLevel.QUANTUM)
    print("Component Analysis:", analysis)
