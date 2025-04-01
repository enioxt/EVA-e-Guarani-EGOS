#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Path Corrector
====================================

This script checks and corrects old paths in the bot's code.
"""

import os
import sys
import re
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/path_fix.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("path_fix")

# Directories to be checked
DIRECTORIES_TO_CHECK = ["bot", "modules", "config"]

# Patterns of old paths to be replaced
# Format: (regex_pattern, replacement)
PATH_PATTERNS = [
    (r'["\']C:\\Eva & Guarani["\']', r'"C:\\Eva & Guarani - EGOS"'),
    (r'["\']C:/Eva & Guarani["\']', r'"C:/Eva e Guarani - EGOS"'),
    (r'["\']/Eva & Guarani["\']', r'"/Eva & Guarani - EGOS"'),
    (r'["\']/home/[^/]+/Eva & Guarani["\']', r'"/home/user/Eva & Guarani - EGOS"'),
    (r'import quantum_', r'import quantum.quantum_'),
    (r'from quantum_', r'from quantum.quantum_'),
]

def fix_file(file_path):
    """Corrects old paths in a file."""
    try:
        # Read the file content
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        
        # Check for old paths
        original_content = content
        for pattern, replacement in PATH_PATTERNS:
            content = re.sub(pattern, replacement, content)
        
        # If there were changes, save the file
        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info(f"[FIXED] {file_path}")
            return True
        else:
            logger.debug(f"[OK] {file_path}")
            return False
    except Exception as e:
        logger.error(f"[ERROR] Failed to process {file_path}: {e}")
        return False

def scan_directory(directory):
    """Checks and corrects old paths in all files of a directory."""
    fixed_files = 0
    
    try:
        # Check if the directory exists
        if not os.path.exists(directory):
            logger.warning(f"[WARNING] Directory {directory} not found")
            return 0
        
        # Traverse all files in the directory
        for root, _, files in os.walk(directory):
            for file in files:
                # Check only Python files
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    if fix_file(file_path):
                        fixed_files += 1
    except Exception as e:
        logger.error(f"[ERROR] Failed to check directory {directory}: {e}")
    
    return fixed_files

def fix_import_paths():
    """Corrects import paths in the code."""
    try:
        # Create __init__.py file in important directories
        for directory in ["", "bot", "modules"]:
            init_file = os.path.join(directory, "__init__.py")
            if not os.path.exists(init_file):
                with open(init_file, "w", encoding="utf-8") as f:
                    f.write(f"""#!/usr/bin/env python
# -*- coding: utf-8 -*-

\"\"\"
Package {os.path.basename(directory) or 'EVA & GUARANI'}
\"\"\"
""")
                logger.info(f"[CREATED] {init_file}")
        
        # Create compatibility file for old imports
        compat_file = os.path.join("bot", "compat.py")
        if not os.path.exists(compat_file):
            with open(compat_file, "w", encoding="utf-8") as f:
                f.write("""#!/usr/bin/env python
# -*- coding: utf-8 -*-

\"\"\"
Compatibility module for old imports
\"\"\"

import sys
import os
import importlib

# Add root directory to path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# Import quantum modules
try:
    import quantum
    
    # Create aliases for compatibility
    sys.modules["quantum_master"] = importlib.import_module("quantum.quantum_master")
    sys.modules["quantum_consciousness_backup"] = importlib.import_module("quantum.quantum_consciousness_backup")
    sys.modules["quantum_memory_preservation"] = importlib.import_module("quantum.quantum_memory_preservation")
    sys.modules["quantum_optimizer"] = importlib.import_module("quantum.quantum_optimizer")
except ImportError as e:
    print(f"Error importing quantum modules: {e}")
""")
            logger.info(f"[CREATED] {compat_file}")
        
        # Modify bot's __init__.py file to import compat
        bot_init = os.path.join("bot", "__init__.py")
        if os.path.exists(bot_init):
            with open(bot_init, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            if "import compat" not in content:
                with open(bot_init, "w", encoding="utf-8") as f:
                    f.write("""#!/usr/bin/env python
# -*- coding: utf-8 -*-

\"\"\"
Package EVA & GUARANI Bot
\"\"\"

# Import compatibility module
try:
    from . import compat
except ImportError:
    pass

""" + content)
                logger.info(f"[MODIFIED] {bot_init}")
    except Exception as e:
        logger.error(f"[ERROR] Failed to correct import paths: {e}")

if __name__ == "__main__":
    print("==================================================")
    print("EVA & GUARANI - Path Correction")
    print("==================================================")
    
    try:
        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)
        
        # Correct import paths
        fix_import_paths()
        
        # Check and correct old paths
        total_fixed = 0
        for directory in DIRECTORIES_TO_CHECK:
            fixed = scan_directory(directory)
            total_fixed += fixed
            print(f"Directory {directory}: {fixed} files fixed")
        
        print(f"\n[OK] Total of {total_fixed} files fixed")
        print("You can now start the bot normally.")
    except Exception as e:
        logger.error(f"[ERROR] Failed to correct paths: {e}")
        import traceback
        logger.error(traceback.format_exc())