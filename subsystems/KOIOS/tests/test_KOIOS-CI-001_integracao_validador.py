#!/usr/bin/env python3
"""
EVA & GUARANI EGOS - Tests for KOIOS Pattern Validator CI/CD Integration
Version: 1.0.0
Last Updated: 2025-04-01
"""

import os
import json
import pytest
from pathlib import Path
from datetime import datetime
from unittest.mock import patch, MagicMock

from ..interfaces.KOIOS_CI_001_integracao_validador import (
    CIIntegration,
    CIEnvironment,
    main
)

@pytest.fixture
def temp_test_env(tmp_path):
    """Create a temporary test environment"""
    # Create required directories
    config_dir = tmp_path / "subsystems" / "KOIOS" / "config"
    artifacts_dir = tmp_path / "artifacts"
    config_dir.mkdir(parents=True)
    artifacts_dir.mkdir(parents=True)

    # Create config file
    config = {
        "integration": {
            "ci_cd": {
                "enabled": True,
                "fail_on_error": True,
                "fail_on_warning": False
            }
        }
    }
    config_path = config_dir / "validator_config.json"
    with open(config_path, "w") as f:
        json.dump(config, f)

    return tmp_path

@pytest.fixture
def ci_integration(temp_test_env):
    """Create a CIIntegration instance"""
    with patch.dict(os.environ, {"GITHUB_ACTIONS": "true",
                                "GITHUB_WORKSPACE": str(temp_test_env)}):
        return CIIntegration()

def test_environment_detection_github(temp_test_env):
    """Test GitHub Actions environment detection"""
    env_vars = {
        "GITHUB_ACTIONS": "true",
        "GITHUB_WORKSPACE": str(temp_test_env),
        "GITHUB_REF_NAME": "main",
        "GITHUB_SHA": "abc123",
        "GITHUB_RUN_NUMBER": "42"
    }
    
    with patch.dict(os.environ, env_vars):
        ci = CIIntegration()
        assert ci.environment.provider == "github"
        assert ci.environment.branch == "main"
        assert ci.environment.commit == "abc123"
        assert ci.environment.build_number == "42"
        assert ci.environment.workspace == Path(temp_test_env)

def test_environment_detection_gitlab(temp_test_env):
    """Test GitLab CI environment detection"""
    env_vars = {
        "GITLAB_CI": "true",
        "CI_PROJECT_DIR": str(temp_test_env),
        "CI_COMMIT_REF_NAME": "main",
        "CI_COMMIT_SHA": "abc123",
        "CI_PIPELINE_IID": "42"
    }
    
    with patch.dict(os.environ, env_vars, clear=True):
        ci = CIIntegration()
        assert ci.environment.provider == "gitlab"
        assert ci.environment.branch == "main"
        assert ci.environment.commit == "abc123"
        assert ci.environment.build_number == "42"
        assert ci.environment.workspace == Path(temp_test_env)

def test_environment_detection_jenkins(temp_test_env):
    """Test Jenkins environment detection"""
    env_vars = {
        "JENKINS_URL": "http://jenkins.example.com",
        "WORKSPACE": str(temp_test_env),
        "GIT_BRANCH": "main",
        "GIT_COMMIT": "abc123",
        "BUILD_NUMBER": "42"
    }
    
    with patch.dict(os.environ, env_vars, clear=True):
        ci = CIIntegration()
        assert ci.environment.provider == "jenkins"
        assert ci.environment.branch == "main"
        assert ci.environment.commit == "abc123"
        assert ci.environment.build_number == "42"
        assert ci.environment.workspace == Path(temp_test_env)

def test_environment_detection_local(temp_test_env):
    """Test local environment detection"""
    with patch.dict(os.environ, {}, clear=True):
        ci = CIIntegration()
        assert ci.environment.provider == "local"
        assert ci.environment.branch == "local"
        assert ci.environment.commit == "local"
        assert ci.environment.build_number == "local"
        assert ci.environment.workspace == Path.cwd()

def test_load_config_success(ci_integration, temp_test_env):
    """Test successful config loading"""
    config = ci_integration.config
    assert config is not None
    assert config.get("enabled") is True
    assert config.get("fail_on_error") is True
    assert config.get("fail_on_warning") is False

def test_load_config_missing_file(temp_test_env):
    """Test config loading with missing file"""
    config_file = temp_test_env / "subsystems" / "KOIOS" / "config" / "validator_config.json"
    config_file.unlink()
    
    with patch.dict(os.environ, {"GITHUB_ACTIONS": "true",
                                "GITHUB_WORKSPACE": str(temp_test_env)}):
        ci = CIIntegration()
        assert ci.config == {}

def test_save_report(ci_integration):
    """Test saving validation report"""
    report = "Test Report"
    results = {
        "stats": {
            "violations": {
                "error": 0,
                "warning": 1
            }
        }
    }
    
    report_path = ci_integration._save_report(report, results)
    
    assert report_path.exists()
    assert report_path.parent == ci_integration.environment.artifacts_dir
    assert report_path.suffix == ".md"
    
    # Check JSON results
    json_path = report_path.with_suffix('.json')
    assert json_path.exists()
    with open(json_path) as f:
        saved_results = json.load(f)
        assert saved_results == results

