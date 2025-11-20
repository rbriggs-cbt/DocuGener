#!/bin/bash
# Build script for creating DocuGener executable (Linux/Mac)
# Note: This is primarily for Windows, but included for completeness

echo "========================================"
echo "Building DocuGener Executable"
echo "========================================"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Go up one level to get project root (scripts/ -> project root)
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Change to project root
cd "$PROJECT_ROOT"

# Check if we found the right directory
if [ ! -f "app/main.py" ]; then
    echo "Error: Could not find project root directory"
    echo "Expected: $PROJECT_ROOT/app/main.py"
    echo "Current directory: $(pwd)"
    exit 1
fi

echo "Project root: $PROJECT_ROOT"
echo ""

# Ensure we're in project root
cd "$PROJECT_ROOT"

# Check if virtual environment exists
if [ ! -d "app/venv" ]; then
    echo "Creating virtual environment..."
    cd app
    python3 -m venv venv
    cd "$PROJECT_ROOT"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source app/venv/bin/activate

# Install/upgrade dependencies
echo ""
echo "Installing dependencies..."
python3 -m pip install -q --upgrade pip
python3 -m pip install -q -r app/requirements.txt

# Build the executable
echo ""
echo "Building executable with PyInstaller..."
echo "This may take a few minutes..."
echo ""

cd app
pyinstaller --clean --noconfirm DocuGener.spec

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "Build successful!"
    echo "========================================"
    echo ""
    echo "Executable location: $PROJECT_ROOT/app/dist/DocuGener"
    echo ""
    echo "You can now distribute DocuGener to users."
    echo "The executable is portable and doesn't require Python."
    echo ""
else
    echo ""
    echo "========================================"
    echo "Build failed!"
    echo "========================================"
    echo ""
    echo "Check the error messages above."
    echo ""
fi

cd "$PROJECT_ROOT"

