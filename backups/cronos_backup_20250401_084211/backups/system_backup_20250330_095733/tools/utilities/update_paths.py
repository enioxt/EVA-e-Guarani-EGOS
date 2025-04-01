#!/usr/bin/env python3
python
import os
import re
import fileinput
import sys

def update_import_paths(file_path):
    """Updates import paths in Python files"""
    if not os.path.exists(file_path) or not file_path.endswith('.py'):
        return False
    
    # Ignore files that are not text or have different encoding
    try:
        with open(file_path, 'r', encoding='utf-8') as test_file:
            test_file.read(1024)  # Try to read a bit of the file to test encoding
    except UnicodeDecodeError:
        print(f"Ignoring binary or non-UTF-8 encoded file: {file_path}")
        return False
    
    updated = False
    import_pattern = re.compile(r'from +([a-zA-Z0-9_]+) +import +|import +([a-zA-Z0-9_]+)')
    module_mapping = {
        'egos_core': 'EGOS.core.egos_core',
        'ethik_core': 'EGOS.core.ethik_core',
        'quantum_core_essence': 'EGOS.core.quantum_core_essence',
    }
    
    temp_file = file_path + '.tmp'
    try:
        with open(file_path, 'r', encoding='utf-8') as source_file, \
             open(temp_file, 'w', encoding='utf-8') as temp:
            
            for line in source_file:
                match = import_pattern.search(line)
                if match:
                    module_name = match.group(1) or match.group(2)
                    if module_name in module_mapping:
                        updated_module = module_mapping[module_name]
                        if match.group(1):  # from X import
                            line = line.replace(f'from {module_name}', f'from {updated_module}')
                        else:  # import X
                            line = line.replace(f'import {module_name}', f'import {updated_module}')
                        updated = True
                
                temp.write(line)
        
        if updated:
            os.replace(temp_file, file_path)
            print(f"Updated: {file_path}")
        else:
            os.remove(temp_file)
        
        return updated
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        if os.path.exists(temp_file):
            os.remove(temp_file)
        return False

def update_bat_script(file_path):
    """Updates paths in .bat scripts"""
    if not os.path.exists(file_path) or not file_path.endswith('.bat'):
        return False
    
    # Try different common encodings for batch files
    encodings = ['utf-8', 'cp1252', 'latin-1']
    content = None
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
                break
        except UnicodeDecodeError:
            continue
    
    if content is None:
        print(f"Could not decode {file_path} with any known encoding")
        return False
    
    updated = False
    # Correcting the regular expression to avoid escape error
    patterns = {
        r'python +([a-zA-Z0-9_]+\.py)': lambda match: f'python EGOS\scripts\\{match.group(1)}',
        r'set +PYTHONPATH=(.*)': lambda match: 'set PYTHONPATH=%PYTHONPATH%;%~dp0\\EGOS'
    }
    
    original_content = content
    for pattern, replacement_func in patterns.items():
        matches = re.finditer(pattern, content)
        for match in reversed(list(matches)):  # Process from back to front to not affect indices
            replacement = replacement_func(match)
            start, end = match.span()
            content = content[:start] + replacement + content[end:]
    
    if content != original_content:
        updated = True
        # Write the updated content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {file_path}")
    
    return updated

def update_init_files():
    """Creates __init__.py files in necessary folders"""
    dirs_needing_init = [
        "EGOS",
        "EGOS/core",
        "EGOS/modules",
        "EGOS/modules/atlas",
        "EGOS/modules/nexus",
        "EGOS/modules/cronos",
        "EGOS/scripts",
    ]
    
    root_dir = os.path.dirname(os.path.abspath(__file__))
    
    for dir_path in dirs_needing_init:
        full_path = os.path.join(root_dir, dir_path)
        if os.path.exists(full_path) and os.path.isdir(full_path):
            init_file = os.path.join(full_path, "__init__.py")
            if not os.path.exists(init_file):
                with open(init_file, 'w', encoding='utf-8') as f:
                    f.write(f"# Package initialization {dir_path}")
                print(f"Created: {init_file}")

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Update .bat files
    for file_name in os.listdir(root_dir):
        if file_name.endswith('.bat'):
            file_path = os.path.join(root_dir, file_name)
            try:
                update_bat_script(file_path)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
    
    # Update import paths in Python files in the root
    for file_name in os.listdir(root_dir):
        if file_name.endswith('.py'):
            file_path = os.path.join(root_dir, file_name)
            try:
                update_import_paths(file_path)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
    
    # Create __init__.py files so that EGOS works as a Python package
    update_init_files()
    
    print("\n=== Path Update Completed ===")
    print("\nNext steps:")
    print("1. Manually check the main scripts to ensure paths are correct")
    print("2. Test system initialization with the new structure")
    print("3. Update documentation to reflect the new file organization")

if __name__ == "__main__":
    main()