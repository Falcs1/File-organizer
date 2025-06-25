#!/usr/bin/env python3
"""
File Organizer Launcher
Simple launcher script for the Advanced File Organizer
"""

import sys
import os
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 6):
        print("❌ Error: Python 3.6 or higher is required!")
        print(f"   Your version: {sys.version}")
        print("   Please upgrade Python and try again.")
        return False
    return True

def check_tkinter():
    """Check if tkinter is available for GUI mode."""
    try:
        import tkinter
        return True
    except ImportError:
        print("⚠️  Warning: tkinter not available - GUI mode disabled")
        print("   You can still use command line mode with --cli")
        return False

def main():
    """Main launcher function."""
    print("🚀 Advanced File Organizer Launcher")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        return 1
    
    # Check if main script exists
    main_script = Path("file_organizer.py")
    if not main_script.exists():
        print("❌ Error: file_organizer.py not found!")
        print("   Make sure all files are in the same directory.")
        input("Press Enter to exit...")
        return 1
    
    # Check tkinter availability
    gui_available = check_tkinter()
    
    print(f"✅ Python version: {sys.version.split()[0]}")
    print(f"✅ Main script found: {main_script}")
    print(f"{'✅' if gui_available else '⚠️ '} GUI mode: {'Available' if gui_available else 'Not available'}")
    print()
    
    # Ask user for preferred mode
    if gui_available:
        print("Choose your preferred mode:")
        print("1. GUI Mode (Recommended)")
        print("2. Command Line Mode")
        print("3. Exit")
        
        while True:
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == "1":
                print("\n🎨 Starting GUI mode...")
                try:
                    subprocess.run([sys.executable, "file_organizer.py"], check=True)
                except subprocess.CalledProcessError as e:
                    print(f"❌ Error running GUI mode: {e}")
                    input("Press Enter to exit...")
                    return 1
                break
            
            elif choice == "2":
                print("\n💻 Starting command line mode...")
                try:
                    subprocess.run([sys.executable, "file_organizer.py", "--cli"], check=True)
                except subprocess.CalledProcessError as e:
                    print(f"❌ Error running CLI mode: {e}")
                    input("Press Enter to exit...")
                    return 1
                break
            
            elif choice == "3":
                print("👋 Goodbye!")
                return 0
            
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")
    
    else:
        # Only CLI mode available
        print("🖥️  Starting in command line mode...")
        print("   (GUI mode not available - tkinter missing)")
        
        confirm = input("\nContinue with command line mode? (y/N): ").strip().lower()
        if confirm in ['y', 'yes']:
            try:
                subprocess.run([sys.executable, "file_organizer.py", "--cli"], check=True)
            except subprocess.CalledProcessError as e:
                print(f"❌ Error running CLI mode: {e}")
                input("Press Enter to exit...")
                return 1
        else:
            print("👋 Goodbye!")
            return 0
    
    print("\n✅ File Organizer completed successfully!")
    input("Press Enter to exit...")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 