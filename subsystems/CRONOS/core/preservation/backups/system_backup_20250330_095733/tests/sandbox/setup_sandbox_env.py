#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Sandbox Environment Setup
This script sets up the necessary environment for the EVA & GUARANI sandbox.
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def print_header():
    """Print a formatted header"""
    print("\n========================================================================")
    print("             EVA & GUARANI - Sandbox Environment Setup                  ")
    print("========================================================================\n")

def print_step(step, description):
    """Print a formatted step"""
    print(f"\n[{step}] {description}")
    print("-" * 70)

def run_command(command, verbose=True):
    """Run a shell command and return the output"""
    if verbose:
        print(f"Running: {command}")
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Error output: {e.stderr}")
        return None

def check_python():
    """Check Python version"""
    print_step("1", "Checking Python installation")
    
    try:
        python_version = sys.version.split()[0]
        print(f"Python version: {python_version}")
        
        major, minor, *_ = python_version.split(".")
        if int(major) < 3 or (int(major) == 3 and int(minor) < 8):
            print("Warning: Python 3.8 or higher is recommended.")
            return False
        
        return True
    except Exception as e:
        print(f"Error checking Python version: {e}")
        return False

def install_dependencies():
    """Install required dependencies"""
    print_step("2", "Installing required dependencies")
    
    requirements = [
        "flask>=2.0.1",
        "flask-cors>=3.0.10",
        "requests>=2.27.1",
        "python-dotenv>=0.19.2",
        "openai>=1.0.0"
    ]
    
    # Check if we need to install the dependencies
    missing_deps = []
    for req in requirements:
        package = req.split(">=")[0]
        try:
            __import__(package.replace("-", "_"))
            print(f"✓ {package} is already installed")
        except ImportError:
            missing_deps.append(req)
    
    if missing_deps:
        print(f"Installing {len(missing_deps)} missing dependencies...")
        for dep in missing_deps:
            print(f"  Installing {dep}...")
            result = run_command(f"{sys.executable} -m pip install {dep}", verbose=False)
            if result is not None:
                print(f"  ✓ {dep} installed successfully")
            else:
                print(f"  ✗ Failed to install {dep}")
                return False
    else:
        print("All dependencies are already installed.")
    
    return True

def check_sandbox_structure():
    """Check and create the sandbox directory structure if needed"""
    print_step("3", "Checking sandbox directory structure")
    
    # Get the sandbox root directory (where this script is located)
    sandbox_root = Path(__file__).parent.resolve()
    print(f"Sandbox root directory: {sandbox_root}")
    
    # Essential directories
    essential_dirs = [
        "api/flask_api",
        "frontend/html_basic",
        "examples",
        "tools",
        "docs"
    ]
    
    # Check if directories exist and create them if they don't
    for directory in essential_dirs:
        dir_path = sandbox_root / directory
        if not dir_path.exists():
            print(f"Creating directory: {dir_path}")
            dir_path.mkdir(parents=True, exist_ok=True)
    
    # Check if essential files exist
    essential_files = [
        ("requirements.txt", "# EVA & GUARANI Sandbox - Requirements\n\n" +
                            "# Web Frameworks\n" +
                            "flask>=2.0.1\n" +
                            "flask-cors>=3.0.10\n\n" +
                            "# Utilities\n" +
                            "requests>=2.27.1\n" +
                            "python-dotenv>=0.19.2\n\n" +
                            "# AI & Translation\n" +
                            "openai>=1.0.0\n")
    ]
    
    for file_name, default_content in essential_files:
        file_path = sandbox_root / file_name
        if not file_path.exists():
            print(f"Creating file: {file_path}")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(default_content)
    
    return True

