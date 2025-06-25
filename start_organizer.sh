#!/bin/bash

echo ""
echo "===================================="
echo "   Advanced File Organizer"
echo "===================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "❌ ERROR: Python is not installed or not in PATH"
        echo "   Please install Python 3.6 or higher"
        echo ""
        read -p "Press Enter to exit..."
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
REQUIRED_VERSION="3.6"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" = "$REQUIRED_VERSION" ]; then
    echo "✅ Python version: $PYTHON_VERSION"
else
    echo "❌ ERROR: Python $REQUIRED_VERSION or higher is required"
    echo "   Your version: $PYTHON_VERSION"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Check if file_organizer.py exists
if [ ! -f "file_organizer.py" ]; then
    echo "❌ ERROR: file_organizer.py not found!"
    echo "   Make sure all files are in the same directory."
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Make scripts executable
chmod +x file_organizer.py 2>/dev/null
chmod +x run_organizer.py 2>/dev/null

# Try to run the launcher first
if [ -f "run_organizer.py" ]; then
    echo "🚀 Starting File Organizer Launcher..."
    echo ""
    $PYTHON_CMD run_organizer.py
else
    echo "🚀 Launcher not found, starting main application..."
    echo ""
    $PYTHON_CMD file_organizer.py
fi

echo ""
echo "✅ File Organizer finished."
read -p "Press Enter to exit..." 