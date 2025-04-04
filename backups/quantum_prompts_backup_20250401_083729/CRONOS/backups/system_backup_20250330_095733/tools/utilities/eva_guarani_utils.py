#!/usr/bin/env python3
python
"""
EVA & GUARANI Utilities
-----------------------

This module provides useful functions for integration with the EVA & GUARANI system.
Import this module for easy access to the main components of the system.

Usage:
    from utils.eva_guarani_utils import setup_quantum_context, auto_documentation

@context: EVA_GUARANI_QUANTUM
"""

import sys
import os
import re
import json
import inspect
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union, Callable

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [EVA&GUARANI] %(levelname)s: %(message)s'
)
logger = logging.getLogger("EVA_GUARANI_UTILS")

# Constants
TERMINOLOGY_PATTERNS = {
    r"\banalise +modular\b|\banalise modular\b|\banálise +modular\b": "análise modular",
    r"\bcartografia +sistemica\b|\bcartografia sistemica\b|\bcartografia +sistêmica\b": "cartografia sistêmica",
    r"\betica +quantica\b|\betica quantica\b|\bética +quântica\b": "ética quântica",
    r"\bpreservacao +evolutiva\b|\bpreservacao evolutiva\b|\bpreservação +evolutiva\b": "preservação evolutiva",
    r"\bentanglement\b": "entanglement",
    r"\bconsciencia +integrada\b|\bconsciencia integrada\b|\bconsciência +integrada\b": "consciência integrada"
}

# Current file path
__current_file = Path(__file__).resolve()

def setup_quantum_context() -> bool:
    """
    Sets up the quantum context for the current module.
    Should be called at the beginning of new scripts to ensure access to the EVA & GUARANI system.

    Returns:
        bool: True if the context was successfully set up, False otherwise

    Example:
        python
        from utils.eva_guarani_utils import setup_quantum_context

        # Set up context at the beginning of the script
        setup_quantum_context()

        # Now you can import components from the EVA & GUARANI system
        from modules.quantum.quantum_knowledge_hub import QuantumKnowledgeHub

    """
    try:
        # Find the project's root directory
        current_dir = Path(os.getcwd())
        root_dir = None

        # Search for the root directory using the current file as reference
        for parent in [__current_file.parent.parent] + list(current_dir.parents):
            if (parent / "docs" / "UNIFIED_DOCUMENTATION.md").exists():
                root_dir = parent
                break
            if (parent / "README.md").exists():
                try:
                    content = (parent / "README.md").read_text(encoding='utf-8')
                    if "EVA & GUARANI" in content:
                        root_dir = parent
                        break
                except:
                    pass

        if not root_dir:
            logger.warning("Could not find the root directory of the EVA & GUARANI project.")
            return False

        # Add to PYTHONPATH if not already present
        root_str = str(root_dir)
        if root_str not in sys.path:
            sys.path.append(root_str)
            logger.info(f"EVA & GUARANI: Root directory '{root_str}' added to PYTHONPATH")

        return True
    except Exception as e:
        logger.error(f"Error setting up quantum context: {e}")
        return False

def get_documentation_path() -> Optional[Path]:
    """
    Returns the path to the unified documentation.

    Returns:
        Path: Path to the unified documentation file or None if not found

    Example:
        python
        from utils.eva_guarani_utils import get_documentation_path

        # Get documentation path
        doc_path = get_documentation_path()

        # Read the documentation
        if doc_path:
            content = doc_path.read_text(encoding='utf-8')
            print(f"Documentation has {len(content)} characters")

    """
    setup_quantum_context()

    # Search for the documentation
    for path in sys.path:
        doc_path = Path(path) / "docs" / "UNIFIED_DOCUMENTATION.md"
        if doc_path.exists():
            return doc_path

    return None

