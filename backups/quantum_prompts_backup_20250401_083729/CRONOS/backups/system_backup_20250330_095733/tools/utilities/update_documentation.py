#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Update Documentation - Script to update the system documentation
This script updates the documentation to reflect the new system structure.

Version: 1.0.0
Date: 20/03/2025
"""

import os
import sys
import logging
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
        logging.FileHandler(str(log_dir / "documentation_update.log"), encoding="utf-8"),
        logging.StreamHandler()
    ]
)

def scan_directory_structure():
    """Scans the project's directory structure"""
    structure = {}
    
    for category in ["core", "modules", "integrations", "tools", "docs", "tests", "ui", "data"]:
        category_path = ROOT_DIR / category
        if not category_path.exists():
            continue
            
        structure[category] = {}
        for item in category_path.glob("*"):
            if item.is_dir() and not item.name.startswith((".", "__")):
                structure[category][item.name] = []
                for subitem in item.glob("*"):
                    if subitem.is_dir() and not subitem.name.startswith((".", "__")):
                        structure[category][item.name].append(subitem.name)
    
    return structure

def update_main_readme():
    """Updates the main README.md with the new structure"""
    readme_path = ROOT_DIR / "README.md"
    structure = scan_directory_structure()
    
    content = f"""# EVA & GUARANI

Modular Analysis System, Systemic Cartography and Quantum Ethics

*Version 8.0.0 - {datetime.now().strftime('%d/%m/%Y')}*

## 🌟 Overview

EVA & GUARANI is an integrated system that transcends dimensions of thought with methodological precision and unconditional love, integrating advanced tools for knowledge visualization and evolutionary preservation.

## 📊 Project Status

- **Version**: 8.0.0
- **State**: In Active Development
- **Last Update**: {datetime.now().strftime('%d/%m/%Y')}

## 🏗️ System Structure

### Main Components

"""
    
    # Add core structure
    if "core" in structure:
        content += "#### [`/core`](/core) - Essential Components\n\n"
        for module, submodules in structure["core"].items():
            content += f"- **{module}**"
            if submodules:
                content += "\n"
                for submodule in sorted(submodules):
                    content += f"  - {submodule}\n"
            else:
                content += "\n"
        content += "\n"
    
    # Add modules structure
    if "modules" in structure:
        content += "#### [`/modules`](/modules) - Functional Modules\n\n"
        for module, submodules in structure["modules"].items():
            content += f"- **{module}**"
            if submodules:
                content += "\n"
                for submodule in sorted(submodules):
                    content += f"  - {submodule}\n"
            else:
                content += "\n"
        content += "\n"
    
    # Add integrations structure
    if "integrations" in structure:
        content += "#### [`/integrations`](/integrations) - Integrations\n\n"
        for integration, submodules in structure["integrations"].items():
            content += f"- **{integration}**"
            if submodules:
                content += "\n"
                for submodule in sorted(submodules):
                    content += f"  - {submodule}\n"
            else:
                content += "\n"
        content += "\n"
    
    # Add tools structure
    if "tools" in structure:
        content += "#### [`/tools`](/tools) - Tools\n\n"
        for tool, submodules in structure["tools"].items():
            content += f"- **{tool}**"
            if submodules:
                content += "\n"
                for submodule in sorted(submodules):
                    content += f"  - {submodule}\n"
            else:
                content += "\n"
        content += "\n"
    
    # Add additional sections
    content += """## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- Dependencies listed in `requirements.txt`

### Installation

bash
# Clone the repository
git clone https://github.com/your-username/eva-guarani.git

# Enter the directory
cd eva-guarani

# Install Python dependencies
pip install -r requirements.txt

# Install Node dependencies (if applicable)
npm install


## 📖 Documentation

Detailed documentation is available in the [`/docs`](/docs) directory and includes:

- User guides
- Developer documentation
- API references
- Tutorials

## 🛠️ Development

### Development Principles

1. **Universal possibility of redemption** - Every being and every code deserves infinite chances
2. **Compassionate temporality** - Evolution occurs in the necessary time
3. **Sacred privacy** - Absolute data protection
4. **Universal accessibility** - Total inclusion
5. **Unconditional love** - Quantum basis of all interactions
6. **Reciprocal trust** - Symbiotic relationship between system and user
7. **Integrated ethics** - Ethics as fundamental DNA
8. **Conscious modularity** - Understanding of parts and whole
9. **Systemic cartography** - Precise mapping of connections
10. **Evolutionary preservation** - Quantum backup that maintains essence

## 📄 License

This project is licensed under the terms of the MIT license. See the `LICENSE` file for more details.

---

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
"""
    
    # Save updated README
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    logging.info("Main README.md updated successfully")

def create_module_readmes():
    """Creates or updates README.md for each main module"""
    structure = scan_directory_structure()
    
    for category, modules in structure.items():
        category_path = ROOT_DIR / category
        
        # Create README for the category
        category_readme = category_path / "README.md"
        with open(category_readme, "w", encoding="utf-8") as f:
            f.write(f"# {category.title()}\n\n")
            f.write(f"{category.title()} Components of the EVA & GUARANI System\n\n")
            
            for module, submodules in modules.items():
                f.write(f"## {module}\n\n")
                if submodules:
                    for submodule in sorted(submodules):
                        f.write(f"- {submodule}\n")
                f.write("\n")
        
        # Create README for each module
        for module in modules:
            module_path = category_path / module
            module_readme = module_path / "README.md"
            
            if not module_readme.exists():
                with open(module_readme, "w", encoding="utf-8") as f:
                    f.write(f"# {module.title()}\n\n")
                    f.write(f"{module.title()} Module of the EVA & GUARANI System\n\n")
                    
                    if modules[module]:
                        f.write("## Components\n\n")
                        for submodule in sorted(modules[module]):
                            f.write(f"- {submodule}\n")
                    
                    f.write("\n## Description\n\n")
                    f.write("TODO: Add detailed module description\n\n")
                    
                    f.write("## Usage\n\n")
                    f.write("TODO: Add usage examples\n\n")
                    
                    f.write("## Dependencies\n\n")
                    f.write("TODO: List specific dependencies\n\n")
                    
                    f.write("---\n\n")
                    f.write("✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧\n")

def main():
    """Main function"""
    logging.info("=== STARTING DOCUMENTATION UPDATE ===")
    
    try:
        # Update main README
        update_main_readme()
        
        # Create/update module READMEs
        create_module_readmes()
        
        logging.info("=== DOCUMENTATION UPDATE COMPLETED ===")
        
    except Exception as e:
        logging.error(f"Error during documentation update: {str(e)}")
        logging.info("=== DOCUMENTATION UPDATE INTERRUPTED WITH ERRORS ===")

if __name__ == "__main__":
    main()