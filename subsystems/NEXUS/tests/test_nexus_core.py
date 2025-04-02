#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - NEXUS Core Tests
===============================

Test suite for the NEXUS Core logic.

Version: 1.0.0
"""

import pytest
import logging
from pathlib import Path
import json
from typing import Dict

# Use absolute import now that project is installed editably
from subsystems.NEXUS.core.nexus_core import NEXUSCore

# Fixture for basic config
@pytest.fixture
def nexus_config() -> Dict:
    return {
        "analysis": {
             "suggestions": {
                  "cognitive_load_threshold_high": 50,
                  "imports_threshold": 15,
                  "imported_by_threshold": 10
             }
        }
    }

# Fixture for a logger
@pytest.fixture
def test_logger() -> logging.Logger:
    logger = logging.getLogger("TestNEXUSCore")
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False
    return logger

# Fixture for the project root using pytest's tmp_path
@pytest.fixture
def project_root(tmp_path: Path) -> Path:
    # Create dummy structure for testing workspace analysis
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    
    # module_a.py - Simple module with function and class
    module_a = """
import os
from typing import List, Optional

def func_a(x: int, y: Optional[str] = None) -> List[str]:
    \"\"\"Example function with docstring.\"\"\"
    if x > 0:
        return [y or 'default'] * x
    return []

class ClassA:
    \"\"\"Example class with docstring.\"\"\"
    def __init__(self, name: str):
        self.name = name
        
    def method_a(self) -> str:
        \"\"\"Example method with docstring.\"\"\"
        return f"Hello {self.name}"
        
    async def async_method(self):
        \"\"\"Async method example.\"\"\"
        return "async"
"""
    (src_dir / "module_a.py").write_text(module_a)
    
    # module_b.py - Module with imports and inheritance
    module_b = """
from .module_a import ClassA, func_a
import datetime as dt
from pathlib import Path

class B(ClassA):
    def run(self) -> None:
        super().method_a()
        func_a(5)
"""
    (src_dir / "module_b.py").write_text(module_b)
    
    # test_a.py - Test module with relative imports
    test_dir = tmp_path / "tests"
    test_dir.mkdir()
    test_a = """
from src.module_a import func_a, ClassA

def test_func_a():
    assert func_a(2, "test") == ["test", "test"]
    
def test_class_a():
    a = ClassA("test")
    assert a.method_a() == "Hello test"
