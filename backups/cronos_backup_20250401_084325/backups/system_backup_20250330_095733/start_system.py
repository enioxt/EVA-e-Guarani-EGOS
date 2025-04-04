import os
import sys
import subprocess
import time
import json
from datetime import datetime
import signal
import atexit


def get_root_dir():
    """Get the root directory of the project."""
    return os.path.dirname(os.path.abspath(__file__))


def install_dependencies():
    """Install required dependencies."""
    print("Installing dependencies...")
    root_dir = get_root_dir()
    requirements_file = os.path.join(root_dir, "core", "metadata", "requirements.txt")

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
        print("Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)


def start_web_interface():
    """Start the web interface."""
    print("Starting web interface...")
    root_dir = get_root_dir()
    web_dir = os.path.join(root_dir, "web")
    app_path = os.path.join(web_dir, "app.py")

    try:
        web_process = subprocess.Popen([sys.executable, app_path])
        return web_process
    except Exception as e:
        print(f"Error starting web interface: {e}")
        return None


def start_metadata_system():
    """Start the metadata system components."""
    print("Starting metadata system...")
    root_dir = get_root_dir()
    metadata_dir = os.path.join(root_dir, "core", "metadata")

    try:
        # Start scanner
        scanner_process = subprocess.Popen(
            [sys.executable, os.path.join(metadata_dir, "scanner.py")]
        )

        # Start tracker
        tracker_process = subprocess.Popen(
            [sys.executable, os.path.join(metadata_dir, "tracker.py")]
        )

        # Start organizer
        organizer_process = subprocess.Popen(
            [sys.executable, os.path.join(metadata_dir, "organizer.py")]
        )

        return [scanner_process, tracker_process, organizer_process]
    except Exception as e:
        print(f"Error starting metadata system: {e}")
        return []


def cleanup_processes(processes):
    """Clean up running processes."""
    for process in processes:
        if process and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()


def main():
    """Main function to start the system."""
    print("Starting EVA & GUARANI system...")

    # Store running processes
    processes = []

    try:
        # Install dependencies
        install_dependencies()

        # Start web interface
        web_process = start_web_interface()
        if web_process:
            processes.append(web_process)

        # Start metadata system
        metadata_processes = start_metadata_system()
        processes.extend(metadata_processes)

        # Register cleanup function
        atexit.register(cleanup_processes, processes)

        # Keep the main process running
        print("\nSystem started successfully!")
        print("Press Ctrl+C to stop...")

        while True:
            # Check if all processes are still running
            all_running = all(p and p.poll() is None for p in processes)
            if not all_running:
                print("\nOne or more components have stopped. Shutting down...")
                break
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        cleanup_processes(processes)
        print("System stopped.")


if __name__ == "__main__":
    main()
