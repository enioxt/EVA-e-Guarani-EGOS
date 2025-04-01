#!/usr/bin/env python3
import os

# Create test directory
os.makedirs("test_dir", exist_ok=True)

# Create test file
with open("test_dir/test.txt", "w") as f:
    f.write("Test file content")

# Read test file
with open("test_dir/test.txt", "r") as f:
    content = f.read()
    print(f"File content: {content}")

print("Test completed successfully!") 