#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Run Tests - Script to execute tests and validate functionalities
This script runs unit and integration tests, generating detailed reports.

Version: 1.0.0
Date: 20/03/2025
"""

import os
import sys
import logging
import subprocess
import json
from pathlib import Path
from datetime import datetime
import pytest
import coverage

# Project root directory
ROOT_DIR = Path(__file__).parent.parent.parent.absolute()

# Logging configuration
log_dir = ROOT_DIR / "data" / "logs" / "system"
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(str(log_dir / "test_execution.log"), encoding="utf-8"),
        logging.StreamHandler()
    ]
)

def setup_test_environment():
    """Sets up the test environment"""
    # Create directory for reports
    report_dir = ROOT_DIR / "docs" / "test_reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    
    # Configure code coverage
    cov = coverage.Coverage(
        branch=True,
        source=[str(ROOT_DIR / d) for d in ['core', 'modules', 'integrations']],
        omit=['**/test_*.py', '**/conftest.py']
    )
    
    return report_dir, cov

def find_test_files():
    """Finds all test files in the project"""
    test_files = []
    for path in ROOT_DIR.rglob("test_*.py"):
        if not any(x.startswith('.') for x in path.parts) and 'venv' not in path.parts:
            test_files.append(path)
    return test_files

def run_unit_tests(cov):
    """Runs unit tests with coverage"""
    logging.info("Running unit tests...")
    
    # Start coverage
    cov.start()
    
    # Configure pytest arguments
    test_dir = ROOT_DIR / 'tests'
    if not test_dir.exists():
        logging.warning("Test directory not found")
        return False
        
    report_dir = ROOT_DIR / 'docs' / 'test_reports'
    report_dir.mkdir(parents=True, exist_ok=True)
    
    pytest_args = [
        str(test_dir),
        '--verbose',
        '--capture=no',
        '--junit-xml=' + str(report_dir / 'unit_tests.xml'),
        '--html=' + str(report_dir / 'unit_tests.html')
    ]
    
    # Run tests
    result = pytest.main(pytest_args)
    
    # Stop coverage
    cov.stop()
    cov.save()
    
    return result == pytest.ExitCode.OK

def run_integration_tests():
    """Runs integration tests"""
    logging.info("Running integration tests...")
    
    test_dir = ROOT_DIR / 'tests' / 'integration'
    if not test_dir.exists():
        logging.warning("Integration test directory not found")
        return False
        
    report_dir = ROOT_DIR / 'docs' / 'test_reports'
    report_dir.mkdir(parents=True, exist_ok=True)
    
    # Configure pytest arguments
    pytest_args = [
        str(test_dir),
        '--verbose',
        '--capture=no',
        '-m', 'integration',
        '--junit-xml=' + str(report_dir / 'integration_tests.xml'),
        '--html=' + str(report_dir / 'integration_tests.html')
    ]
    
    # Run tests
    result = pytest.main(pytest_args)
    
    return result == pytest.ExitCode.OK

def generate_coverage_report(cov, report_dir):
    """Generates code coverage report"""
    logging.info("Generating coverage report...")
    
    # Generate HTML report
    cov.html_report(directory=str(report_dir / 'coverage'))
    
    # Generate JSON report
    cov.json_report(outfile=str(report_dir / 'coverage.json'))
    
    return True

def analyze_test_results(report_dir):
    """Analyzes test results and generates report"""
    report_file = report_dir / f"test_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    try:
        coverage_data = None
        coverage_file = report_dir / 'coverage.json'
        
        if coverage_file.exists():
            with open(coverage_file, 'r', encoding='utf-8') as f:
                coverage_data = json.load(f)
        
        # Generate report
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# Test Execution Report\n\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            if coverage_data:
                f.write("## Coverage Summary\n\n")
                f.write(f"- Total Coverage: {coverage_data['totals']['percent_covered']:.2f}%\n")
                f.write(f"- Tested Lines: {coverage_data['totals']['covered_lines']}\n")
                f.write(f"- Untested Lines: {coverage_data['totals']['missing_lines']}\n\n")
                
                f.write("## Details by Module\n\n")
                for file_path, data in coverage_data['files'].items():
                    rel_path = Path(file_path).relative_to(ROOT_DIR)
                    f.write(f"### {rel_path}\n\n")
                    f.write(f"- Coverage: {data['summary']['percent_covered']:.2f}%\n")
                    f.write(f"- Tested Lines: {data['summary']['covered_lines']}\n")
                    f.write(f"- Untested Lines: {data['summary']['missing_lines']}\n\n")
            else:
                f.write("## Warning\n\n")
                f.write("Coverage data not available.\n\n")
            
            f.write("## Recommendations\n\n")
            f.write("1. Implement more unit tests\n")
            f.write("2. Add integration tests\n")
            f.write("3. Configure CI/CD for automatic test execution\n")
            
            f.write("\n---\n\n")
            f.write("✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧\n")
        
        logging.info(f"Test report generated: {report_file}")
        return True
        
    except Exception as e:
        logging.error(f"Error generating test report: {str(e)}")
        return False

def main():
    """Main function"""
    logging.info("=== STARTING TEST EXECUTION ===")
    
    try:
        # Set up environment
        report_dir, cov = setup_test_environment()
        
        # Run unit tests
        unit_success = run_unit_tests(cov)
        
        # Run integration tests
        integration_success = run_integration_tests()
        
        # Generate coverage report
        coverage_success = generate_coverage_report(cov, report_dir)
        
        # Analyze results
        analysis_success = analyze_test_results(report_dir)
        
        if unit_success and integration_success and coverage_success and analysis_success:
            logging.info("=== TEST EXECUTION COMPLETED SUCCESSFULLY ===")
        else:
            logging.warning("=== TEST EXECUTION COMPLETED WITH WARNINGS ===")
        
    except Exception as e:
        logging.error(f"Error during test execution: {str(e)}")
        logging.info("=== TEST EXECUTION INTERRUPTED WITH ERRORS ===")

if __name__ == "__main__":
    main()