"""
    (test_dir / "test_a.py").write_text(test_a)
    
    # Create ignored files
    venv_dir = tmp_path / ".venv"
    venv_dir.mkdir()
    (venv_dir / "ignored.py").write_text("print('ignored')")
    
    return tmp_path

# Fixture for NEXUSCore instance
@pytest.fixture
def nexus(nexus_config, test_logger, project_root) -> NEXUSCore:
    return NEXUSCore(config=nexus_config, logger=test_logger, project_root=project_root)

# --- Test Cases --- #

def test_nexus_initialization(nexus, nexus_config, test_logger, project_root):
    """Test basic initialization of NEXUSCore."""
    assert nexus.config == nexus_config
    assert nexus.logger == test_logger
    assert nexus.project_root == project_root

def test_analyze_code_success(nexus, project_root):
    """Test analyzing a valid Python file."""
    file_to_analyze = project_root / "src" / "module_a.py"
    analysis = nexus.analyze_code(str(file_to_analyze))
    
    assert analysis is not None
    assert "error" not in analysis
    assert analysis['lines'] > 0
    assert analysis['chars'] > 0
    
    # Check complexity
    assert 'complexity' in analysis
    assert 'cognitive_load' in analysis['complexity']
    assert analysis['complexity']['cognitive_load'] > 0  # Should count def, if, etc.
    
    # Check imports
    assert len(analysis['imports']) == 2
    assert any('import os' in imp for imp in analysis['imports'])
    assert any('from typing import List, Optional' in imp for imp in analysis['imports'])
    
    # Check functions
    assert len(analysis['functions']) == 1
    func = analysis['functions'][0]
    assert func['name'] == 'func_a'
    assert len(func['params']) == 2
    assert func['doc'] == 'Example function with docstring.'
    assert not func['is_async']
    
    # Check classes
    assert len(analysis['classes']) == 1
    cls = analysis['classes'][0]
    assert cls['name'] == 'ClassA'
    assert cls['doc'] == 'Example class with docstring.'
    assert len(cls['methods']) == 3  # __init__, method_a, async_method
    
    # Check methods
    methods = {m['name']: m for m in cls['methods']}
    assert '__init__' in methods
    assert 'method_a' in methods
    assert 'async_method' in methods
    assert methods['async_method']['is_async']
    assert methods['method_a']['doc'] == 'Example method with docstring.'

def test_analyze_code_file_not_found(nexus, project_root):
    """Test analyzing a non-existent file."""
    non_existent_file = project_root / "src" / "no_such_file.py"
    analysis = nexus.analyze_code(str(non_existent_file))
    assert analysis is None

def test_analyze_dependencies_basic(nexus, project_root):
    """Test dependency analysis with AST parsing."""
    py_files = [str(p) for p in project_root.rglob("*.py") if ".venv" not in str(p)]
    dependencies = nexus.analyze_dependencies(py_files)
    
    assert dependencies is not None
    
    module_a_path = str(project_root / "src" / "module_a.py")
    module_b_path = str(project_root / "src" / "module_b.py")
    test_a_path = str(project_root / "tests" / "test_a.py")
    
    # Check module_a.py
    assert module_a_path in dependencies
    assert len(dependencies[module_a_path]['imports']) == 2
    assert any('import os' in imp for imp in dependencies[module_a_path]['imports'])
    assert any('from typing import' in imp for imp in dependencies[module_a_path]['imports'])
    
    # Check module_b.py
    assert module_b_path in dependencies
    assert len(dependencies[module_b_path]['imports']) == 3
    assert any('from .module_a import' in imp for imp in dependencies[module_b_path]['imports'])
    
    # Check test_a.py
    assert test_a_path in dependencies
    assert len(dependencies[test_a_path]['imports']) == 1
    assert any('from src.module_a import' in imp for imp in dependencies[test_a_path]['imports'])
    
    # Check imported_by relationships
    assert module_b_path in dependencies[module_a_path]['imported_by']
    assert test_a_path in dependencies[module_a_path]['imported_by']

def test_analyze_workspace(nexus, project_root):
    """Test analyzing the workspace."""
    analysis = nexus.analyze_workspace()
    
    assert analysis is not None
    assert "error" not in analysis
    
    # Check metrics
    assert analysis['metrics']['total_files'] == 3  # module_a, module_b, test_a
    assert analysis['metrics']['total_lines'] > 0
    assert analysis['metrics']['total_functions'] > 0
    assert analysis['metrics']['total_classes'] > 0
    assert analysis['metrics']['avg_complexity'] > 0
    
    # Check file analysis
    assert len(analysis['files']) == 3
    assert str(project_root / "src" / "module_a.py") in analysis['files']
    assert str(project_root / "src" / "module_b.py") in analysis['files']
    assert str(project_root / "tests" / "test_a.py") in analysis['files']
    
    # Check dependencies
    assert 'dependencies' in analysis
    assert analysis['dependencies'] is not None

def test_suggest_improvements(nexus, project_root):
    """Test generating improvement suggestions."""
    workspace_analysis = nexus.analyze_workspace()
    assert workspace_analysis is not None
    
    suggestions = nexus.suggest_improvements(workspace_analysis)
    assert isinstance(suggestions, list)
    
    # Group suggestions by type
    by_type = {}
    for suggestion in suggestions:
        by_type.setdefault(suggestion['type'], []).append(suggestion)
    
    # We expect some documentation suggestions since some functions/methods lack docstrings
    assert 'documentation' in by_type
    
    # We don't expect complexity warnings for our simple test files
    complexity_warnings = by_type.get('complexity', [])
    assert all(s['severity'] != 'high' for s in complexity_warnings)

def test_export_analysis_json(nexus, project_root):
    """Test exporting analysis to JSON."""
    workspace_analysis = nexus.analyze_workspace()
    json_output = nexus.export_analysis(workspace_analysis, format='json')
    
    assert isinstance(json_output, str)
    try:
        data = json.loads(json_output)
        assert 'metrics' in data
        assert 'files' in data
        assert 'dependencies' in data
    except json.JSONDecodeError:
        pytest.fail("Exported JSON is invalid")

def test_export_analysis_markdown(nexus, project_root):
    """Test exporting analysis to Markdown."""
    workspace_analysis = nexus.analyze_workspace()
    md_output = nexus.export_analysis(workspace_analysis, format='md')
    
    assert isinstance(md_output, str)
    assert "# NEXUS Analysis Report" in md_output
    assert "## Overall Metrics" in md_output
    assert "## File Analysis" in md_output
    assert "## Dependencies" in md_output
    
    # Check for specific content
    assert "`module_a.py`" in md_output
    assert "ClassA" in md_output
    assert "func_a" in md_output
    assert "Example function with docstring" in md_output 