def auto_documentation(name: str = None, description: str = None) -> Callable:
    """
    Decorator to automatically add standard EVA & GUARANI documentation
    to functions and classes. Maintains style and terminology consistency.

    Args:
        name (str, optional): Custom name for the component.
        description (str, optional): Custom description.

    Returns:
        Callable: Configured decorator

    Example:
        python
        from utils.eva_guarani_utils import auto_documentation

        @auto_documentation(description="Processes data using modular analysis")
        def process_data(data):
            # Implementation
            pass

        @auto_documentation()
        class DataProcessor:
            # Implementation
            pass

    """
    def decorator(obj):
        if inspect.isfunction(obj) or inspect.ismethod(obj):
            # Documentation for function/method
            if not obj.__doc__:
                obj.__doc__ = f"""
                {name or obj.__name__}

                {description or 'Implements functionality following the principles of EVA & GUARANI.'}

                This component follows the principles of:
                - Modular Analysis: Independent components with clear interfaces
                - Systemic Cartography: Clear mapping of dependencies
                - Quantum Ethics: Consideration of multidimensional implications

                @context: EVA_GUARANI_QUANTUM
                """
            else:
                # Add context tag
                if "@context:" not in obj.__doc__:
                    obj.__doc__ += "\n\n@context: EVA_GUARANI_QUANTUM"
        elif inspect.isclass(obj):
            # Documentation for class
            if not obj.__doc__:
                obj.__doc__ = f"""
                {name or obj.__name__}

                {description or 'Implements component following the principles of EVA & GUARANI.'}

                This class follows the principles of:
                - Modular Analysis: Independent components with clear interfaces
                - Systemic Cartography: Clear mapping of dependencies
                - Quantum Ethics: Consideration of multidimensional implications

                @context: EVA_GUARANI_QUANTUM
                """
            else:
                # Add context tag
                if "@context:" not in obj.__doc__:
                    obj.__doc__ += "\n\n@context: EVA_GUARANI_QUANTUM"

        return obj

    return decorator

def ensure_terminology_consistency(text: str) -> str:
    """
    Ensures terminology consistency in texts according to EVA & GUARANI standards.

    Args:
        text (str): Text to be checked/corrected

    Returns:
        str: Text with consistent terminology

    Example:
        python
        from utils.eva_guarani_utils import ensure_terminology_consistency

        # Correct terminology in text
        comment = "Este módulo implementa analise modular e preservacao evolutiva"
        fixed_comment = ensure_terminology_consistency(comment)
        print(fixed_comment)  # "Este módulo implementa análise modular e preservação evolutiva"

    """
    result = text
    for pattern, replacement in TERMINOLOGY_PATTERNS.items():
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    return result

def import_quantum_components() -> Dict[str, Any]:
    """
    Dynamically imports the main components of the EVA & GUARANI quantum system.

    Returns:
        Dict[str, Any]: Dictionary with imported components

    Example:
        python
        from utils.eva_guarani_utils import import_quantum_components

        # Import components
        components = import_quantum_components()

        # Use components
        if 'QuantumKnowledgeHub' in components:
            hub = components['QuantumKnowledgeHub']()
            result = hub.query("How to implement modular analysis?")

    """
    setup_quantum_context()

    # Components we will try to import
    components = {}

    # List of modules to import (path, class)
    modules_to_import = [
        ("modules.quantum.quantum_knowledge_hub", "QuantumKnowledgeHub"),
        ("modules.integration.integration_bridge", "IntegrationBridge"),
        ("modules.mycelium.mycelium_network", "MyceliumNetwork")
    ]

    for module_path, class_name in modules_to_import:
        try:
            # Try absolute import
            module = __import__(module_path, fromlist=[class_name])
            components[class_name] = getattr(module, class_name)
        except (ImportError, AttributeError) as e:
            logger.debug(f"Could not import {class_name} from {module_path}: {e}")

            # Try to find the module in alternative locations
            try:
                # Check in each path in PYTHONPATH
                for path in sys.path:
                    path_obj = Path(path)
                    for root, dirs, files in os.walk(path_obj):
                        for file in files:
                            if file == f"{class_name.lower()}.py" or file == f"{module_path.split('.')[-1]}.py":
                                file_path = Path(root) / file
                                spec = importlib.util.spec_from_file_location(class_name, file_path)
                                if spec and spec.loader:
                                    module = importlib.util.module_from_spec(spec)
                                    spec.loader.exec_module(module)
                                    if hasattr(module, class_name):
                                        components[class_name] = getattr(module, class_name)
                                        break
            except Exception as e:
                logger.debug(f"Error importing {class_name} from alternative locations: {e}")

    return components

