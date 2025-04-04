#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Update Module Documentation - Script to update specific module documentation
This script updates the module READMEs with usage examples and dependencies.

Version: 1.0.0
Date: 20/03/2025
"""

import os
import sys
import logging
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
        logging.FileHandler(str(log_dir / "module_documentation.log"), encoding="utf-8"),
        logging.StreamHandler(),
    ],
)


def extract_module_info(module_path):
    """Extracts module information through static analysis"""
    info = {"classes": [], "functions": [], "dependencies": set(), "examples": []}

    for py_file in module_path.rglob("*.py"):
        if py_file.name.startswith("test_"):
            continue

        try:
            with open(py_file, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())

                # Extract classes and functions
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        info["classes"].append(
                            {
                                "name": node.name,
                                "file": py_file.relative_to(module_path),
                                "doc": ast.get_docstring(node) or "No documentation",
                            }
                        )
                    elif isinstance(node, ast.FunctionDef):
                        if not node.name.startswith("_"):
                            info["functions"].append(
                                {
                                    "name": node.name,
                                    "file": py_file.relative_to(module_path),
                                    "doc": ast.get_docstring(node) or "No documentation",
                                }
                            )

                    # Extract examples from docstrings
                    if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                        doc = ast.get_docstring(node)
                        if doc and "Example" in doc:
                            example = doc.split("Example")[1].split("\n\n")[0]
                            info["examples"].append({"name": node.name, "example": example.strip()})

                # Extract imports
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for n in node.names:
                            info["dependencies"].add(n.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            info["dependencies"].add(node.module.split(".")[0])

        except Exception as e:
            logging.error(f"Error analyzing {py_file}: {str(e)}")

    return info


def generate_module_readme(module_path, info):
    """Generates README.md for a specific module"""
    module_name = module_path.name
    readme_path = module_path / "README.md"

    content = f"""# Module {module_name}

## Description

{module_name.title()} is a module of the EVA & GUARANI system responsible for [TODO: add specific description].

## Components

### Classes

"""

    if info["classes"]:
        for cls in info["classes"]:
            content += f"#### {cls['name']}\n\n"
            content += f"File: `{cls['file']}`\n\n"
            content += f"{cls['doc']}\n\n"
    else:
        content += "No documented classes.\n\n"

    content += "### Functions\n\n"

    if info["functions"]:
        for func in info["functions"]:
            content += f"#### {func['name']}\n\n"
            content += f"File: `{func['file']}`\n\n"
            content += f"{func['doc']}\n\n"
    else:
        content += "No documented functions.\n\n"

    content += "## Usage Examples\n\n"

    if info["examples"]:
        for example in info["examples"]:
            content += f"### {example['name']}\n\n"
            content += "python\n"
            content += example["example"]
            content += "\n\n\n"
    else:
        content += "python\n"
        content += f"# Basic usage example of the {module_name} module\n"
        content += "from " + module_name + " import *\n\n"
        content += "# TODO: Add specific examples\n"
        content += "\n\n"

    content += "## Dependencies\n\n"

    if info["dependencies"]:
        for dep in sorted(info["dependencies"]):
            content += f"- {dep}\n"
    else:
        content += "No external dependencies.\n\n"

    content += "\n## Integration with Other Modules\n\n"
    content += "TODO: Document how this module integrates with other system components.\n\n"

    content += "## Tests\n\n"
    content += "To run the tests for this module:\n\n"
    content += "bash\n"
    content += f"python -m pytest tests/{module_name}\n"
    content += "\n\n"

    content += "## Contributing\n\n"
    content += "1. Keep the documentation updated\n"
    content += "2. Add tests for new features\n"
    content += "3. Follow the EVA & GUARANI development principles\n\n"

    content += "---\n\n"
    content += "✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧\n"

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)

    logging.info(f"README.md updated for the module {module_name}")


def update_module_docs():
    """Updates the documentation of all modules"""
    module_dirs = [ROOT_DIR / "core", ROOT_DIR / "modules", ROOT_DIR / "integrations"]

    for base_dir in module_dirs:
        if not base_dir.exists():
            continue

        for module_path in base_dir.iterdir():
            if not module_path.is_dir() or module_path.name.startswith(("_", ".")):
                continue

            logging.info(
                f"Processing documentation for module: {module_path.relative_to(ROOT_DIR)}"
            )

            try:
                # Extract module information
                info = extract_module_info(module_path)

                # Generate README
                generate_module_readme(module_path, info)

            except Exception as e:
                logging.error(f"Error processing module {module_path}: {str(e)}")


def main():
    """Main function"""
    logging.info("=== STARTING MODULE DOCUMENTATION UPDATE ===")

    try:
        update_module_docs()
        logging.info("=== MODULE DOCUMENTATION UPDATE COMPLETED ===")

    except Exception as e:
        logging.error(f"Error during documentation update: {str(e)}")
        logging.info("=== MODULE DOCUMENTATION UPDATE INTERRUPTED WITH ERRORS ===")


if __name__ == "__main__":
    main()
