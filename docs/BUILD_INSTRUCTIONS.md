# Building DocuGener Executable

This guide explains how to build a single portable executable file that users can run without installing Python.

## Prerequisites

- Python 3.8 or higher installed
- Windows 10+ (for building Windows executable)
- All project dependencies installed

## Quick Build

### Windows

1. **Run the build script:**
   ```batch
   scripts\build_exe.bat
   ```

   This script will:
   - Create a virtual environment if needed
   - Install all dependencies including PyInstaller
   - Build the executable using the spec file
   - Output the executable to `app/dist/DocuGener.exe`

### Linux/macOS

1. **Run the build script:**
   ```bash
   ./scripts/build_exe.sh
   ```

   This will create the executable at `app/dist/DocuGener`

## Manual Build

If you prefer to build manually:

1. **Navigate to the app directory:**
   ```batch
   cd app
   ```

2. **Create and activate virtual environment:**
   ```batch
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```batch
   pip install -r requirements.txt
   ```

4. **Build the executable:**
   ```batch
   pyinstaller --clean --noconfirm DocuGener.spec
   ```

5. **Find your executable:**
   The executable will be at `app/dist/DocuGener.exe`

## What Gets Included

The executable includes:
- All Python dependencies (Flask, pynput, Pillow, etc.)
- Frontend static files (HTML, CSS, JavaScript)
- All Python modules from the app service
- Windows-specific libraries (pywin32)

## Distribution

The `DocuGener.exe` file is completely portable:
- Users don't need Python installed
- Users don't need to install any dependencies
- Just double-click to run

### Important Notes for Users

1. **First Run:**
   - The executable will create a `captures` folder next to the .exe file
   - The executable will create a `projects.db` file next to the .exe file
   - These files store user data and should be backed up

2. **Running the Application:**
   - Double-click `DocuGener.exe` to start
   - A console window will appear (this is normal)
   - The web interface will be available at `http://localhost:5000`
   - Press Ctrl+Click anywhere to capture screenshots

3. **Stopping the Application:**
   - Press Ctrl+C in the console window, or close the console window

## File Size

The executable will be approximately 50-100 MB due to:
- Python interpreter bundled inside
- All dependencies included
- Frontend files included

This is normal for PyInstaller executables.

## Troubleshooting

### Build Fails

- Make sure all dependencies are installed: `pip install -r app/requirements.txt`
- Make sure PyInstaller is installed: `pip install pyinstaller`
- Check that the `frontend/public` directory exists
- Ensure you're running the build script from the project root directory

### Executable Doesn't Run

- Make sure you're on Windows 10 or later
- Check Windows Defender isn't blocking it (may need to allow it)
- Try running from command prompt to see error messages

### Missing Modules Error

- Edit `app/DocuGener.spec` and add missing modules to `hiddenimports` list
- Rebuild the executable

## Customization

### Adding an Icon

1. Create or obtain a `.ico` file
2. Edit `app/DocuGener.spec`
3. Change `icon=None` to `icon='path/to/your/icon.ico'`
4. Rebuild

### Removing Console Window

1. Edit `app/DocuGener.spec`
2. Change `console=True` to `console=False`
3. Rebuild

Note: Removing the console makes debugging harder, so keep it during development.

## Advanced Options

See PyInstaller documentation for more options:
- https://pyinstaller.org/

