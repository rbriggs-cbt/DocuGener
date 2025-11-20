# DocuGener Development Guide

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Windows 10+ (for window detection features)
- Git

### Initial Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd DocuGener
   ```

2. **Set up Python environment**
   ```bash
   cd app
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

## Project Structure

```
DocuGener/
├── app/                       # Application code
│   ├── api_server.py          # Flask server & API endpoints
│   ├── click_detector.py      # Mouse click detection
│   ├── image_manager.py       # Image storage management
│   ├── main.py                # Application entry point
│   ├── project_manager.py     # Project database management
│   ├── screen_capture.py      # Screenshot capture
│   ├── window_info.py         # Window title/URL detection
│   ├── requirements.txt       # Python dependencies
│   ├── DocuGener.spec         # PyInstaller build configuration
│   └── venv/                  # Local virtual environment (gitignored)
├── captures/                  # Runtime data (gitignored)
│   └── metadata.json          # Capture metadata
├── docs/                      # Documentation
│   ├── architecture.md        # System architecture
│   ├── api-reference.md       # API documentation
│   ├── BUILD_INSTRUCTIONS.md  # Build executable guide
│   ├── CONTRIBUTING.md        # Contribution guidelines
│   ├── development.md         # This file
│   ├── user-guide.md          # User manual
│   └── ...
├── frontend/                  # Web UI
│   └── public/
│       ├── index.html         # Main HTML
│       ├── app.js             # Frontend JavaScript
│       └── styles.css         # Styling
├── scripts/                   # Build scripts
│   ├── build_exe.bat          # Windows build script
│   └── build_exe.sh           # Linux/macOS build script
├── README.md                  # Main readme
├── LICENSE                    # MIT License
└── .gitignore                 # Git ignore rules
```

## Running in Development

### Running the Application

```bash
cd app
python main.py
```

The application will start on `http://localhost:5000` and serve both the API and web interface.

## Development Workflow

1. Make changes to code
2. Test locally
3. Commit changes with descriptive messages
4. Push to repository

## Code Style

### Python
- Follow PEP 8 style guide
- Use type hints where appropriate
- Document functions with docstrings
- Maximum line length: 100 characters

### JavaScript
- Use modern ES6+ syntax
- Use meaningful variable names
- Comment complex logic
- Follow consistent indentation (2 spaces)

## Testing

Currently, manual testing is used. Future improvements:
- Unit tests for app components
- Integration tests for API endpoints
- Frontend testing with Jest

## Debugging

### App Service
- Check console output for error messages
- Use Python debugger (`pdb`) for breakpoints
- Check Flask logs for API errors

### Frontend
- Use browser DevTools console
- Check Network tab for API requests
- Use browser debugger for JavaScript

## Common Issues

### Screenshot capture fails
- Ensure you have proper permissions
- Check if pyautogui is installed correctly
- Verify screen resolution settings

### API requests fail
- Ensure the app service is running on port 5000
- Check CORS settings
- Verify frontend is accessing correct URL

### Window detection doesn't work
- Ensure you're on Windows
- Check pywin32 installation
- Verify window is not minimized

## Adding New Features

1. **App Feature**
   - Add new module in `app/`
   - Update `api_server.py` if API endpoint needed
   - Update `main.py` if initialization needed
   - Update `requirements.txt` if new dependency

2. **Frontend Feature**
   - Update `public/app.js` for logic
   - Update `public/styles.css` for styling
   - Update `public/index.html` for UI

3. **Documentation**
   - Update relevant documentation files
   - Update README if user-facing

## Building for Production

Currently, the application runs in development mode. For production:

1. Set `debug=False` in Flask app
2. Use production WSGI server (e.g., Gunicorn)
3. Set up proper error logging
4. Configure environment variables

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License. See LICENSE file for details.

