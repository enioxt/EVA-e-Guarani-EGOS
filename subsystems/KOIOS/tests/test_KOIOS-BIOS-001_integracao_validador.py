#!/usr/bin/env python3
"""
EVA & GUARANI EGOS - Tests for KOIOS Pattern Validator BIOS-Q Integration
Version: 1.0.0
Last Updated: 2025-04-01
"""

import os
import json
import pytest
from pathlib import Path
from datetime import datetime
from unittest.mock import patch, MagicMock

from ..interfaces.KOIOS_BIOS_001_integracao_validador import (
    BiosQIntegration,
    ValidationStatus,
    initialize_validation
)

@pytest.fixture
def temp_test_env(tmp_path):
    """Create a temporary test environment"""
    # Create required directories
    config_dir = tmp_path / "config"
    reports_dir = tmp_path / "reports"
    config_dir.mkdir()
    reports_dir.mkdir()

    # Create config file
    config = {
        "integration": {
            "bios_q": {
                "enabled": True,
                "check_on_startup": True,
                "block_on_error": False
            }
        }
    }
    config_path = config_dir / "validator_config.json"
    with open(config_path, "w") as f:
        json.dump(config, f)

    return tmp_path

@pytest.fixture
def bios_integration(temp_test_env):
    """Create a BiosQIntegration instance"""
    return BiosQIntegration(temp_test_env)

def test_initialization(bios_integration):
    """Test BiosQIntegration initialization"""
    assert bios_integration.base_path.exists()
    assert bios_integration.config is not None
    assert bios_integration.config.get("enabled") is True
    assert bios_integration.status_file.parent.exists()

def test_load_config_success(bios_integration):
    """Test successful config loading"""
    config = bios_integration._load_config()
    assert config is not None
    assert config.get("enabled") is True
    assert config.get("check_on_startup") is True
    assert config.get("block_on_error") is False

def test_load_config_missing_file(temp_test_env):
    """Test config loading with missing file"""
    # Remove config file
    config_file = temp_test_env / "config" / "validator_config.json"
    config_file.unlink()
    
    bios = BiosQIntegration(temp_test_env)
    config = bios._load_config()
    assert config == {}

def test_save_and_load_status(bios_integration):
    """Test saving and loading validation status"""
    # Create test status
    status = ValidationStatus(
        success=True,
        errors=0,
        warnings=2,
        timestamp=datetime.now().isoformat(),
        details={"test": "data"},
        report_path="test_report.md"
    )
    
    # Save status
    bios_integration._save_status(status)
    assert bios_integration.status_file.exists()
    
    # Load status
    loaded_status = bios_integration._load_status()
    assert loaded_status is not None
    assert loaded_status.success == status.success
    assert loaded_status.errors == status.errors
    assert loaded_status.warnings == status.warnings
    assert loaded_status.details == status.details
    assert loaded_status.report_path == status.report_path

def test_validate_system_success(bios_integration):
    """Test successful system validation"""
    mock_results = {
        "stats": {
            "violations": {
                "error": 0,
                "warning": 2
            }
        }
    }
    
    with patch("pathlib.Path.exists", return_value=True), \
         patch("builtins.open", MagicMock()), \
         patch("json.dump", MagicMock()), \
         patch("..core.KOIOS_VALIDATE_001_padrao_nomenclatura.PatternValidator") as mock_validator:
        
        # Configure mock validator
        mock_validator_instance = MagicMock()
        mock_validator_instance.validate_tree.return_value = mock_results
        mock_validator_instance.generate_report.return_value = "Test Report"
        mock_validator.return_value = mock_validator_instance
        
        # Run validation
        success, message = bios_integration.validate_system()
        
        assert success is True
        assert "completed" in message
        assert "0 errors" in message
        assert "2 warnings" in message

