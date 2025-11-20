@echo off
REM Build script for creating DocuGener executable
REM This script creates a single portable .exe file

echo ========================================
echo Building DocuGener Executable
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "app\main.py" (
    echo Error: This script must be run from the project root directory
    echo Current directory: %CD%
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "app\venv" (
    echo Creating virtual environment...
    cd app
    python -m venv venv
    cd ..
)

REM Activate virtual environment
echo Activating virtual environment...
call app\venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo.
echo Installing dependencies...
python -m pip install -q --upgrade pip
python -m pip install -q -r app\requirements.txt

REM Build the executable
echo.
echo Building executable with PyInstaller...
echo This may take a few minutes...
echo.

cd app
pyinstaller --clean --noconfirm DocuGener.spec

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo Build successful!
    echo ========================================
    echo.
    echo Executable location: app\dist\DocuGener.exe
    echo.
    echo You can now distribute DocuGener.exe to users.
    echo The executable is portable and doesn't require Python.
    echo.
) else (
    echo.
    echo ========================================
    echo Build failed!
    echo ========================================
    echo.
    echo Check the error messages above.
    echo.
)

cd ..
pause

