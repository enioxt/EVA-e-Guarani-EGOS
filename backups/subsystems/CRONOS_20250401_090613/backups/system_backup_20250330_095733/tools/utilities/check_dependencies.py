#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Dependency Checker
This script checks if all necessary dependencies are installed.
"""

import os
import sys
import subprocess
import importlib.util
import platform
from colorama import init, Fore, Style

# Initialize colorama for color support in the terminal
init()

# List of necessary dependencies
DEPENDENCIES = [
    {"name": "python-telegram-bot", "import_name": "telegram", "version": "13.0"},
    {"name": "psutil", "import_name": "psutil", "version": "5.8.0"},
    {"name": "colorama", "import_name": "colorama", "version": "0.4.4"},
    {"name": "requests", "import_name": "requests", "version": "2.25.1"},
    {"name": "pillow", "import_name": "PIL", "version": "8.0.0"},
    {"name": "numpy", "import_name": "numpy", "version": "1.19.0"},
    {"name": "openai", "import_name": "openai", "version": "0.27.0"},
    {"name": "tenacity", "import_name": "tenacity", "version": "8.0.0"}
]

# Optional dependencies
OPTIONAL_DEPENDENCIES = [
    {"name": "matplotlib", "import_name": "matplotlib", "version": "3.4.0", "description": "Graph generation"},
    {"name": "pandas", "import_name": "pandas", "version": "1.3.0", "description": "Data analysis"},
    {"name": "scikit-learn", "import_name": "sklearn", "version": "0.24.0", "description": "Machine learning algorithms"},
    {"name": "transformers", "import_name": "transformers", "version": "4.5.0", "description": "Advanced language models"}
]

def check_python_version():
    """Checks if the Python version is compatible."""
    required_version = (3, 8)
    current_version = sys.version_info
    
    if current_version < required_version:
        print(f"{Fore.RED}[ERROR] Incompatible Python version: {sys.version}")
        print(f"       Python {required_version[0]}.{required_version[1]} or higher is required.{Style.RESET_ALL}")
        return False
    else:
        print(f"{Fore.GREEN}[OK] Python version: {sys.version.split()[0]}{Style.RESET_ALL}")
        return True

def check_dependency(dependency):
    """Checks if a dependency is installed."""
    name = dependency["name"]
    import_name = dependency["import_name"]
    required_version = dependency["version"]
    
    try:
        # Check if the module can be imported
        spec = importlib.util.find_spec(import_name)
        if spec is None:
            return False, f"{Fore.RED}[MISSING] {name} is not installed{Style.RESET_ALL}"
        
        # Import the module to check the version
        module = importlib.import_module(import_name)
        version = getattr(module, "__version__", "Unknown")
        
        return True, f"{Fore.GREEN}[OK] {name} (version {version}){Style.RESET_ALL}"
    except ImportError:
        return False, f"{Fore.RED}[MISSING] {name} is not installed{Style.RESET_ALL}"
    except Exception as e:
        return False, f"{Fore.YELLOW}[WARNING] Error checking {name}: {e}{Style.RESET_ALL}"

def install_dependency(dependency):
    """Attempts to install a dependency using pip."""
    name = dependency["name"]
    version = dependency["version"]
    
    print(f"{Fore.YELLOW}Attempting to install {name}...{Style.RESET_ALL}")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", f"{name}>={version}"])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    """Main function."""
    print(f"\n{Fore.CYAN}========================================================")
    print(f"       EVA & GUARANI - DEPENDENCY CHECKER")
    print(f"========================================================{Style.RESET_ALL}\n")
    
    # Check Python version
    python_ok = check_python_version()
    if not python_ok:
        print(f"\n{Fore.RED}Please update your Python version before continuing.{Style.RESET_ALL}")
        return
    
    # Check operating system
    print(f"{Fore.CYAN}System: {platform.system()} {platform.release()} ({platform.architecture()[0]}){Style.RESET_ALL}")
    
    # Check mandatory dependencies
    print(f"\n{Fore.CYAN}Checking mandatory dependencies...{Style.RESET_ALL}")
    missing_deps = []
    
    for dep in DEPENDENCIES:
        installed, message = check_dependency(dep)
        print(message)
        if not installed:
            missing_deps.append(dep)
    
    # Check optional dependencies
    print(f"\n{Fore.CYAN}Checking optional dependencies...{Style.RESET_ALL}")
    missing_optional_deps = []
    
    for dep in OPTIONAL_DEPENDENCIES:
        installed, message = check_dependency(dep)
        description = dep.get("description", "")
        print(f"{message} - {description}")
        if not installed:
            missing_optional_deps.append(dep)
    
    # Ask if the user wants to install missing mandatory dependencies
    if missing_deps:
        print(f"\n{Fore.YELLOW}Missing mandatory dependencies: {len(missing_deps)}{Style.RESET_ALL}")
        install = input("Do you want to install the missing mandatory dependencies? (y/n): ").lower() == 'y'
        
        if install:
            for dep in missing_deps:
                success = install_dependency(dep)
                if success:
                    print(f"{Fore.GREEN}[OK] {dep['name']} installed successfully!{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}[ERROR] Failed to install {dep['name']}.{Style.RESET_ALL}")
    
    # Ask if the user wants to install missing optional dependencies
    if missing_optional_deps:
        print(f"\n{Fore.YELLOW}Missing optional dependencies: {len(missing_optional_deps)}{Style.RESET_ALL}")
        install = input("Do you want to install the missing optional dependencies? (y/n): ").lower() == 'y'
        
        if install:
            for dep in missing_optional_deps:
                success = install_dependency(dep)
                if success:
                    print(f"{Fore.GREEN}[OK] {dep['name']} installed successfully!{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}[ERROR] Failed to install {dep['name']}.{Style.RESET_ALL}")
    
    # Final summary
    print(f"\n{Fore.CYAN}========================================================")
    print(f"                      FINAL SUMMARY")
    print(f"========================================================{Style.RESET_ALL}")
    
    if not missing_deps:
        print(f"{Fore.GREEN}All mandatory dependencies are installed!{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}Some mandatory dependencies are missing.{Style.RESET_ALL}")
        print("Run this script again to try to install them.")
    
    if not missing_optional_deps:
        print(f"{Fore.GREEN}All optional dependencies are installed!{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}Some optional dependencies are missing.{Style.RESET_ALL}")
        print("This may limit some functionalities of the bot.")
    
    print(f"\n{Fore.CYAN}The EVA & GUARANI bot is ready to be started!{Style.RESET_ALL}")
    print(f"Run 'start_bot.bat' to start the bot.")

if __name__ == "__main__":
    main()
    input("\nPress ENTER to exit...")