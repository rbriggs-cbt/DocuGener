# DocuGener Architecture

## Overview

DocuGener is built with a Python-based architecture where Flask serves both the REST API and the web interface.

## System Architecture

```
┌─────────────────┐
│   User Browser  │
│  (localhost:5000)│
└────────┬─────────┘
         │
         │ HTTP Requests
         │ (API + Static Files)
         │
┌────────▼──────────────────────────────────────┐
│  Flask Server (Port 5000)                     │
│  ┌────────────────────────────────────────┐  │
│  │  API Routes (/api/*)                   │  │
│  │  Static File Serving (HTML/CSS/JS)     │  │
│  └────────────────────────────────────────┘  │
└────────┬──────────────────────────────────────┘
         │
         │
    ┌────┴────────────────────────────────────┐
    │                                          │
┌───▼──────────┐  ┌───────────▼──────┐  ┌─────▼──────────┐
│ Click        │  │ Screen           │  │ Window         │
│ Detector     │  │ Capture          │  │ Info           │
└──────────────┘  └──────────────────┘  └────────────────┘
         │                 │                 │
         └─────────────────┼─────────────────┘
                          │
                  ┌───────▼────────┐
                  │  Image Manager │
                  │  (Storage)     │
                  └────────────────┘
```

## Components

### App Service (Python)

#### 1. Click Detector (`click_detector.py`)
- **Purpose**: Monitors global mouse clicks using `pynput`
- **Key Features**:
  - Detects Ctrl+Left Click combinations
  - Thread-safe keyboard state tracking
  - Global event listener

#### 2. Screen Capture (`screen_capture.py`)
- **Purpose**: Captures screenshots with click pointer highlights
- **Key Features**:
  - Uses `pyautogui` for thread-safe screen capture
  - Adds visual pointer highlight overlay (red circle with white border)
  - Handles full-screen captures

#### 3. Window Info (`window_info.py`)
- **Purpose**: Detects window titles and web URLs
- **Key Features**:
  - Uses Windows API (`pywin32`) to get window information
  - Extracts URLs from browser window titles
  - Gets window information at specific screen coordinates

#### 4. Image Manager (`image_manager.py`)
- **Purpose**: Manages storage and metadata for captures
- **Key Features**:
  - Stores images in `captures/` directory (project root)
  - Maintains JSON metadata file (`captures/metadata.json`)
  - Handles CRUD operations for captures
  - Works with both script and executable environments

#### 5. API Server (`api_server.py`)
- **Purpose**: Flask REST API and web server for frontend communication
- **Key Features**:
  - Serves static files (HTML, CSS, JS) from `frontend/public/`
  - Handles SPA routing (serves index.html for non-API routes)
  - REST API endpoints for frontend communication
- **Endpoints**:
  - `GET /api/captures` - List all captures
  - `GET /api/captures/<id>` - Get capture image
  - `DELETE /api/captures/<id>` - Delete capture
  - `POST /api/captures/<id>/context` - Update context text
  - `POST /api/pause` - Pause/resume capture
  - `GET /api/status` - Get capture status
  - `POST /api/export` - Export to PowerPoint/PDF
  - `GET /` - Serve web interface (index.html)
  - `GET /<static_file>` - Serve static assets (CSS, JS, etc.)

#### 6. Project Manager (`project_manager.py`)
- **Purpose**: Manages project storage and retrieval using SQLite
- **Key Features**:
  - Stores projects in `projects.db` (project root)
  - Handles project creation, loading, and deletion
  - Manages project-specific capture organization

#### 7. Main Entry Point (`main.py`)
- **Purpose**: Initializes and coordinates all components
- **Responsibilities**:
  - Starts click detector
  - Launches Flask API server in separate thread
  - Handles graceful shutdown

### Frontend (Static Files)

#### 1. Web Interface (`frontend/public/`)
- **index.html**: Main HTML structure
- **styles.css**: Styling and layout
- **app.js**: Frontend JavaScript logic
  - Fetches and displays captures
  - Handles user interactions (pause, delete, export)
  - Auto-refreshes capture list

## Data Flow

### Capture Flow
1. User presses **Ctrl+Click** anywhere on screen
2. `ClickDetector` detects the event
3. `WindowInfo` gets window title and URL at click location
4. `ScreenCapture` takes screenshot with pointer highlight
5. `ImageManager` saves image and metadata
6. Frontend polls API and displays new capture

### Export Flow
1. User clicks "Export" in web interface
2. Frontend sends POST request to `/api/export` with format (pptx/pdf)
3. App service loads all captures from metadata
4. Generates PowerPoint or PDF with images and context text
5. Returns file for download

### Project Flow
1. User creates a new project via web interface
2. Frontend sends POST request to `/api/projects`
3. Project Manager creates project entry in database
4. Captures can be associated with projects
5. Projects can be loaded, listed, and deleted via API

## Technology Stack

### App Service
- **Python 3.8+**
- **Flask**: Web framework for API
- **pynput**: Mouse/keyboard event handling
- **pyautogui**: Screen capture
- **pywin32**: Windows API access
- **Pillow (PIL)**: Image processing
- **python-pptx**: PowerPoint generation
- **reportlab**: PDF generation

### Frontend
- **Vanilla JavaScript**: No framework dependencies
- **HTML5/CSS3**: Modern web standards
- **Static files served by Flask**: HTML, CSS, and JavaScript files

## Security Considerations

- No authentication required (local use only)
- CORS enabled for localhost only
- File operations restricted to `captures/` directory
- No external network requests (except local API)

## Performance

- Click detection: Near-instant (< 10ms)
- Screen capture: ~100-200ms per capture
- Image storage: ~50-100ms per image
- Web interface: Auto-refreshes every 2 seconds

## Future Enhancements

- Multi-monitor support
- Video recording option
- Cloud storage integration
- User authentication
- Capture editing tools
- Keyboard shortcut customization

