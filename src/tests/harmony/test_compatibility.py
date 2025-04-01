"""
Tests for the HARMONY compatibility tester implementation.
"""

import os
import platform
import pytest
from pathlib import Path
from typing import Dict, Any

from src.core.harmony.adapter import (
    OperatingSystem,
    PlatformType,
    PlatformInfo,
    CompatibilityTestResult
)
from src.core.harmony.compatibility_tester import (
    HarmonyCompatibilityTester,
    FileSystemTest,
    EncodingTest,
    UITest
)

# ======================================================================
# Fixtures
# ======================================================================

@pytest.fixture
def windows_platform() -> PlatformInfo:
    """Create a Windows platform info fixture."""
    return PlatformInfo(
        os=OperatingSystem.WINDOWS,
        os_version="10.0.19045",
        platform_type=PlatformType.DESKTOP,
        architecture="x86_64",
        python_version=platform.python_version(),
        hostname="test-windows",
        user="test_user"
    )

@pytest.fixture
def linux_platform() -> PlatformInfo:
    """Create a Linux platform info fixture."""
    return PlatformInfo(
        os=OperatingSystem.LINUX,
        os_version="5.15.0",
        platform_type=PlatformType.DESKTOP,
        architecture="x86_64",
        python_version=platform.python_version(),
        hostname="test-linux",
        user="test_user"
    )

@pytest.fixture
def macos_platform() -> PlatformInfo:
    """Create a macOS platform info fixture."""
    return PlatformInfo(
        os=OperatingSystem.MACOS,
        os_version="13.0.0",
        platform_type=PlatformType.DESKTOP,
        architecture="arm64",
        python_version=platform.python_version(),
        hostname="test-macos",
        user="test_user"
    )

@pytest.fixture
def tester() -> HarmonyCompatibilityTester:
    """Create a compatibility tester instance."""
    return HarmonyCompatibilityTester()

# ======================================================================
# Test Cases
# ======================================================================

def test_list_available_tests(tester: HarmonyCompatibilityTester):
    """Test listing available compatibility tests."""
    tests = tester.list_available_tests()
    
    assert len(tests) == 3
    assert any(t["id"] == "fs_compat" for t in tests)
    assert any(t["id"] == "encoding_compat" for t in tests)
    assert any(t["id"] == "ui_compat" for t in tests)

def test_file_system_test_windows(tester: HarmonyCompatibilityTester, windows_platform: PlatformInfo):
    """Test file system compatibility on Windows."""
    result = tester.run_test("fs_compat", windows_platform)
    
    assert isinstance(result, CompatibilityTestResult)
    assert result.test_name == "File System Compatibility"
    assert result.platform == windows_platform
    
    # Windows-specific assertions
    assert result.details["path_separators"]["expected"] == "\\"
    assert not result.details["case_sensitive"]
    assert result.details["max_path_length"]["windows"] == 260

def test_file_system_test_linux(tester: HarmonyCompatibilityTester, linux_platform: PlatformInfo):
    """Test file system compatibility on Linux."""
    result = tester.run_test("fs_compat", linux_platform)
    
    assert isinstance(result, CompatibilityTestResult)
    assert result.test_name == "File System Compatibility"
    assert result.platform == linux_platform
    
    # Linux-specific assertions
    assert result.details["path_separators"]["expected"] == "/"
    assert result.details["case_sensitive"]
    assert result.details["max_path_length"]["posix"] == 4096

def test_encoding_test_windows(tester: HarmonyCompatibilityTester, windows_platform: PlatformInfo):
    """Test encoding compatibility on Windows."""
    result = tester.run_test("encoding_compat", windows_platform)
    
    assert isinstance(result, CompatibilityTestResult)
    assert result.test_name == "Text Encoding Compatibility"
    assert result.platform == windows_platform
    
    # Windows-specific assertions
    assert result.details["utf8_support"]
    assert "cp1252" in result.details["required_encodings"]
    assert "utf-16" in result.details["required_encodings"]

def test_encoding_test_linux(tester: HarmonyCompatibilityTester, linux_platform: PlatformInfo):
    """Test encoding compatibility on Linux."""
    result = tester.run_test("encoding_compat", linux_platform)
    
    assert isinstance(result, CompatibilityTestResult)
    assert result.test_name == "Text Encoding Compatibility"
    assert result.platform == linux_platform
    
    # Linux-specific assertions
    assert result.details["utf8_support"]
    assert "utf-8" in result.details["required_encodings"]
    assert "iso-8859-1" in result.details["required_encodings"]

def test_ui_test_windows(tester: HarmonyCompatibilityTester, windows_platform: PlatformInfo):
    """Test UI compatibility on Windows."""
    result = tester.run_test("ui_compat", windows_platform)
    
    assert isinstance(result, CompatibilityTestResult)
    assert result.test_name == "UI Compatibility"
    assert result.platform == windows_platform
    
    # Windows-specific assertions
    assert "dpi_aware" in result.details
    assert "dark_mode_support" in result.details
    assert result.details["platform_ui_toolkit"] == "Win32"

def test_ui_test_linux(tester: HarmonyCompatibilityTester, linux_platform: PlatformInfo):
    """Test UI compatibility on Linux."""
    result = tester.run_test("ui_compat", linux_platform)
    
    assert isinstance(result, CompatibilityTestResult)
    assert result.test_name == "UI Compatibility"
    assert result.platform == linux_platform
    
    # Linux-specific assertions
    assert "dpi_aware" in result.details
    assert "dark_mode_support" in result.details
    assert result.details["platform_ui_toolkit"] == "GTK"

def test_run_test_suite(tester: HarmonyCompatibilityTester, windows_platform: PlatformInfo, linux_platform: PlatformInfo):
    """Test running a complete test suite."""
    platforms = [windows_platform, linux_platform]
    results = tester.run_test_suite("default", platforms)
    
    assert len(results) == len(platforms) * 3  # 3 tests per platform
    assert all(isinstance(r, CompatibilityTestResult) for r in results)
    
    # Verify we have results for each test and platform
    test_ids = set()
    platform_oss = set()
    
    for result in results:
        test_ids.add(result.test_name)
        platform_oss.add(result.platform.os)
    
    assert len(test_ids) == 3  # All three tests ran
    assert len(platform_oss) == 2  # Both platforms were tested

def test_invalid_test_id(tester: HarmonyCompatibilityTester, windows_platform: PlatformInfo):
    """Test handling of invalid test IDs."""
    with pytest.raises(ValueError, match="Test invalid_test not found"):
        tester.run_test("invalid_test", windows_platform)

def test_test_error_handling(tester: HarmonyCompatibilityTester, windows_platform: PlatformInfo):
    """Test error handling in compatibility tests."""
    # Create a test that raises an exception
    class ErrorTest(FileSystemTest):
        def run(self, target_platform: PlatformInfo, config: Dict[str, Any] = None) -> CompatibilityTestResult:
            raise RuntimeError("Test error")
    
    # Replace the file system test with our error test
    tester.tests["fs_compat"] = ErrorTest()
    
    result = tester.run_test("fs_compat", windows_platform)
    assert not result.passed
    assert "Test failed: Test error" in result.message 