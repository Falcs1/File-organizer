#!/usr/bin/env python3
"""
File Organizer Undo Tool
Reverses file organization operations using undo logs.
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime


def find_undo_logs():
    """Find all undo log files in the current directory."""
    undo_logs = []
    for file in os.listdir('.'):
        if file.startswith('undo_log_') and file.endswith('.json'):
            undo_logs.append(file)
    return sorted(undo_logs, reverse=True)  # Most recent first


def undo_organization(undo_log_file, auto_confirm=False):
    """
    Undo a previous organization operation.
    
    Why we need this standalone tool:
    - Sometimes users just want to quickly undo without opening the GUI
    - Provides a simple command-line interface for undo operations
    - Can be used in scripts or automation
    - Separates undo logic for clarity and simplicity
    """
    print(f"Loading undo log: {undo_log_file}")
    
    try:
        with open(undo_log_file, 'r') as f:
            operations = json.load(f)
    except Exception as e:
        print(f"❌ Error loading undo log: {e}")
        return False
    
    if not operations:
        print("❌ Undo log is empty")
        return False
    
    print(f"Found {len(operations)} operations to undo")
    
    # Ask for confirmation unless auto-confirm is enabled
    if not auto_confirm:
        confirm = input(f"Undo {len(operations)} file operations? (y/N): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("Undo cancelled")
            return False
    else:
        print(f"Auto-confirming undo of {len(operations)} file operations...")
    
    # Reverse operations (last operation first)
    operations.reverse()
    
    successful = 0
    failed = 0
    
    print("\nUndoing operations...")
    print("=" * 50)
    
    for i, operation in enumerate(operations):
        try:
            # Get original and current locations
            source = Path(operation['source'])      # Where file should go back
            destination = Path(operation['destination'])  # Where file currently is
            
            # Show progress
            if (i + 1) % 100 == 0 or i < 10:
                print(f"[{i+1}/{len(operations)}] Restoring {destination.name}...")
            
            # Check if file exists in organized location
            if not destination.exists():
                if i < 10:  # Only show details for first few
                    print(f"  ⚠️  File not found: {destination.name}")
                failed += 1
                continue
            
            # Create original directory if needed
            source.parent.mkdir(parents=True, exist_ok=True)
            
            # Move file back to original location
            shutil.move(str(destination), str(source))
            successful += 1
            
            if i < 10:  # Show details for first few operations
                print(f"  ✅ Restored: {destination.name} -> {source}")
                
        except Exception as e:
            if i < 10:  # Only show details for first few
                print(f"  ❌ Failed to restore {operation.get('destination', 'unknown')}: {e}")
            failed += 1
    
    print("=" * 50)
    print(f"Undo completed!")
    print(f"✅ Successfully restored: {successful}")
    print(f"❌ Failed to restore: {failed}")
    
    # Clean up empty directories
    print("\nCleaning up empty directories...")
    cleanup_empty_dirs()
    
    return True


def cleanup_empty_dirs():
    """Remove empty directories left after undo operations."""
    try:
        # Look for common organized file locations
        possible_dirs = [
            Path.home() / "Organized Files",
            Path("Organized Files"),
            Path("../Organized Files")
        ]
        
        for base_dir in possible_dirs:
            if base_dir.exists():
                cleanup_dir_tree(base_dir)
                break
    except Exception as e:
        print(f"Note: Could not clean up directories: {e}")


def cleanup_dir_tree(base_dir):
    """Remove empty directories in a directory tree."""
    removed_count = 0
    
    # Walk bottom-up to remove empty directories
    for root, dirs, files in os.walk(base_dir, topdown=False):
        for directory in dirs:
            dir_path = Path(root) / directory
            try:
                if dir_path.exists() and not any(dir_path.iterdir()):
                    dir_path.rmdir()
                    removed_count += 1
            except:
                pass  # Ignore errors
    
    if removed_count > 0:
        print(f"Removed {removed_count} empty directories")


def main():
    """Main function."""
    print("🔄 File Organizer Undo Tool")
    print("=" * 40)
    
    # Check for auto-confirm flag
    auto_confirm = '--yes' in sys.argv or '-y' in sys.argv
    
    # Find available undo logs
    undo_logs = find_undo_logs()
    
    if not undo_logs:
        print("❌ No undo log files found in current directory")
        print("   Undo logs are named like: undo_log_YYYYMMDD_HHMMSS.json")
        return 1
    
    print(f"Found {len(undo_logs)} undo log(s):")
    for i, log_file in enumerate(undo_logs):
        # Extract timestamp from filename
        try:
            timestamp_part = log_file.replace('undo_log_', '').replace('.json', '')
            dt = datetime.strptime(timestamp_part, '%Y%m%d_%H%M%S')
            formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
            
            # Get file size
            size_mb = os.path.getsize(log_file) / (1024 * 1024)
            
            print(f"  {i+1}. {log_file} ({formatted_time}, {size_mb:.1f}MB)")
        except:
            print(f"  {i+1}. {log_file}")
    
    # Let user choose which log to use
    if len(undo_logs) == 1:
        print(f"\nUsing the only available log: {undo_logs[0]}")
        chosen_log = undo_logs[0]
    else:
        while True:
            try:
                choice = input(f"\nChoose an undo log (1-{len(undo_logs)}): ").strip()
                index = int(choice) - 1
                
                if 0 <= index < len(undo_logs):
                    chosen_log = undo_logs[index]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(undo_logs)}")
            except ValueError:
                print("Please enter a valid number")
            except KeyboardInterrupt:
                print("\nCancelled")
                return 0
    
    # Perform the undo
    print(f"\nSelected: {chosen_log}")
    success = undo_organization(chosen_log, auto_confirm)
    
    if success:
        print("\n🎉 Undo completed successfully!")
        print("Your files have been restored to their original locations.")
    else:
        print("\n❌ Undo failed or was cancelled")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main()) 