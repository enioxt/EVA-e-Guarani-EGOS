#!/usr/bin/env python3
"""
Test suite for BIOS-Q initialization module
"""

import os
import json
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open
from ..core.initialize import BiosQ

@pytest.fixture
def bios_instance():
    """Create a BIOS-Q instance for testing"""
    return BiosQ()

@pytest.fixture
def mock_config():
    """Create a mock configuration for testing"""
    return {
        "system": {
            "name": "EVA & GUARANI",
            "version": "8.1",
            "language": "en",
            "debug_mode": False,
            "log_level": "INFO"
        }
    }

def test_bios_initialization(bios_instance):
    """Test BIOS-Q instance initialization"""
    assert isinstance(bios_instance, BiosQ)
    assert bios_instance.config == {}
    assert bios_instance.logger is not None

def test_logging_setup(bios_instance):
    """Test logging configuration"""
    logger = bios_instance.logger
    assert logger.name == "BIOS-Q"
    assert logger.level == 20  # INFO level
    assert len(logger.handlers) > 0

@patch("pathlib.Path.exists")
@patch("builtins.open", new_callable=mock_open)
def test_load_config_success(mock_file, mock_exists, bios_instance, mock_config):
    """Test successful configuration loading"""
    mock_exists.return_value = True
    mock_file.return_value.__enter__.return_value.read.return_value = json.dumps(mock_config)
    
    config = bios_instance.load_config()
    assert config == mock_config
    assert bios_instance.config == mock_config

@patch("pathlib.Path.exists")
def test_load_config_missing(mock_exists, bios_instance):
    """Test behavior when configuration file is missing"""
    mock_exists.return_value = False
    
    config = bios_instance.load_config()
    assert config == {}
    assert bios_instance.config == {}

@patch("pathlib.Path.mkdir")
def test_initialize_directories_success(mock_mkdir, bios_instance):
    """Test successful directory initialization"""
    result = bios_instance.initialize_directories()
    assert result is True
    assert mock_mkdir.call_count > 0

@patch("pathlib.Path.mkdir")
def test_initialize_directories_failure(mock_mkdir, bios_instance):
    """Test directory initialization failure"""
    mock_mkdir.side_effect = Exception("Failed to create directory")
    result = bios_instance.initialize_directories()
    assert result is False

def test_verify_environment_python_version():
    """Test Python version verification"""
    with patch("sys.version_info", (3, 10)):
        bios = BiosQ()
        assert bios.verify_environment() is False

    with patch("sys.version_info", (3, 11)):
        bios = BiosQ()
        with patch("pkg_resources.require") as mock_require:
            mock_require.return_value = None
            assert bios.verify_environment() is True

@patch("pkg_resources.require")
def test_verify_environment_packages(mock_require, bios_instance):
    """Test package verification"""
    # Test successful package verification
    mock_require.return_value = None
    assert bios_instance.verify_environment() is True
    
    # Test package version conflict
    mock_require.side_effect = Exception("Package conflict")
    assert bios_instance.verify_environment() is False

def test_initialize_system_success(bios_instance):
    """Test successful system initialization"""
    with patch.multiple(bios_instance,
                       load_config=lambda: True,
                       initialize_directories=lambda: True,
                       verify_environment=lambda: True):
        assert bios_instance.initialize_system() is True

def test_initialize_system_failure_config(bios_instance):
    """Test system initialization failure due to config"""
    with patch.multiple(bios_instance,
                       load_config=lambda: False,
                       initialize_directories=lambda: True,
                       verify_environment=lambda: True):
        assert bios_instance.initialize_system() is False

def test_initialize_system_failure_directories(bios_instance):
    """Test system initialization failure due to directories"""
    with patch.multiple(bios_instance,
                       load_config=lambda: True,
                       initialize_directories=lambda: False,
                       verify_environment=lambda: True):
        assert bios_instance.initialize_system() is False

def test_initialize_system_failure_environment(bios_instance):
    """Test system initialization failure due to environment"""
    with patch.multiple(bios_instance,
                       load_config=lambda: True,
                       initialize_directories=lambda: True,
                       verify_environment=lambda: False):
        assert bios_instance.initialize_system() is False 