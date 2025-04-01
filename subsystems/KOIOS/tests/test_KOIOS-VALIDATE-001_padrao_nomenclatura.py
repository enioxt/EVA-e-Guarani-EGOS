#!/usr/bin/env python3
"""
EVA & GUARANI EGOS - Tests for KOIOS Pattern Validation System
Version: 1.0.0
Last Updated: 2025-04-01
"""

import os
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open
import ast

# Import the validator
from ..core.KOIOS_VALIDATE_001_padrao_nomenclatura import (
    PatternValidator,
    ValidationType,
    ValidationRule
)

@pytest.fixture
def temp_test_env(tmp_path):
    """Create a temporary test environment with sample files and directories"""
    # Create standard directories
    core_dir = tmp_path / "core"
    tests_dir = tmp_path / "tests"
    docs_dir = tmp_path / "docs"
    core_dir.mkdir()
    tests_dir.mkdir()
    docs_dir.mkdir()

    # Create sample files
    valid_files = [
        core_dir / "KOIOS-VALIDATE-001_padrao_nomenclatura.py",
        tests_dir / "test_KOIOS-VALIDATE-001_padrao_nomenclatura.py",
        docs_dir / "KOIOS-DOC-001_guia_implementacao.md"
    ]

    invalid_files = [
        core_dir / "invalid_file.py",
        tests_dir / "test_invalid.py",
        docs_dir / "invalid_doc.md"
    ]

    # Create all files
    for file in valid_files + invalid_files:
        file.touch()

    return tmp_path

@pytest.fixture
def validator(temp_test_env):
    """Create a PatternValidator instance with the test environment"""
    return PatternValidator(temp_test_env)

def test_validator_initialization(validator):
    """Test validator initialization"""
    assert validator.base_path.exists()
    assert validator.rules is not None
    assert ValidationType.FILENAME in validator.rules
    assert ValidationType.DIRECTORY in validator.rules
    assert ValidationType.CODE in validator.rules

def test_validate_valid_file_name(validator):
    """Test validation of valid file names"""
    valid_files = [
        "KOIOS-VALIDATE-001_padrao_nomenclatura.py",
        "test_KOIOS-VALIDATE-001_padrao_nomenclatura.py",
        "KOIOS-DOC-001_guia_implementacao.md"
    ]

    for file_name in valid_files:
        file_path = validator.base_path / "core" / file_name
        violations = validator.validate_file_name(file_path)
        assert len(violations) == 0, f"Expected no violations for {file_name}"

def test_validate_invalid_file_name(validator):
    """Test validation of invalid file names"""
    invalid_files = [
        "invalid_file.py",
        "test_invalid.py",
        "invalid_doc.md"
    ]

    for file_name in invalid_files:
        file_path = validator.base_path / "core" / file_name
        violations = validator.validate_file_name(file_path)
        assert len(violations) > 0, f"Expected violations for {file_name}"
        assert violations[0]["severity"] == "error"
        assert "pattern" in violations[0]["violation"]

def test_validate_directory_structure(validator):
    """Test validation of directory structure"""
    # Test valid directory
    core_dir = validator.base_path / "core"
    violations = validator.validate_directory_structure(core_dir)
    assert len(violations) == 0, "Expected no violations for 'core' directory"

    # Test invalid directory
    invalid_dir = validator.base_path / "invalid_dir"
    invalid_dir.mkdir()
    violations = validator.validate_directory_structure(invalid_dir)
    assert len(violations) > 0, "Expected violations for invalid directory"
    assert violations[0]["severity"] == "warning"

def test_validate_python_code():
    """Test validation of Python code conventions"""
    valid_code = '''
class EthikBackupManager:
    def create_backup_manifest(self):
        pass
'''
    invalid_code = '''
class invalidClass:
    def InvalidFunction(self):
        pass
'''

    # Test valid code
    with patch('builtins.open', mock_open(read_data=valid_code)):
        validator = PatternValidator(Path())
        violations = validator.validate_python_code(Path("test.py"))
        assert len(violations) == 0, "Expected no violations for valid code"

    # Test invalid code
    with patch('builtins.open', mock_open(read_data=invalid_code)):
        validator = PatternValidator(Path())
        violations = validator.validate_python_code(Path("test.py"))
        assert len(violations) > 0, "Expected violations for invalid code"
        assert any("class name" in v["violation"].lower() for v in violations)
        assert any("function name" in v["violation"].lower() for v in violations)

def test_validate_tree(validator, temp_test_env):
    """Test validation of entire directory tree"""
    results = validator.validate_tree()
    
    assert "violations" in results
    assert "stats" in results
    assert results["stats"]["total_files"] > 0
    assert results["stats"]["total_directories"] > 0
    assert results["stats"]["violations"]["error"] > 0  # Due to invalid files
    assert results["stats"]["violations"]["warning"] > 0  # Due to invalid directories

def test_generate_report(validator):
    """Test report generation"""
    results = {
        "violations": [
            {
                "type": "filename",
                "path": "invalid_file.py",
                "violation": "Invalid file name",
                "severity": "error",
                "suggestion": "Rename following pattern"
            }
        ],
        "stats": {
            "total_files": 10,
            "total_directories": 3,
            "violations": {
                "error": 1,
                "warning": 2
            }
        }
    }

    report = validator.generate_report(results)
    
    assert "EVA & GUARANI - Pattern Validation Report" in report
    assert "Statistics" in report
    assert "Violations" in report
    assert "ERROR" in report
    assert "invalid_file.py" in report

def test_main_function(temp_test_env):
    """Test main function execution"""
    with patch('sys.argv', ['script.py', '--path', str(temp_test_env)]):
        from ..core.KOIOS_VALIDATE_001_padrao_nomenclatura import main
        exit_code = main()
        assert exit_code == 1  # Should be 1 due to errors in test environment

def test_validation_rule_creation():
    """Test creation of validation rules"""
    rule = ValidationRule(
        pattern=r"^test_.*\.py$",
        description="Test file pattern",
        example="test_example.py",
        severity="error",
        applies_to=[".py"]
    )
    
    assert rule.pattern == r"^test_.*\.py$"
    assert rule.severity == "error"
    assert ".py" in rule.applies_to

def test_validator_with_empty_directory(tmp_path):
    """Test validator behavior with empty directory"""
    validator = PatternValidator(tmp_path)
    results = validator.validate_tree()
    
    assert results["stats"]["total_files"] == 0
    assert results["stats"]["total_directories"] == 1  # Root directory
    assert results["stats"]["violations"]["error"] == 0
    assert results["stats"]["violations"]["warning"] == 1  # Root directory name warning

def test_validator_with_nonexistent_path():
    """Test validator behavior with nonexistent path"""
    nonexistent_path = Path("/nonexistent/path")
    validator = PatternValidator(nonexistent_path)
    
    with pytest.raises(Exception):
        validator.validate_tree()

# ✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧ 