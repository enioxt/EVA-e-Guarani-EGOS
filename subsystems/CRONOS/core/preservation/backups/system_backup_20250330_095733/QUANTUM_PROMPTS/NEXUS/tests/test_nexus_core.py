"""
EVA & GUARANI - NEXUS Core Tests
Version: 1.0.0
"""

import json
import os
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd

from core.python.nexus_core import NEXUSCore

@pytest.fixture
def nexus():
    """Create a NEXUSCore instance for testing."""
    with patch('core.python.nexus_core.CursorAPI') as mock_cursor:
        instance = NEXUSCore()
        instance.cursor = mock_cursor
        return instance

@pytest.fixture
def sample_code():
    """Sample Python code for testing."""
    return """
import os
from pathlib import Path
import numpy as np

class TestClass:
    \"\"\"Test class docstring.\"\"\"
    
    def __init__(self):
        \"\"\"Initialize test class.\"\"\"
        self.value = 42
        
    def test_method(self, param1: int) -> str:
        \"\"\"Test method docstring.\"\"\"
        if param1 > 0:
            return "positive"
        return "negative"

def test_function(a: int, b: int) -> int:
    \"\"\"Test function docstring.\"\"\"
    return a + b
"""

def test_init(nexus):
    """Test NEXUSCore initialization."""
    assert isinstance(nexus.config, dict)
    assert nexus.vectorizer is not None
    assert nexus.logger is not None

def test_analyze_code(nexus, sample_code, tmp_path):
    """Test code analysis functionality."""
    # Create temporary file with sample code
    test_file = tmp_path / "test.py"
    test_file.write_text(sample_code)
    
    # Analyze code
    metrics = nexus.analyze_code(str(test_file))
    
    # Verify metrics
    assert isinstance(metrics, dict)
    assert 'lines' in metrics
    assert 'chars' in metrics
    assert 'complexity' in metrics
    assert 'imports' in metrics
    assert 'functions' in metrics
    assert 'classes' in metrics
    
    # Check specific metrics
    assert metrics['lines'] > 0
    assert len(metrics['imports']) == 3
    assert len(metrics['functions']) == 1
    assert len(metrics['classes']) == 1

def test_calculate_complexity(nexus, sample_code):
    """Test complexity calculation."""
    complexity = nexus._calculate_complexity(sample_code)
    
    assert isinstance(complexity, dict)
    assert 'max_depth' in complexity
    assert 'avg_depth' in complexity
    assert 'cognitive_load' in complexity
    assert complexity['max_depth'] >= 0
    assert complexity['avg_depth'] >= 0
    assert complexity['cognitive_load'] >= 0

def test_extract_imports(nexus, sample_code):
    """Test import statement extraction."""
    imports = nexus._extract_imports(sample_code)
    
    assert isinstance(imports, list)
    assert len(imports) == 3
    assert 'import os' in imports
    assert 'from pathlib import Path' in imports
    assert 'import numpy as np' in imports

def test_extract_functions(nexus, sample_code):
    """Test function extraction."""
    functions = nexus._extract_functions(sample_code)
    
    assert isinstance(functions, list)
    assert len(functions) == 1
    
    func = functions[0]
    assert func['name'] == 'test_function'
    assert func['params'] == 'a: int, b: int'
    assert 'Test function docstring' in func['doc']

def test_extract_classes(nexus, sample_code):
    """Test class extraction."""
    classes = nexus._extract_classes(sample_code)
    
    assert isinstance(classes, list)
    assert len(classes) == 1
    
    cls = classes[0]
    assert cls['name'] == 'TestClass'
    assert 'Test class docstring' in cls['doc']
    assert len(cls['methods']) == 2  # __init__ and test_method

def test_extract_methods(nexus, sample_code):
    """Test method extraction."""
    lines = sample_code.splitlines()
    methods = nexus._extract_methods(lines[5:])  # Start from class definition
    
    assert isinstance(methods, list)
    assert len(methods) == 2
    
    init_method = methods[0]
    assert init_method['name'] == '__init__'
    assert 'Initialize test class' in init_method['doc']
    
    test_method = methods[1]
    assert test_method['name'] == 'test_method'
    assert test_method['params'] == 'param1: int'
    assert 'Test method docstring' in test_method['doc']

