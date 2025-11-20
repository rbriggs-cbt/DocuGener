# DocuGener

DocuGener is a powerful screen capture and documentation tool that automatically captures screenshots on Ctrl+Click with pointer highlights, captures window titles and web URLs, and provides a web interface for organizing and exporting to presentations.

## Overview

DocuGener helps you create step-by-step documentation by automatically capturing screenshots when you Ctrl+Click anywhere on your screen. Each capture includes a visual pointer highlight, window information, and optional context text. You can then organize all captures in a web interface and export them to PowerPoint or PDF presentations.

## Features

- Automatic screen capture on mouse clicks
- Click pointer highlight overlay
- Window title detection
- Web URL detection for browser windows
- Pause/resume functionality
- Web interface for organizing captures
- Context text input for each capture
- Export to PowerPoint (.pptx) or PDF

## Setup

### Backend (Python)

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the backend:
   ```bash
   python main.py
   ```

### Frontend (Node.js)

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the frontend server:
   ```bash
   npm start
   ```

4. Open your browser to `http://localhost:5100`

## Usage

1. Start the backend server (Python) - see Backend setup above
2. Start the frontend server (Node.js) - see Frontend setup above
3. Open your browser to `http://localhost:5100`
4. **Press Ctrl+Click** anywhere on your screen to capture screenshots
5. Use the web interface to:
   - View all captures in chronological order
   - Add context/descriptions to each capture
   - Delete unwanted captures
   - Pause/resume capture functionality
   - Export to PowerPoint (.pptx) or PDF

## Documentation

Comprehensive documentation is available in the `documentation/` folder:
- [Architecture Overview](documentation/architecture.md)
- [API Reference](documentation/api-reference.md)
- [Development Guide](documentation/development.md)
- [User Guide](documentation/user-guide.md)

## Requirements

- Python 3.8+
- Node.js 14+
- Windows 10+ (for window detection features)

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) and the [Development Guide](documentation/development.md) for details.

## Acknowledgments

DocuGener uses the following open-source libraries:
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [pynput](https://github.com/moses-palmer/pynput) - Input monitoring
- [pyautogui](https://github.com/asweigart/pyautogui) - Screen capture
- [Pillow](https://python-pillow.org/) - Image processing
- [python-pptx](https://python-pptx.readthedocs.io/) - PowerPoint generation
- [reportlab](https://www.reportlab.com/) - PDF generation
- [Express](https://expressjs.com/) - Node.js web server

All dependencies are properly licensed and compatible with MIT License.

