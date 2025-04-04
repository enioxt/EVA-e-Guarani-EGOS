#!/usr/bin/env python3
import os
import sys
import socket
from pathlib import Path


def check_file_access(path):
    try:
        with open(path, "r") as f:
            print(f"✅ Can read {path}")
    except Exception as e:
        print(f"❌ Cannot read {path}: {e}")


def check_dir_access(path):
    try:
        if os.path.exists(path):
            print(f"✅ Directory exists: {path}")
            if os.access(path, os.W_OK):
                print(f"✅ Can write to directory: {path}")
            else:
                print(f"❌ Cannot write to directory: {path}")
        else:
            print(f"❌ Directory does not exist: {path}")
    except Exception as e:
        print(f"❌ Error checking directory {path}: {e}")


def check_port_access(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(("localhost", port))
        print(f"✅ Port {port} is available")
    except Exception as e:
        print(f"❌ Port {port} is not available: {e}")
    finally:
        sock.close()


def main():
    print("=== MCP Permission Check ===")

    # Check global config
    user_home = str(Path.home())
    cursor_config_dir = os.path.join(user_home, ".cursor")
    check_dir_access(cursor_config_dir)
    check_file_access(os.path.join(cursor_config_dir, "mcp.json"))

    # Check local config
    check_file_access(".cursor/mcp.json")

    # Check logs directory
    check_dir_access("logs")

    # Check port
    check_port_access(38002)
    check_port_access(38003)


if __name__ == "__main__":
    main()