def check_for_run_script():
    """Check if run_sandbox scripts exist and create them if needed"""
    print_step("4", "Checking run scripts")
    
    sandbox_root = Path(__file__).parent.resolve()
    
    # Create Windows batch file if it doesn't exist
    batch_file = sandbox_root / "run_sandbox.bat"
    if not batch_file.exists():
        print(f"Creating run_sandbox.bat")
        with open(batch_file, "w", encoding="utf-8") as f:
            f.write("@echo off\n")
            f.write("REM EVA & GUARANI - Sandbox Runner\n")
            f.write("REM This batch file runs the sandbox environment\n\n")
            f.write("echo Starting EVA & GUARANI sandbox environment...\n\n")
            f.write("cd api\\flask_api\n")
            f.write("start \"EVA & GUARANI - Flask API\" python -m flask run --debug\n\n")
            f.write("echo Opening browser...\n")
            f.write("timeout /t 3 /nobreak > NUL\n")
            f.write("start http://localhost:5000\n\n")
            f.write("echo.\n")
            f.write("echo Sandbox is running. Press Ctrl+C in the Flask window to stop.\n")
    
    # Create Python run script if it doesn't exist
    py_file = sandbox_root / "run_sandbox.py"
    if not py_file.exists():
        print(f"Creating run_sandbox.py")
        with open(py_file, "w", encoding="utf-8") as f:
            f.write('#!/usr/bin/env python\n')
            f.write('# -*- coding: utf-8 -*-\n\n')
            f.write('"""\n')
            f.write('EVA & GUARANI - Sandbox Runner\n')
            f.write('This script runs the sandbox environment\n')
            f.write('"""\n\n')
            f.write('import os\n')
            f.write('import sys\n')
            f.write('import time\n')
            f.write('import subprocess\n')
            f.write('import webbrowser\n')
            f.write('from pathlib import Path\n\n')
            f.write('def main():\n')
            f.write('    """Main function"""\n')
            f.write('    print("Starting EVA & GUARANI sandbox environment...")\n\n')
            f.write('    # Get the api directory\n')
            f.write('    sandbox_root = Path(__file__).parent.resolve()\n')
            f.write('    api_dir = sandbox_root / "api" / "flask_api"\n\n')
            f.write('    # Change to the API directory\n')
            f.write('    os.chdir(api_dir)\n\n')
            f.write('    # Start the Flask server\n')
            f.write('    flask_process = subprocess.Popen([sys.executable, "-m", "flask", "run", "--debug"])\n\n')
            f.write('    # Wait a moment for the server to start\n')
            f.write('    print("Opening browser at http://localhost:5000")\n')
            f.write('    time.sleep(3)\n')
            f.write('    webbrowser.open("http://localhost:5000")\n\n')
            f.write('    print("Press Ctrl+C to stop the server")\n\n')
            f.write('    try:\n')
            f.write('        # Keep the script running until Ctrl+C\n')
            f.write('        flask_process.wait()\n')
            f.write('    except KeyboardInterrupt:\n')
            f.write('        # Terminate the Flask process on Ctrl+C\n')
            f.write('        flask_process.terminate()\n')
            f.write('        print("\\nSandbox stopped.")\n\n')
            f.write('    return 0\n\n')
            f.write('if __name__ == "__main__":\n')
            f.write('    sys.exit(main())\n')
    
    # Make Python script executable
    if platform.system() != "Windows":
        os.chmod(py_file, 0o755)
    
    return True

def main():
    """Main function"""
    print_header()
    
    # Check Python version
    if not check_python():
        print("⚠️ Python version check failed. Continuing anyway...")
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies. Please check the error messages above.")
        return 1
    
    # Check sandbox structure
    if not check_sandbox_structure():
        print("❌ Failed to verify sandbox structure. Please check the error messages above.")
        return 1
    
    # Check for run scripts
    if not check_for_run_script():
        print("❌ Failed to create run scripts. Please check the error messages above.")
        return 1
    
    print("\n✅ Sandbox environment setup completed successfully!")
    print("\nYou can now run the sandbox using:")
    print("  - On Windows: run_sandbox.bat")
    print("  - On Linux/Mac: python run_sandbox.py")
    print("\nSandbox URL: http://localhost:5000")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 