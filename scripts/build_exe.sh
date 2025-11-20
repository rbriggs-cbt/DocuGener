#!/bin/bash
# Build script for creating DocuGener executable (Linux/Mac)
# Note: This is primarily for Windows, but included for completeness

echo "========================================"
echo "Building DocuGener Executable"
echo "========================================"
echo ""

# Check if we're in the right directory
if [ ! -f "app/main.py" ]; then
    echo "Error: This script must be run from the project root directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "app/venv" ]; then
    echo "Creating virtual environment..."
    cd app
    python3 -m venv venv
    cd ..
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
    echo "Executable location: app/dist/DocuGener"
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

cd ..