class DocumentationGenerator:
    """
    Automatic documentation generator following EVA & GUARANI standards.

    This class provides methods to generate standardized documentation for
    modules, functions, and classes, following the principles of modular analysis
    and systemic cartography.

    Example:
        python
        from utils.eva_guarani_utils import DocumentationGenerator

        # Create documentation generator
        doc_gen = DocumentationGenerator()

        # Generate documentation for a module
        module_doc = doc_gen.generate_module_doc("my_module", "Processes data using quantum ethics")

        # Insert at the beginning of the file
        with open("my_module.py", "r+") as f:
            content = f.read()
            f.seek(0)
            f.write(module_doc + "\n\n" + content)

    """

    def __init__(self):
        """Initializes the documentation generator."""
        setup_quantum_context()

    def generate_module_doc(self, module_name: str, description: str) -> str:
        """
        Generates documentation for a Python module.

        Args:
            module_name (str): Module name
            description (str): Module description

        Returns:
            str: Formatted documentation
        """
        return f'''"""
{module_name}
{"=" * len(module_name)}

{description}

This module follows the principles of EVA & GUARANI:
- Modular Analysis: Independent components with clear interfaces
- Systemic Cartography: Clear mapping of dependencies
- Quantum Ethics: Consideration of multidimensional implications
- Evolutionary Preservation: Maintaining integrity during transformations

References:
- Unified Documentation: docs/UNIFIED_DOCUMENTATION.md

@context: EVA_GUARANI_QUANTUM
"""'''

    def generate_class_doc(self, class_name: str, description: str) -> str:
        """
        Generates documentation for a Python class.

        Args:
            class_name (str): Class name
            description (str): Class description

        Returns:
            str: Formatted documentation
        """
        return f'''"""
{description}

This class follows the principles of EVA & GUARANI:
- Modular Analysis: Encapsulation and well-defined interfaces
- Systemic Cartography: Clarity in relationships with other components
- Quantum Ethics: Consideration of multidimensional implications

@context: EVA_GUARANI_QUANTUM
"""'''

    def generate_function_doc(self, func_name: str, description: str,
                             params: Dict[str, str] = None,
                             returns: str = None) -> str:
        """
        Generates documentation for a Python function.

        Args:
            func_name (str): Function name
            description (str): Function description
            params (Dict[str, str], optional): Dictionary of parameters and their descriptions
            returns (str, optional): Description of the return value

        Returns:
            str: Formatted documentation
        """
        doc = f'"""\n{description}\n\n'

        if params:
            doc += "Args:\n"
            for param, desc in params.items():
                doc += f"    {param} ({desc.split(':')[0] if ':' in desc else 'Any'}): {desc.split(':')[1] if ':' in desc else desc}\n"
            doc += "\n"

        if returns:
            doc += f"Returns:\n    {returns.split(':')[0] if ':' in returns else 'Any'}: {returns.split(':')[1] if ':' in returns else returns}\n\n"

        doc += "@context: EVA_GUARANI_QUANTUM\n\"\"\""
        return doc

    def generate_markdown_doc(self, title: str, description: str) -> str:
        """
        Generates documentation in Markdown format.

        Args:
            title (str): Document title
            description (str): Main description/content

        Returns:
            str: Formatted Markdown documentation
        """
        return f'''# {title}

> "At the intersection of modular analysis, systemic cartography, and quantum ethics."

## Context

{description}

## Content

- [Introduction](#introduction)
- [Implementation](#implementation)
- [Connections](#connections)
- [Conclusion](#conclusion)

## Introduction

[Describe the purpose and context]

## Implementation

[Technical details of the implementation]

## Connections

This document relates to:
- [Quantum Knowledge System](../docs/UNIFIED_DOCUMENTATION.md#2-quantum-knowledge-system)
- [Technical Architecture](../docs/UNIFIED_DOCUMENTATION.md#7-technical-architecture)

## Conclusion

[Summary and next steps]

---

✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
'''

