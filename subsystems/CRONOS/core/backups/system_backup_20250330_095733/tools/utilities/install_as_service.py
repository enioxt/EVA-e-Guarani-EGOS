#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Service Installer
This script installs the Telegram bot as a service on Windows.
"""

import os
import sys
import time
import logging
import argparse
import subprocess
from pathlib import Path

# Logging configuration
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/service_installer.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("service_installer")

def check_admin():
    """Checks if the script is being run as an administrator."""
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def install_nssm():
    """Installs NSSM (Non-Sucking Service Manager) if not already installed."""
    try:
        # Check if NSSM is already installed
        nssm_path = os.path.join(os.environ.get('PROGRAMFILES', 'C:\\Program Files'), 'nssm', 'nssm.exe')
        if os.path.exists(nssm_path):
            logger.info(f"NSSM is already installed at: {nssm_path}")
            return nssm_path
        
        # Check if we have a local copy of NSSM
        local_nssm = os.path.join('tools', 'nssm.exe')
        if os.path.exists(local_nssm):
            logger.info(f"Using local NSSM: {local_nssm}")
            return os.path.abspath(local_nssm)
        
        # Create directory for tools
        os.makedirs('tools', exist_ok=True)
        
        # Download NSSM
        logger.info("Downloading NSSM...")
        import urllib.request
        nssm_url = "https://nssm.cc/release/nssm-2.24.zip"
        zip_path = os.path.join('tools', 'nssm.zip')
        
        urllib.request.urlretrieve(nssm_url, zip_path)
        logger.info(f"NSSM downloaded to: {zip_path}")
        
        # Extract NSSM
        logger.info("Extracting NSSM...")
        import zipfile
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall('tools')
        
        # Find the NSSM executable
        import glob
        nssm_exe_paths = glob.glob(os.path.join('tools', 'nssm-*', 'win64', 'nssm.exe'))
        if not nssm_exe_paths:
            nssm_exe_paths = glob.glob(os.path.join('tools', 'nssm-*', 'win32', 'nssm.exe'))
        
        if nssm_exe_paths:
            nssm_exe = nssm_exe_paths[0]
            # Copy to the tools directory
            import shutil
            shutil.copy(nssm_exe, local_nssm)
            logger.info(f"NSSM installed at: {local_nssm}")
            return os.path.abspath(local_nssm)
        else:
            logger.error("Could not find the NSSM executable after extraction.")
            return None
    except Exception as e:
        logger.error(f"Error installing NSSM: {e}")
        return None

def install_service(service_name, display_name, description, script_path, nssm_path):
    """Installs the bot as a service using NSSM."""
    try:
        # Get absolute path of the Python script
        script_path = os.path.abspath(script_path)
        python_exe = sys.executable
        
        # Check if the service already exists
        check_cmd = f'"{nssm_path}" status "{service_name}"'
        result = subprocess.run(check_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if result.returncode == 0:
            logger.warning(f"Service '{service_name}' already exists. Removing...")
            remove_cmd = f'"{nssm_path}" remove "{service_name}" confirm'
            subprocess.run(remove_cmd, shell=True, check=True)
        
        # Install the service
        logger.info(f"Installing service '{service_name}'...")
        install_cmd = f'"{nssm_path}" install "{service_name}" "{python_exe}" "{script_path}"'
        subprocess.run(install_cmd, shell=True, check=True)
        
        # Configure service details
        subprocess.run(f'"{nssm_path}" set "{service_name}" DisplayName "{display_name}"', shell=True, check=True)
        subprocess.run(f'"{nssm_path}" set "{service_name}" Description "{description}"', shell=True, check=True)
        
        # Configure working directory
        work_dir = os.path.dirname(os.path.abspath(script_path))
        subprocess.run(f'"{nssm_path}" set "{service_name}" AppDirectory "{work_dir}"', shell=True, check=True)
        
        # Configure output redirection
        log_dir = os.path.join(work_dir, "logs")
        os.makedirs(log_dir, exist_ok=True)
        
        stdout_log = os.path.join(log_dir, f"{service_name}_stdout.log")
        stderr_log = os.path.join(log_dir, f"{service_name}_stderr.log")
        
        subprocess.run(f'"{nssm_path}" set "{service_name}" AppStdout "{stdout_log}"', shell=True, check=True)
        subprocess.run(f'"{nssm_path}" set "{service_name}" AppStderr "{stderr_log}"', shell=True, check=True)
        
        # Configure automatic restart
        subprocess.run(f'"{nssm_path}" set "{service_name}" AppRestartDelay 10000', shell=True, check=True)  # 10 seconds
        
        # Start the service
        logger.info(f"Starting service '{service_name}'...")
        start_cmd = f'"{nssm_path}" start "{service_name}"'
        subprocess.run(start_cmd, shell=True, check=True)
        
        logger.info(f"Service '{service_name}' installed and started successfully.")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error executing command: {e}")
        return False
    except Exception as e:
        logger.error(f"Error installing service: {e}")
        return False

def remove_service(service_name, nssm_path):
    """Removes the bot service."""
    try:
        # Check if the service exists
        check_cmd = f'"{nssm_path}" status "{service_name}"'
        result = subprocess.run(check_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if result.returncode != 0:
            logger.warning(f"Service '{service_name}' does not exist.")
            return True
        
        # Stop the service
        logger.info(f"Stopping service '{service_name}'...")
        stop_cmd = f'"{nssm_path}" stop "{service_name}"'
        subprocess.run(stop_cmd, shell=True)
        
        # Remove the service
        logger.info(f"Removing service '{service_name}'...")
        remove_cmd = f'"{nssm_path}" remove "{service_name}" confirm'
        subprocess.run(remove_cmd, shell=True, check=True)
        
        logger.info(f"Service '{service_name}' removed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error executing command: {e}")
        return False
    except Exception as e:
        logger.error(f"Error removing service: {e}")
        return False

def main():
    """Main function."""
    # Check if we are on Windows
    if sys.platform != 'win32':
        print("This script only works on Windows.")
        return 1
    
    # Check if running as administrator
    if not check_admin():
        print("This script needs to be run as administrator.")
        print("Please run again with administrative privileges.")
        return 1
    
    parser = argparse.ArgumentParser(description='Install the EVA & GUARANI bot as a Windows service')
    parser.add_argument('--remove', action='store_true', help='Remove the service')
    parser.add_argument('--service-name', default='EVAGuaraniBot', help='Service name (default: EVAGuaraniBot)')
    parser.add_argument('--display-name', default='EVA & GUARANI Telegram Bot', help='Service display name')
    parser.add_argument('--script', default='monitor_bot.py', help='Script to be run as a service (default: monitor_bot.py)')
    args = parser.parse_args()
    
    print("=" * 50)
    print("EVA & GUARANI - Service Installer")
    print("=" * 50)
    
    # Install NSSM
    print("Checking/installing NSSM...")
    nssm_path = install_nssm()
    
    if not nssm_path:
        print("❌ Failed to install NSSM. Cannot continue.")
        return 1
    
    print(f"✅ NSSM available at: {nssm_path}")
    
    # Configure service
    service_name = args.service_name
    display_name = args.display_name
    description = "Service to keep the EVA & GUARANI Telegram bot running."
    script_path = os.path.abspath(args.script)
    
    if not os.path.exists(script_path):
        print(f"❌ Script not found: {script_path}")
        return 1
    
    # Remove or install the service
    if args.remove:
        print(f"Removing service '{service_name}'...")
        if remove_service(service_name, nssm_path):
            print(f"✅ Service '{service_name}' removed successfully.")
        else:
            print(f"❌ Failed to remove service '{service_name}'.")
            return 1
    else:
        print(f"Installing service '{service_name}'...")
        print(f"Script: {script_path}")
        print(f"Description: {description}")
        
        if install_service(service_name, display_name, description, script_path, nssm_path):
            print(f"✅ Service '{service_name}' installed and started successfully.")
            print("\nThe bot will now run automatically when Windows starts.")
            print("To manage the service, use the Windows Services Manager.")
            print(f"Service name: {service_name}")
        else:
            print(f"❌ Failed to install service '{service_name}'.")
            return 1
    
    print("\n" + "=" * 50)
    return 0

if __name__ == "__main__":
    sys.exit(main())