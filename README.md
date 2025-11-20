# DocuGener

DocuGener is a powerful screen capture and documentation tool that automatically captures screenshots on Ctrl+Click with pointer highlights, captures window titles and web URLs, and provides a web interface for organizing and exporting to presentations.

## Overview

DocuGener helps you create step-by-step documentation by automatically capturing screenshots when you Ctrl+Click anywhere on your screen. Each capture includes a visual pointer highlight, window information, and optional context text. You can then organize all captures in a web interface and export them to PowerPoint or PDF presentations.

## Features

- **Automatic Screen Capture**: Captures screenshots on Ctrl+Click with visual pointer highlights
- **Window Detection**: Automatically detects window titles and web URLs
- **Web Interface**: Modern, responsive web UI for managing captures
- **Context Management**: Add descriptions and context to each capture
- **Export Options**: Export to PowerPoint (.pptx) or PDF format
- **Pause/Resume**: Control capture functionality on the fly
- **Project Management**: Organize captures into projects
- **Portable Executable**: Build a single .exe file for easy distribution

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Windows 10+ (for window detection features)

### Installation

1. **Clone or download the repository**
   ```bash
   git clone <repository-url>
   cd DocuGener
   ```

2. **Set up the Python environment**
   ```bash
   cd app
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

4. **Open in browser**
   Navigate to `http://localhost:5000` in your web browser

## Usage

1. **Start DocuGener** (see Installation above)
2. **Open your browser** to `http://localhost:5000`
3. **Press Ctrl+Click** anywhere on your screen to capture screenshots
4. **Use the web interface** to:
   - View all captures in chronological order
   - Add context/descriptions to each capture
   - Delete unwanted captures
   - Pause/resume capture functionality
   - Export to PowerPoint (.pptx) or PDF

## Project Structure

```
DocuGener/
├── app/                    # Application code
│   ├── api_server.py      # Flask server & API endpoints
│   ├── click_detector.py  # Mouse click detection
│   ├── image_manager.py   # Image storage management
│   ├── main.py            # Application entry point
│   ├── project_manager.py # Project database management
│   ├── screen_capture.py  # Screenshot capture
│   ├── window_info.py     # Window title/URL detection
│   ├── requirements.txt   # Python dependencies
│   └── DocuGener.spec     # PyInstaller build configuration
├── captures/              # Runtime data (gitignored)
│   └── metadata.json      # Capture metadata
├── docs/                  # Documentation
│   ├── architecture.md    # System architecture
│   ├── api-reference.md  # API documentation
│   ├── BUILD_INSTRUCTIONS.md  # Build executable guide
│   ├── CONTRIBUTING.md   # Contribution guidelines
│   ├── development.md    # Development guide
│   ├── user-guide.md     # User manual
│   └── ...
├── frontend/              # Web UI
│   └── public/
│       ├── index.html    # Main HTML
│       ├── app.js        # Frontend JavaScript
│       └── styles.css    # Styling
├── scripts/               # Build scripts
│   ├── build_exe.bat     # Windows build script
│   └── build_exe.sh      # Linux/macOS build script
├── README.md              # This file
└── LICENSE                # MIT License
```

## Building Executable

To create a portable `.exe` file for distribution:

**Windows:**
```batch
scripts\build_exe.bat
```

**Linux/macOS:**
```bash
./scripts/build_exe.sh
```

The executable will be created at `app/dist/DocuGener.exe` (Windows) or `app/dist/DocuGener` (Linux/macOS).

See [Build Instructions](docs/BUILD_INSTRUCTIONS.md) for detailed information.

### Download Pre-built Executable

📦 **Download the latest release:**

**Direct Download Links (Right-click → Save As, or use the links):**
- [Download DocuGener.exe](https://raw.githubusercontent.com/rbriggs-cbt/DocuGener/nightly/app/dist/DocuGener.exe) - Portable Windows executable (75 MB)
- [Download HOW_TO_USE.txt](https://raw.githubusercontent.com/rbriggs-cbt/DocuGener/nightly/app/dist/HOW_TO_USE.txt) - Quick start guide

**Alternative:** Browse the [app/dist/](app/dist/) folder and right-click on `DocuGener.exe` → "Save link as..." to download.

The executable is self-contained and requires no Python installation. Simply download, run, and open `http://localhost:5000` in your browser.

## Documentation

Comprehensive documentation is available in the `docs/` folder:

- **[User Guide](docs/user-guide.md)** - Complete user manual
- **[Development Guide](docs/development.md)** - Setup and development instructions
- **[Architecture Overview](docs/architecture.md)** - System design and components
- **[API Reference](docs/api-reference.md)** - REST API documentation
- **[Build Instructions](docs/BUILD_INSTRUCTIONS.md)** - Building executable guide
- **[Contributing Guide](docs/CONTRIBUTING.md)** - How to contribute

## Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows 10+ (for window detection features)
- **Dependencies**: See `app/requirements.txt`

## Technology Stack

### Backend
- **Flask** - Web framework and API server
- **pynput** - Mouse/keyboard event handling
- **pyautogui** - Screen capture
- **pywin32** - Windows API access
- **Pillow (PIL)** - Image processing
- **python-pptx** - PowerPoint generation
- **reportlab** - PDF generation

### Frontend
- **Vanilla JavaScript** - No framework dependencies
- **HTML5/CSS3** - Modern web standards

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](docs/CONTRIBUTING.md) and the [Development Guide](docs/development.md) for details.

## Acknowledgments

DocuGener uses the following open-source libraries:
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [pynput](https://github.com/moses-palmer/pynput) - Input monitoring
- [pyautogui](https://github.com/asweigart/pyautogui) - Screen capture
- [Pillow](https://python-pillow.org/) - Image processing
- [python-pptx](https://python-pptx.readthedocs.io/) - PowerPoint generation
- [reportlab](https://www.reportlab.com/) - PDF generation

All dependencies are properly licensed and compatible with MIT License.