def add_quantum_context_to_file(file_path: str) -> bool:
    """
    Adds EVA & GUARANI quantum context to an existing file.

    Args:
        file_path (str): Path to the file to be modified

    Returns:
        bool: True if the file was successfully modified, False otherwise

    Example:
        python
        from utils.eva_guarani_utils import add_quantum_context_to_file

        # Add quantum context to a file
        success = add_quantum_context_to_file("my_script.py")

    """
    try:
        file = Path(file_path)
        if not file.exists():
            logger.error(f"File {file_path} does not exist")
            return False

        # Determine file type
        file_type = file.suffix.lower()

        # Read current content
        content = file.read_text(encoding='utf-8')

        # Check if it already has quantum context
        if "@context: EVA_GUARANI_QUANTUM" in content:
            logger.info(f"File {file_path} already has quantum context")
            return True

        # Create documentation generator
        doc_gen = DocumentationGenerator()

        # Add context based on file type
        if file_type == '.py':
            # For Python files
            module_name = file.stem
            module_doc = doc_gen.generate_module_doc(module_name,
                                                    f"Module {module_name} integrated into the EVA & GUARANI system")

            # Add at the beginning
            if content.startswith('"""') or content.startswith("'''"):
                # Already has docstring, add context
                end_of_docstring = content.find('"""', 3) if content.startswith('"""') else content.find("'''", 3)
                if end_of_docstring > 0:
                    new_content = content[:end_of_docstring] + "\n\n@context: EVA_GUARANI_QUANTUM" + content[end_of_docstring:]
                else:
                    new_content = module_doc + "\n\n" + content
            else:
                new_content = module_doc + "\n\n" + content

        elif file_type == '.md':
            # For Markdown files
            title = file.stem.replace('_', ' ').title()
            existing_title = re.search(r'^# +(.+)$', content, re.MULTILINE)
            if existing_title:
                title = existing_title.group(1)

            if not content.strip():
                # Empty file, generate complete document
                new_content = doc_gen.generate_markdown_doc(title, "This document is part of the EVA & GUARANI system")
            else:
                # Add context comment at the end
                if not content.endswith("\n\n✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"):
                    new_content = content + "\n\n---\n\n✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧"
                else:
                    logger.info(f"File {file_path} already has EVA & GUARANI signature")
                    return True

        elif file_type in ['.js', '.ts']:
            # For JavaScript/TypeScript files
            if not content.strip():
                # Empty file
                new_content = f'''/**
 * @module {file.stem}
 * @description Module {file.stem} integrated into the EVA & GUARANI system
 *
 * This module follows the principles of EVA & GUARANI:
 * - Modular Analysis: Independent components with clear interfaces
 * - Systemic Cartography: Clear mapping of dependencies
 * - Quantum Ethics: Consideration of multidimensional implications
 *
 * @context EVA_GUARANI_QUANTUM
 */

'''
            else:
                # Check if it already has JSDoc comment
                if content.lstrip().startswith('/**'):
                    end_of_comment = content.find('*/', 3)
                    if end_of_comment > 0:
                        if '@context' not in content[:end_of_comment]:
                            new_content = content[:end_of_comment] + " * @context EVA_GUARANI_QUANTUM\n " + content[end_of_comment:]
                        else:
                            logger.info(f"File {file_path} already has quantum context in JSDoc")
                            return True
                    else:
                        new_content = f'''/**
 * @module {