def test_analyze_dependencies(nexus, tmp_path):
    """Test dependency analysis."""
    # Create test files
    file1 = tmp_path / "module1.py"
    file1.write_text("import os\nfrom module2 import func")
    
    file2 = tmp_path / "module2.py"
    file2.write_text("def func():\n    pass")
    
    files = [str(file1), str(file2)]
    deps = nexus.analyze_dependencies(files)
    
    assert isinstance(deps, dict)
    assert len(deps) == 2
    assert 'imports' in deps[str(file1)]
    assert 'imported_by' in deps[str(file2)]

def test_export_analysis_json(nexus):
    """Test analysis export to JSON."""
    data = {
        'metrics': {'lines': 100, 'complexity': 5},
        'dependencies': {'file1.py': {'imports': [], 'imported_by': []}}
    }
    
    result = nexus.export_analysis(data, 'json')
    assert isinstance(result, str)
    
    # Verify JSON is valid
    parsed = json.loads(result)
    assert parsed == data

def test_export_analysis_markdown(nexus):
    """Test analysis export to Markdown."""
    data = {
        'metrics': {'lines': 100, 'complexity': 5},
        'dependencies': {'file1.py': {'imports': ['os'], 'imported_by': []}}
    }
    
    result = nexus.export_analysis(data, 'md')
    assert isinstance(result, str)
    assert '# NEXUS Analysis Report' in result
    assert '## Code Metrics' in result
    assert '## Dependencies' in result

def test_analyze_workspace(nexus):
    """Test workspace analysis."""
    # Mock workspace files
    nexus.cursor.get_workspace_files.return_value = ['file1.py', 'file2.py']
    
    # Mock file analysis results
    with patch.object(nexus, 'analyze_code') as mock_analyze:
        mock_analyze.return_value = {
            'lines': 100,
            'chars': 1000,
            'complexity': {'cognitive_load': 5, 'max_depth': 3, 'avg_depth': 2},
            'imports': [],
            'functions': [],
            'classes': []
        }
        
        with patch.object(nexus, 'analyze_dependencies') as mock_deps:
            mock_deps.return_value = {}
            
            analysis = nexus.analyze_workspace()
            
            assert isinstance(analysis, dict)
            assert 'files' in analysis
            assert 'dependencies' in analysis
            assert 'metrics' in analysis
            assert analysis['metrics']['total_files'] == 2
            assert analysis['metrics']['total_lines'] == 200

def test_suggest_improvements(nexus):
    """Test improvement suggestions."""
    analysis = {
        'files': {
            'complex.py': {
                'complexity': {
                    'cognitive_load': 25,
                    'max_depth': 6
                }
            }
        },
        'dependencies': {
            'heavy.py': {
                'imports': ['mod' + str(i) for i in range(20)],
                'imported_by': ['file' + str(i) for i in range(15)]
            }
        }
    }
    
    suggestions = nexus.suggest_improvements(analysis)
    assert isinstance(suggestions, list)
    assert len(suggestions) > 0
    
    # Verify suggestion structure
    for suggestion in suggestions:
        assert 'file' in suggestion
        assert 'type' in suggestion
        assert 'severity' in suggestion
        assert 'message' in suggestion

def test_invalid_export_format(nexus):
    """Test error handling for invalid export format."""
    data = {'test': 'data'}
    with pytest.raises(ValueError):
        nexus.export_analysis(data, 'invalid_format')

def test_file_not_found(nexus):
    """Test error handling for non-existent file."""
    with pytest.raises(Exception):
        nexus.analyze_code('nonexistent.py')

def test_workspace_analysis_error(nexus):
    """Test error handling in workspace analysis."""
    nexus.cursor.get_workspace_files.side_effect = Exception("API Error")
    with pytest.raises(Exception):
        nexus.analyze_workspace() 