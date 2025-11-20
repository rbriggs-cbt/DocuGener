@echo off
REM Build script for creating DocuGener executable
REM This script creates a single portable .exe file

echo ========================================
echo Building DocuGener Executable
echo ========================================
echo.

REM Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"
REM Go up one level to get project root (scripts/ -> project root)
REM Remove trailing backslash from SCRIPT_DIR first
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
cd /d "%SCRIPT_DIR%\.."
set "PROJECT_ROOT=%CD%"

REM Check if we found the right directory
if not exist "%PROJECT_ROOT%\app\main.py" (
    echo Error: Could not find project root directory
    echo Expected: %PROJECT_ROOT%\app\main.py
    echo Current directory: %CD%
    pause
    exit /b 1
)

echo Project root: %PROJECT_ROOT%
echo.

REM Change to project root directory
cd /d "%PROJECT_ROOT%"

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
    echo Executable location: %PROJECT_ROOT%\app\dist\DocuGener.exe
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

cd "%PROJECT_ROOT%"
pause

