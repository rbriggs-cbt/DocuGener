# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for DocuGener
Creates a single portable executable
"""

import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Get project paths
# This spec file is in the app directory
# SPECPATH is set by PyInstaller - it may be the directory or the file path
try:
    # PyInstaller sets SPECPATH when running
    spec_path = SPECPATH
    # Check if it's a directory or a file path
    if os.path.isdir(spec_path):
        # SPECPATH is the directory containing the spec file (app directory)
        app_dir = os.path.abspath(spec_path)
    else:
        # SPECPATH is the spec file path
        app_dir = os.path.dirname(os.path.abspath(spec_path))
except NameError:
    # Fallback - use current working directory
    # This handles the case when running the spec file directly for testing
    app_dir = os.getcwd()

# Project root is one level up from the app directory
project_root = os.path.dirname(app_dir)
# Frontend public directory
frontend_public = os.path.join(project_root, 'frontend', 'public')

# Verify frontend directory exists
if not os.path.exists(frontend_public):
    try:
        spec_info = f"SPECPATH: {SPECPATH}"
    except NameError:
        spec_info = "SPECPATH: not set"
    raise FileNotFoundError(
        f"Frontend directory not found: {frontend_public}\n"
        f"{spec_info}\n"
        f"App dir: {app_dir}\n"
        f"Project root: {project_root}\n"
        f"Expected frontend path: {frontend_public}\n"
        f"Current working directory: {os.getcwd()}"
    )

# Collect all data files needed
datas = [
    (frontend_public, 'frontend/public'),
]

# Collect hidden imports
hiddenimports = [
    'pynput',
    'pynput.keyboard',
    'pynput.mouse',
    'pywin32',
    'win32api',
    'win32gui',
    'win32con',
    'flask',
    'flask_cors',
    'PIL',
    'PIL.Image',
    'reportlab',
    'pptx',
    'pptx.util',
    'sqlite3',
    'tempfile',
    'threading',
    'json',
    'datetime',
]

# Collect all submodules for packages that might have dynamic imports
hiddenimports += collect_submodules('pynput')
hiddenimports += collect_submodules('flask')
hiddenimports += collect_submodules('reportlab')
hiddenimports += collect_submodules('pptx')

a = Analysis(
    [os.path.join(app_dir, 'main.py')],
    pathex=[app_dir],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='DocuGener',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Keep console for debugging output
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Can add icon file path here if you have one
)