def test_validate_system_failure(bios_integration):
    """Test system validation with errors"""
    mock_results = {
        "stats": {
            "violations": {
                "error": 2,
                "warning": 1
            }
        }
    }
    
    with patch("pathlib.Path.exists", return_value=True), \
         patch("builtins.open", MagicMock()), \
         patch("json.dump", MagicMock()), \
         patch("..core.KOIOS_VALIDATE_001_padrao_nomenclatura.PatternValidator") as mock_validator:
        
        # Configure mock validator
        mock_validator_instance = MagicMock()
        mock_validator_instance.validate_tree.return_value = mock_results
        mock_validator_instance.generate_report.return_value = "Test Report"
        mock_validator.return_value = mock_validator_instance
        
        # Enable block_on_error
        bios_integration.config["block_on_error"] = True
        
        # Run validation
        success, message = bios_integration.validate_system()
        
        assert success is False
        assert "failed" in message
        assert "2 errors" in message

def test_check_status(bios_integration):
    """Test checking validation status"""
    # Test with no status file
    status = bios_integration.check_status()
    assert status["success"] is False
    assert status["errors"] == -1
    assert status["warnings"] == -1
    assert status["last_check"] is None
    assert status["report"] is None
    
    # Test with status file
    test_status = ValidationStatus(
        success=True,
        errors=0,
        warnings=1,
        timestamp=datetime.now().isoformat(),
        details={},
        report_path="test.md"
    )
    bios_integration._save_status(test_status)
    
    status = bios_integration.check_status()
    assert status["success"] is True
    assert status["errors"] == 0
    assert status["warnings"] == 1
    assert status["last_check"] is not None
    assert status["report"] == "test.md"

def test_is_valid(bios_integration):
    """Test quick validation check"""
    # Test with no status
    assert bios_integration.is_valid() is False
    
    # Test with valid status
    test_status = ValidationStatus(
        success=True,
        errors=0,
        warnings=0,
        timestamp=datetime.now().isoformat(),
        details={},
    )
    bios_integration._save_status(test_status)
    assert bios_integration.is_valid() is True
    
    # Test with invalid status
    test_status.success = False
    bios_integration._save_status(test_status)
    assert bios_integration.is_valid() is False

def test_initialize_validation_success():
    """Test successful initialization"""
    with patch.dict(os.environ, {"EVA_GUARANI_ROOT": "/test/path"}), \
         patch("pathlib.Path.exists", return_value=True), \
         patch("builtins.open", MagicMock()), \
         patch("json.dump", MagicMock()), \
         patch("..interfaces.KOIOS_BIOS_001_integracao_validador.BiosQIntegration") as mock_bios:
        
        # Configure mock
        mock_instance = MagicMock()
        mock_instance.validate_system.return_value = (True, "Success")
        mock_bios.return_value = mock_instance
        
        # Run initialization
        result = initialize_validation()
        assert result == 0

def test_initialize_validation_failure():
    """Test initialization failure"""
    with patch.dict(os.environ, {"EVA_GUARANI_ROOT": "/test/path"}), \
         patch("pathlib.Path.exists", return_value=True), \
         patch("builtins.open", MagicMock()), \
         patch("json.dump", MagicMock()), \
         patch("..interfaces.KOIOS_BIOS_001_integracao_validador.BiosQIntegration") as mock_bios:
        
        # Configure mock
        mock_instance = MagicMock()
        mock_instance.validate_system.return_value = (False, "Error")
        mock_bios.return_value = mock_instance
        
        # Run initialization
        result = initialize_validation()
        assert result == 1

def test_initialize_validation_exception():
    """Test initialization with exception"""
    with patch.dict(os.environ, {"EVA_GUARANI_ROOT": "/test/path"}), \
         patch("..interfaces.KOIOS_BIOS_001_integracao_validador.BiosQIntegration") as mock_bios:
        
        # Configure mock to raise exception
        mock_bios.side_effect = Exception("Test error")
        
        # Run initialization
        result = initialize_validation()
        assert result == 1

# ✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧ 