#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Verify Integrations - Script to verify integrations between modules
This script analyzes and validates the integrations between different system components.

Version: 1.0.0
Date: 20/03/2025
"""

import os
import sys
import logging
import importlib
import ast
from pathlib import Path
from datetime import datetime

# Project root directory
ROOT_DIR = Path(__file__).parent.parent.parent.absolute()

# Logging configuration
log_dir = ROOT_DIR / "data" / "logs" / "system"
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(str(log_dir / "integration_verification.log"), encoding="utf-8"),
        logging.StreamHandler(),
    ],
)


class DependencyAnalyzer(ast.NodeVisitor):
    """Dependency analyzer for Python files"""

    def __init__(self):
        self.imports = []
        self.from_imports = []

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append(alias.name)

    def visit_ImportFrom(self, node):
        if node.module:
            for alias in node.names:
                self.from_imports.append(f"{node.module}.{alias.name}")


def analyze_file_dependencies(file_path):
    """Analyzes the dependencies of a Python file"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
            analyzer = DependencyAnalyzer()
            analyzer.visit(tree)
            return analyzer.imports + analyzer.from_imports
    except Exception as e:
        logging.error(f"Error analyzing {file_path}: {str(e)}")
        return []


def find_python_files():
    """Finds all Python files in the project"""
    python_files = []
    for path in ROOT_DIR.rglob("*.py"):
        if not any(x.startswith(".") for x in path.parts) and "venv" not in path.parts:
            python_files.append(path)
    return python_files


def analyze_module_dependencies():
    """Analyzes dependencies between modules"""
    files = find_python_files()
    dependencies = {}

    for file in files:
        rel_path = file.relative_to(ROOT_DIR)
        deps = analyze_file_dependencies(file)
        dependencies[str(rel_path)] = deps

    return dependencies


def verify_imports(dependencies):
    """Verifies if the imports are valid"""
    issues = []

    for file, deps in dependencies.items():
        for dep in deps:
            if dep.startswith(("core", "modules", "integrations")):
                module_path = ROOT_DIR / dep.replace(".", "/")
                py_file = module_path.with_suffix(".py")
                init_file = module_path / "__init__.py"

                if not py_file.exists() and not init_file.exists():
                    issues.append((file, dep))

    return issues


def analyze_integration_patterns():
    """Analyzes common integration patterns"""
    patterns = {
        "api_calls": [],
        "event_handlers": [],
        "database_access": [],
        "file_operations": [],
        "external_services": [],
    }

    for file in find_python_files():
        try:
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()

                # Search for integration patterns
                if "requests." in content or "aiohttp." in content:
                    patterns["api_calls"].append(file)
                if "on_event" in content or "event_handler" in content:
                    patterns["event_handlers"].append(file)
                if "database." in content or "models." in content:
                    patterns["database_access"].append(file)
                if "open(" in content or "with open" in content:
                    patterns["file_operations"].append(file)
                if any(
                    service in content
                    for service in ["redis", "kafka", "rabbitmq", "elasticsearch"]
                ):
                    patterns["external_services"].append(file)
        except Exception as e:
            logging.error(f"Error analyzing patterns in {file}: {str(e)}")

    return patterns


def generate_integration_report(dependencies, issues, patterns):
    """Generates integration report"""
    report_dir = ROOT_DIR / "docs" / "integration_reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    report_file = report_dir / f"integration_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

    with open(report_file, "w", encoding="utf-8") as f:
        f.write("# Integration Analysis Report\n\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        # Issues found
        f.write("## Import Issues\n\n")
        if issues:
            for file, dep in issues:
                f.write(f"- File `{file}` tries to import `{dep}` (not found)\n")
        else:
            f.write("No import issues found.\n")

        # Integration patterns
        f.write("\n## Integration Patterns\n\n")
        for pattern, files in patterns.items():
            f.write(f"\n### {pattern.replace('_', ' ').title()}\n\n")
            for file in files:
                f.write(f"- `{file.relative_to(ROOT_DIR)}`\n")

        # Dependency map
        f.write("\n## Dependency Map\n\n")
        for file, deps in dependencies.items():
            if deps:
                f.write(f"\n### `{file}`\n\n")
                for dep in sorted(deps):
                    f.write(f"- {dep}\n")

        # Recommendations
        f.write("\n## Recommendations\n\n")

        if issues:
            f.write("### Necessary Corrections\n\n")
            for file, dep in issues:
                f.write(f"- [ ] Fix import of `{dep}` in `{file}`\n")

        f.write("\n### Suggested Improvements\n\n")
        f.write("- [ ] Document integration interfaces\n")
        f.write("- [ ] Implement integration tests\n")
        f.write("- [ ] Add logging in critical points\n")
        f.write("- [ ] Implement error handling\n")

        f.write("\n---\n\n")
        f.write("✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧\n")

    logging.info(f"Integration report generated: {report_file}")
    return report_file


def main():
    """Main function"""
    logging.info("=== STARTING INTEGRATION VERIFICATION ===")

    try:
        # Analyze dependencies
        logging.info("Analyzing dependencies between modules...")
        dependencies = analyze_module_dependencies()

        # Verify imports
        logging.info("Verifying imports...")
        issues = verify_imports(dependencies)

        # Analyze integration patterns
        logging.info("Analyzing integration patterns...")
        patterns = analyze_integration_patterns()

        # Generate report
        report = generate_integration_report(dependencies, issues, patterns)

        if issues:
            logging.warning(f"Found {len(issues)} import issues")
        else:
            logging.info("No import issues found")

        logging.info("=== INTEGRATION VERIFICATION COMPLETED ===")

    except Exception as e:
        logging.error(f"Error during integration verification: {str(e)}")
        logging.info("=== INTEGRATION VERIFICATION INTERRUPTED WITH ERRORS ===")


if __name__ == "__main__":
    main()