def test_create_annotations(ci_integration, capsys):
    """Test creating CI-specific annotations"""
    violations = [
        {
            "severity": "error",
            "path": "test.py",
            "line": 42,
            "violation": "Test error",
            "suggestion": "Fix it"
        },
        {
            "severity": "warning",
            "path": "test2.py",
            "line": 24,
            "violation": "Test warning",
            "suggestion": "Consider fixing"
        }
    ]
    
    ci_integration.create_annotations(violations)
    captured = capsys.readouterr()
    
    if ci_integration.environment.provider == "github":
        assert "::error file=test.py,line=42::" in captured.out
        assert "::warning file=test2.py,line=24::" in captured.out
    elif ci_integration.environment.provider == "gitlab":
        assert "error: test.py:42" in captured.out
        assert "warning: test2.py:24" in captured.out
    elif ci_integration.environment.provider == "jenkins":
        assert "[ERROR] test.py:42" in captured.out
        assert "[WARNING] test2.py:24" in captured.out

def test_run_validation_success(ci_integration):
    """Test successful validation run"""
    mock_results = {
        "stats": {
            "violations": {
                "error": 0,
                "warning": 1
            }
        },
        "violations": []
    }
    
    with patch("..core.KOIOS_VALIDATE_001_padrao_nomenclatura.PatternValidator") as mock_validator:
        # Configure mock validator
        mock_instance = MagicMock()
        mock_instance.validate_tree.return_value = mock_results
        mock_instance.generate_report.return_value = "Test Report"
        mock_validator.return_value = mock_instance
        
        # Run validation
        success, message, report_path = ci_integration.run_validation()
        
        assert success is True
        assert "completed" in message
        assert "0 errors" in message
        assert "1 warning" in message
        assert report_path is not None
        assert report_path.exists()

def test_run_validation_failure(ci_integration):
    """Test validation run with failures"""
    mock_results = {
        "stats": {
            "violations": {
                "error": 2,
                "warning": 1
            }
        },
        "violations": []
    }
    
    with patch("..core.KOIOS_VALIDATE_001_padrao_nomenclatura.PatternValidator") as mock_validator:
        # Configure mock validator
        mock_instance = MagicMock()
        mock_instance.validate_tree.return_value = mock_results
        mock_instance.generate_report.return_value = "Test Report"
        mock_validator.return_value = mock_instance
        
        # Run validation
        success, message, report_path = ci_integration.run_validation()
        
        assert success is False
        assert "failed" in message
        assert "2 errors" in message
        assert "1 warning" in message
        assert report_path is not None
        assert report_path.exists()

def test_run_validation_exception(ci_integration):
    """Test validation run with exception"""
    with patch("..core.KOIOS_VALIDATE_001_padrao_nomenclatura.PatternValidator") as mock_validator:
        # Configure mock to raise exception
        mock_validator.side_effect = Exception("Test error")
        
        # Run validation
        success, message, report_path = ci_integration.run_validation()
        
        assert success is False
        assert "Test error" in message
        assert report_path is None

def test_main_function_success(temp_test_env):
    """Test successful main function execution"""
    with patch.dict(os.environ, {"GITHUB_ACTIONS": "true",
                                "GITHUB_WORKSPACE": str(temp_test_env)}), \
         patch("..interfaces.KOIOS_CI_001_integracao_validador.CIIntegration") as mock_ci:
        
        # Configure mock
        mock_instance = MagicMock()
        mock_instance.run_validation.return_value = (True, "Success", Path("report.md"))
        mock_ci.return_value = mock_instance
        
        # Run main
        result = main()
        assert result == 0

def test_main_function_failure(temp_test_env):
    """Test main function with failure"""
    with patch.dict(os.environ, {"GITHUB_ACTIONS": "true",
                                "GITHUB_WORKSPACE": str(temp_test_env)}), \
         patch("..interfaces.KOIOS_CI_001_integracao_validador.CIIntegration") as mock_ci:
        
        # Configure mock
        mock_instance = MagicMock()
        mock_instance.run_validation.return_value = (False, "Error", Path("report.md"))
        mock_ci.return_value = mock_instance
        
        # Run main
        result = main()
        assert result == 1

def test_main_function_exception(temp_test_env):
    """Test main function with exception"""
    with patch.dict(os.environ, {"GITHUB_ACTIONS": "true",
                                "GITHUB_WORKSPACE": str(temp_test_env)}), \
         patch("..interfaces.KOIOS_CI_001_integracao_validador.CIIntegration") as mock_ci:
        
        # Configure mock to raise exception
        mock_ci.side_effect = Exception("Test error")
        
        # Run main
        result = main()
        assert result == 1

# ✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧ 