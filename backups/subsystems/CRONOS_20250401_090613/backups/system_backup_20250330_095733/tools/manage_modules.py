#!/usr/bin/env python3
"""
EVA & GUARANI - Module Management Tool
This tool helps manage the modules directory by allowing you to enable/disable
specific modules when you need them, improving indexing performance.
"""

import os
import sys
import json
import shutil
from pathlib import Path
import argparse

# Configuration
MODULE_GROUPS = {
    "core": [
        "analysis",
        "visualization",
        "preservation",
    ],
    "extensions": [
        "plugins",
        "integration",
        "customization",
    ],
    "specialized": [
        "blockchain",
        "quantum",
        "eliza",
    ],
    "utilities": [
        "monitoring",
        "config",
        "nexus",
    ]
}

def get_module_size(module_path):
    """Calculate the size of a module directory."""
    size = 0
    if module_path.exists():
        for path in module_path.glob('**/*'):
            if path.is_file():
                size += path.stat().st_size
    return size

def human_readable_size(size_bytes):
    """Convert bytes to human-readable format."""
    if size_bytes == 0:
        return "0B"
    
    size_names = ("B", "KB", "MB", "GB", "TB")
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024
        i += 1
    
    return f"{size_bytes:.2f} {size_names[i]}"

def list_modules(modules_dir, only_enabled=False, show_details=False):
    """List modules in the modules directory."""
    modules_path = Path(modules_dir)
    
    if not modules_path.exists():
        print(f"Error: Modules directory '{modules_dir}' does not exist.")
        return
    
    # Track enabled and disabled modules
    enabled_modules = []
    disabled_modules = []
    
    # Check which modules are enabled/disabled
    for item in modules_path.glob('*'):
        if not item.is_dir() or item.name.startswith('__'):
            continue
        
        if item.name.endswith('.disabled'):
            disabled_modules.append(item)
        else:
            enabled_modules.append(item)
    
    # Determine which list to display
    modules_to_display = enabled_modules if only_enabled else enabled_modules + disabled_modules
    
    # Sort modules by group
    modules_by_group = {}
    ungrouped_modules = []
    
    for module in modules_to_display:
        module_name = module.name
        if module_name.endswith('.disabled'):
            module_name = module_name[:-9]  # Remove .disabled suffix
        
        # Find which group this module belongs to
        found_group = None
        for group, modules in MODULE_GROUPS.items():
            if module_name in modules:
                found_group = group
                break
        
        if found_group:
            if found_group not in modules_by_group:
                modules_by_group[found_group] = []
            modules_by_group[found_group].append(module)
        else:
            ungrouped_modules.append(module)
    
    # Display modules by group
    print("\nModules by Group:")
    print(f"{'Status':<10} {'Group':<15} {'Module':<20} {'Size':<10}")
    print("-" * 60)
    
    for group, modules in sorted(modules_by_group.items()):
        for module in sorted(modules, key=lambda m: m.name):
            module_name = module.name
            is_enabled = not module_name.endswith('.disabled')
            if not is_enabled:
                module_name = module_name[:-9]
            
            status = "Enabled" if is_enabled else "Disabled"
            size = human_readable_size(get_module_size(module))
            
            print(f"{status:<10} {group:<15} {module_name:<20} {size:<10}")
    
    # Display ungrouped modules
    if ungrouped_modules:
        print("\nUngrouped Modules:")
        for module in sorted(ungrouped_modules, key=lambda m: m.name):
            module_name = module.name
            is_enabled = not module_name.endswith('.disabled')
            if not is_enabled:
                module_name = module_name[:-9]
            
            status = "Enabled" if is_enabled else "Disabled"
            size = human_readable_size(get_module_size(module))
            
            print(f"{status:<10} {'ungrouped':<15} {module_name:<20} {size:<10}")
    
    # Show detailed information if requested
    if show_details:
        total_size = sum(get_module_size(m) for m in modules_to_display)
        print(f"\nTotal size of all modules: {human_readable_size(total_size)}")
        print(f"Enabled modules: {len(enabled_modules)}")
        print(f"Disabled modules: {len(disabled_modules)}")

def enable_module(modules_dir, module_name):
    """Enable a module that was previously disabled."""
    modules_path = Path(modules_dir)
    disabled_path = modules_path / f"{module_name}.disabled"
    enabled_path = modules_path / module_name
    
    if not disabled_path.exists():
        print(f"Error: Disabled module '{module_name}' not found.")
        return False
    
    try:
        disabled_path.rename(enabled_path)
        print(f"✓ Module '{module_name}' enabled successfully.")
        return True
    except Exception as e:
        print(f"Error enabling module '{module_name}': {e}")
        return False

def disable_module(modules_dir, module_name):
    """Disable a module to improve indexing performance."""
    modules_path = Path(modules_dir)
    enabled_path = modules_path / module_name
    disabled_path = modules_path / f"{module_name}.disabled"
    
    if not enabled_path.exists():
        print(f"Error: Module '{module_name}' not found or already disabled.")
        return False
    
    try:
        enabled_path.rename(disabled_path)
        print(f"✓ Module '{module_name}' disabled successfully.")
        return True
    except Exception as e:
        print(f"Error disabling module '{module_name}': {e}")
        return False

def toggle_module_group(modules_dir, group_name, enable=True):
    """Enable or disable all modules in a group."""
    if group_name not in MODULE_GROUPS:
        print(f"Error: Group '{group_name}' not found.")
        return False
    
    modules = MODULE_GROUPS[group_name]
    success_count = 0
    
    for module_name in modules:
        if enable:
            if enable_module(modules_dir, module_name):
                success_count += 1
        else:
            if disable_module(modules_dir, module_name):
                success_count += 1
    
    if success_count > 0:
        action = "enabled" if enable else "disabled"
        print(f"\n✓ Successfully {action} {success_count} of {len(modules)} modules in group '{group_name}'.")
    
    return success_count > 0

def save_profile(profile_name, enabled_modules):
    """Save the current module configuration as a profile."""
    profiles_dir = Path("tools/module_profiles")
    profiles_dir.mkdir(exist_ok=True, parents=True)
    
    profile_path = profiles_dir / f"{profile_name}.json"
    
    profile_data = {
        "name": profile_name,
        "enabled_modules": enabled_modules
    }
    
    try:
        with open(profile_path, 'w') as f:
            json.dump(profile_data, f, indent=4)
        
        print(f"✓ Profile '{profile_name}' saved successfully.")
        return True
    except Exception as e:
        print(f"Error saving profile '{profile_name}': {e}")
        return False

def load_profile(modules_dir, profile_name):
    """Load a saved module configuration profile."""
    profiles_dir = Path("tools/module_profiles")
    profile_path = profiles_dir / f"{profile_name}.json"
    
    if not profile_path.exists():
        print(f"Error: Profile '{profile_name}' not found.")
        return False
    
    try:
        with open(profile_path, 'r') as f:
            profile_data = json.load(f)
        
        enabled_modules = profile_data.get("enabled_modules", [])
        modules_path = Path(modules_dir)
        
        # First disable all modules
        for item in modules_path.glob('*'):
            if item.is_dir() and not item.name.startswith('__') and not item.name.endswith('.disabled'):
                disable_module(modules_dir, item.name)
        
        # Then enable only the ones in the profile
        for module_name in enabled_modules:
            enable_module(modules_dir, module_name)
        
        print(f"✓ Profile '{profile_name}' loaded successfully.")
        print(f"  Enabled modules: {', '.join(enabled_modules)}")
        return True
    except Exception as e:
        print(f"Error loading profile '{profile_name}': {e}")
        return False

def create_current_profile(modules_dir):
    """Create a profile from the current module state."""
    modules_path = Path(modules_dir)
    enabled_modules = []
    
    for item in modules_path.glob('*'):
        if item.is_dir() and not item.name.startswith('__') and not item.name.endswith('.disabled'):
            enabled_modules.append(item.name)
    
    return enabled_modules

def main():
    parser = argparse.ArgumentParser(description="Manage EVA & GUARANI modules to improve performance")
    parser.add_argument("--modules-dir", default="modules", help="Directory containing the modules")
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List available modules")
    list_parser.add_argument("--enabled", action="store_true", help="Show only enabled modules")
    list_parser.add_argument("--details", action="store_true", help="Show detailed information")
    
    # Enable command
    enable_parser = subparsers.add_parser("enable", help="Enable a module")
    enable_parser.add_argument("module", help="Name of the module to enable")
    
    # Disable command
    disable_parser = subparsers.add_parser("disable", help="Disable a module")
    disable_parser.add_argument("module", help="Name of the module to disable")
    
    # Group command
    group_parser = subparsers.add_parser("group", help="Manage module groups")
    group_parser.add_argument("action", choices=["list", "enable", "disable"], help="Action to perform on the group")
    group_parser.add_argument("group", nargs="?", help="Name of the group")
    
    # Profile command
    profile_parser = subparsers.add_parser("profile", help="Manage module profiles")
    profile_parser.add_argument("action", choices=["list", "save", "load"], help="Action to perform with profiles")
    profile_parser.add_argument("name", nargs="?", help="Name of the profile")
    
    args = parser.parse_args()
    
    if args.command == "list":
        list_modules(args.modules_dir, args.enabled, args.details)
    
    elif args.command == "enable":
        enable_module(args.modules_dir, args.module)
    
    elif args.command == "disable":
        disable_module(args.modules_dir, args.module)
    
    elif args.command == "group":
        if args.action == "list":
            print("\nAvailable module groups:")
            for group, modules in MODULE_GROUPS.items():
                print(f"\n{group.upper()}")
                for module in modules:
                    print(f"  - {module}")
        
        elif args.action in ["enable", "disable"]:
            if not args.group:
                print("Error: Group name is required.")
                return
            
            toggle_module_group(args.modules_dir, args.group, args.action == "enable")
    
    elif args.command == "profile":
        if args.action == "list":
            profiles_dir = Path("tools/module_profiles")
            if not profiles_dir.exists():
                print("No profiles exist yet.")
                return
            
            profiles = list(profiles_dir.glob("*.json"))
            if not profiles:
                print("No profiles exist yet.")
                return
            
            print("\nAvailable profiles:")
            for profile in profiles:
                try:
                    with open(profile, 'r') as f:
                        data = json.load(f)
                    
                    name = data.get("name", profile.stem)
                    enabled = data.get("enabled_modules", [])
                    
                    print(f"\n{name}")
                    print(f"  Enabled modules: {', '.join(enabled)}")
                except:
                    print(f"\n{profile.stem} (Error reading profile)")
        
        elif args.action == "save":
            if not args.name:
                print("Error: Profile name is required.")
                return
            
            enabled_modules = create_current_profile(args.modules_dir)
            save_profile(args.name, enabled_modules)
        
        elif args.action == "load":
            if not args.name:
                print("Error: Profile name is required.")
                return
            
            load_profile(args.modules_dir, args.name)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 