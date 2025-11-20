# DocuGener API Reference

## Base URL

All API endpoints are prefixed with `/api` and served on `http://localhost:5000`.

## Endpoints

### Get All Captures

**GET** `/api/captures`

Returns a list of all captures with metadata.

**Response:**
```json
[
  {
    "id": "20251119_215420_506",
    "filename": "20251119_215420_506.png",
    "timestamp": "2025-11-19T21:54:20.506000",
    "click_x": 500,
    "click_y": 300,
    "window_title": "Chrome Legacy Window",
    "url": "https://example.com",
    "context": "User clicked on login button"
  }
]
```

**Status Codes:**
- `200 OK`: Success

---

### Get Capture Image

**GET** `/api/captures/<capture_id>`

Returns the PNG image file for a specific capture.

**Parameters:**
- `capture_id` (path): Unique identifier for the capture

**Response:**
- Content-Type: `image/png`
- Body: Binary image data

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Capture not found

---

### Delete Capture

**DELETE** `/api/captures/<capture_id>`

Deletes a capture and its associated image file.

**Parameters:**
- `capture_id` (path): Unique identifier for the capture

**Response:**
```json
{
  "success": true
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Capture not found

---

### Update Context

**POST** `/api/captures/<capture_id>/context`

Updates the context/description text for a capture.

**Parameters:**
- `capture_id` (path): Unique identifier for the capture

**Request Body:**
```json
{
  "context": "Updated description text"
}
```

**Response:**
```json
{
  "success": true
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Capture not found

---

### Pause/Resume Capture

**POST** `/api/pause`

Pauses or resumes the capture functionality.

**Request Body:**
```json
{
  "paused": true
}
```

**Response:**
```json
{
  "paused": true
}
```

**Status Codes:**
- `200 OK`: Success

---

### Get Status

**GET** `/api/status`

Returns the current capture status (paused or active).

**Response:**
```json
{
  "paused": false
}
```

**Status Codes:**
- `200 OK`: Success

---

### Export Captures

**POST** `/api/export`

Exports captures to PowerPoint or PDF format.

**Request Body:**
```json
{
  "format": "pptx",
  "capture_ids": ["20251119_215420_506", "20251119_215426_104"]
}
```

**Parameters:**
- `format` (string, required): Export format - `"pptx"` or `"pdf"`
- `capture_ids` (array, optional): List of capture IDs to export. If empty, exports all captures.

**Response:**
- Content-Type: 
  - `application/vnd.openxmlformats-officedocument.presentationml.presentation` (for pptx)
  - `application/pdf` (for pdf)
- Body: Binary file data
- Headers: `Content-Disposition: attachment; filename=docugener_export.{format}`

**Status Codes:**
- `200 OK`: Success
- `400 Bad Request`: Invalid format

**Example:**
```bash
curl -X POST http://localhost:5000/api/export \
  -H "Content-Type: application/json" \
  -d '{"format": "pptx"}' \
  --output presentation.pptx
```

---

### Get All Projects

**GET** `/api/projects`

Returns a list of all projects.

**Response:**
```json
[
  {
    "id": 1,
    "name": "My Project",
    "created_at": "2025-11-19T21:54:20.506000"
  }
]
```

**Status Codes:**
- `200 OK`: Success

---

### Create Project

**POST** `/api/projects`

Creates a new project.

**Request Body:**
```json
{
  "name": "My New Project"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "My New Project",
  "created_at": "2025-11-19T21:54:20.506000"
}
```

**Status Codes:**
- `200 OK`: Success
- `400 Bad Request`: Invalid request

---

### Get Project

**GET** `/api/projects/<project_id>`

Returns project details.

**Parameters:**
- `project_id` (path): Project ID

**Response:**
```json
{
  "id": 1,
  "name": "My Project",
  "created_at": "2025-11-19T21:54:20.506000"
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Project not found

---

### Update Project

**PUT** `/api/projects/<project_id>`

Updates project name.

**Parameters:**
- `project_id` (path): Project ID

**Request Body:**
```json
{
  "name": "Updated Project Name"
}
```

**Response:**
```json
{
  "success": true
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Project not found

---

### Delete Project

**DELETE** `/api/projects/<project_id>`

Deletes a project and its associated captures.

**Parameters:**
- `project_id` (path): Project ID

**Response:**
```json
{
  "success": true
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Project not found

---

### Save Current Captures to Project

**POST** `/api/projects/<project_id>/save`

Saves all current captures to a project.

**Parameters:**
- `project_id` (path): Project ID

**Response:**
```json
{
  "success": true
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Project not found

---

### Load Project Captures

**POST** `/api/projects/<project_id>/load`

Loads all captures from a project into the current session.

**Parameters:**
- `project_id` (path): Project ID

**Response:**
```json
{
  "success": true,
  "captures": [...]
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Project not found
- `500 Internal Server Error`: Failed to load project

## Error Responses

All error responses follow this format:

```json
{
  "error": "Error message description"
}
```

Common status codes:
- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## CORS

The API supports CORS for localhost origins. All endpoints accept requests from:
- `http://localhost:5000` (web interface and API)
- `http://127.0.0.1:5000`

## Rate Limiting

Currently, there is no rate limiting implemented. This is acceptable for local use.

## Authentication

No authentication is required. The API is designed for local use only.

