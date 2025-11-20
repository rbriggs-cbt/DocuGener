"""
Flask API server for DocuGener.
Provides REST endpoints for captures, context updates, export, and pause/resume.
Also serves the frontend static files.
"""
import os
import sys
import sqlite3
from flask import Flask, jsonify, request, send_file, send_from_directory
from flask_cors import CORS
from image_manager import ImageManager
from project_manager import ProjectManager
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from pptx import Presentation
from pptx.util import Inches
import tempfile


def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Running as script, use the actual file location
        base_path = os.path.dirname(os.path.abspath(__file__))
        # Go up one level to project root
        base_path = os.path.dirname(base_path)
    return os.path.join(base_path, relative_path)


# Get the base directory (app folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Get the project root directory (one level up from app)
PROJECT_ROOT = os.path.dirname(BASE_DIR)
# Frontend public directory - use resource path for PyInstaller compatibility
FRONTEND_PUBLIC = get_resource_path('frontend/public')

app = Flask(__name__, static_folder=None)  # We'll handle static files manually
CORS(app, resources={r"/api/*": {"origins": "*", "methods": ["GET", "POST", "DELETE", "OPTIONS"]}})  # Enable CORS for frontend

# Global state
image_manager = ImageManager()
project_manager = ProjectManager()
is_paused = False


@app.route('/api/captures', methods=['GET'])
def get_captures():
    """Get all captures with metadata."""
    captures = image_manager.get_all_captures()
    return jsonify(captures)


@app.route('/api/captures/<capture_id>', methods=['GET', 'DELETE', 'OPTIONS'])
def handle_capture(capture_id):
    """Handle GET (image) or DELETE for a specific capture."""
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = jsonify({'success': True})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response
    
    if request.method == 'GET':
        # Get a specific capture image
        image_path = image_manager.get_image_path(capture_id)
        if image_path and os.path.exists(image_path):
            return send_file(image_path, mimetype='image/png')
        return jsonify({'error': 'Capture not found'}), 404
    
    elif request.method == 'DELETE':
        # Delete a capture
        if image_manager.delete_capture(capture_id):
            return jsonify({'success': True})
        return jsonify({'error': 'Capture not found'}), 404


@app.route('/api/captures/<capture_id>/context', methods=['POST'])
def update_context(capture_id):
    """Update context text for a capture."""
    data = request.get_json()
    context = data.get('context', '')
    
    if image_manager.update_context(capture_id, context):
        return jsonify({'success': True})
    return jsonify({'error': 'Capture not found'}), 404


@app.route('/api/pause', methods=['POST'])
def pause():
    """Pause or resume capture."""
    global is_paused
    data = request.get_json()
    is_paused = data.get('paused', False)
    return jsonify({'paused': is_paused})


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get current capture status."""
    global is_paused
    return jsonify({'paused': is_paused})


@app.route('/api/clear-all', methods=['POST'])
def clear_all():
    """Clear all captures from current session."""
    try:
        # Delete all image files
        captures = image_manager.get_all_captures()
        for capture in captures:
            image_path = image_manager.get_image_path(capture['id'])
            if image_path and os.path.exists(image_path):
                try:
                    os.remove(image_path)
                except:
                    pass
        
        # Clear metadata
        image_manager._save_metadata([])
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/projects', methods=['GET'])
def list_projects():
    """List all saved projects."""
    projects = project_manager.list_projects()
    return jsonify(projects)


@app.route('/api/projects', methods=['POST'])
def create_project():
    """Create a new project."""
    data = request.get_json()
    name = data.get('name', 'Untitled Project')
    description = data.get('description', '')
    
    try:
        project_id = project_manager.create_project(name, description)
        return jsonify({'id': project_id, 'success': True})
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Project name already exists'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """Get a project by ID."""
    project = project_manager.get_project(project_id)
    if project:
        return jsonify(project)
    return jsonify({'error': 'Project not found'}), 404


@app.route('/api/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    """Update a project."""
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    
    if project_manager.update_project(project_id, name, description):
        return jsonify({'success': True})
    return jsonify({'error': 'Project not found'}), 404


@app.route('/api/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    """Delete a project."""
    if project_manager.delete_project(project_id):
        return jsonify({'success': True})
    return jsonify({'error': 'Project not found'}), 404


@app.route('/api/projects/<int:project_id>/save', methods=['POST'])
def save_to_project(project_id):
    """Save current captures to a project."""
    try:
        if project_manager.save_project(project_id, image_manager):
            return jsonify({'success': True})
        return jsonify({'error': 'Failed to save project'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/projects/<int:project_id>/load', methods=['POST'])
def load_project(project_id):
    """Load a project's captures into current session."""
    try:
        if project_manager.load_project(project_id, image_manager):
            # Return updated captures list
            captures = image_manager.get_all_captures()
            return jsonify({'success': True, 'captures': captures})
        return jsonify({'error': 'Failed to load project'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/export', methods=['POST'])
def export():
    """Export captures to PowerPoint or PDF."""
    data = request.get_json()
    format_type = data.get('format', 'pptx')  # 'pptx' or 'pdf'
    capture_ids = data.get('capture_ids', [])  # If empty, export all
    
    if not capture_ids:
        # Export all captures
        all_captures = image_manager.get_all_captures()
        capture_ids = [c['id'] for c in all_captures]
    
    if format_type == 'pptx':
        return export_to_pptx(capture_ids)
    elif format_type == 'pdf':
        return export_to_pdf(capture_ids)
    else:
        return jsonify({'error': 'Invalid format'}), 400


def export_to_pptx(capture_ids):
    """Export captures to PowerPoint format."""
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)
    
    for capture_id in capture_ids:
        capture = image_manager.get_capture(capture_id)
        if not capture:
            continue
        
        image_path = image_manager.get_image_path(capture_id)
        if not image_path or not os.path.exists(image_path):
            continue
        
        # Create slide with completely blank layout
        # Find the blankest layout available (one with no placeholders)
        blank_layout = None
        for layout in prs.slide_layouts:
            if len(layout.placeholders) == 0:
                blank_layout = layout
                break
        
        # If no completely blank layout found, use layout 5 (blank)
        if blank_layout is None:
            blank_layout = prs.slide_layouts[5]  # Layout 5 is typically blank
        
        slide = prs.slides.add_slide(blank_layout)
        
        # Remove any placeholders that might exist to ensure completely blank slide
        # Collect shapes to remove first (can't modify while iterating)
        shapes_to_remove = []
        for shape in slide.shapes:
            if shape.is_placeholder:
                shapes_to_remove.append(shape)
        
        # Remove placeholder shapes
        for shape in shapes_to_remove:
            try:
                sp = shape.element
                parent = sp.getparent()
                if parent is not None:
                    parent.remove(sp)
            except:
                # If XML removal fails, try alternative method
                try:
                    slide.shapes._spTree.remove(shape.element)
                except:
                    pass  # Continue if removal fails
        
        # Add image - use absolute path
        abs_image_path = os.path.abspath(image_path)
        left = Inches(0.5)
        top = Inches(1)
        width = Inches(9)
        height = Inches(5)
        slide.shapes.add_picture(abs_image_path, left, top, width, height)
        
        # Add text box for context
        if capture.get('context'):
            left = Inches(0.5)
            top = Inches(6)
            width = Inches(9)
            height = Inches(1)
            textbox = slide.shapes.add_textbox(left, top, width, height)
            text_frame = textbox.text_frame
            text_frame.text = capture['context']
            text_frame.word_wrap = True
        
        # Add window title and URL as subtitle
        subtitle_text = capture.get('window_title', '')
        if capture.get('url'):
            subtitle_text += f" - {capture['url']}"
        
        if subtitle_text:
            left = Inches(0.5)
            top = Inches(0.2)
            width = Inches(9)
            height = Inches(0.5)
            subtitle = slide.shapes.add_textbox(left, top, width, height)
            subtitle.text_frame.text = subtitle_text
            subtitle.text_frame.paragraphs[0].font.size = Inches(0.2)
    
    # Save to temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pptx')
    prs.save(temp_file.name)
    temp_file.close()
    
    return send_file(
        temp_file.name,
        mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation',
        as_attachment=True,
        download_name='docugener_export.pptx'
    )


def export_to_pdf(capture_ids):
    """Export captures to PDF format."""
    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    temp_file.close()
    
    # Use landscape orientation
    from reportlab.lib.pagesizes import landscape, letter
    doc = SimpleDocTemplate(temp_file.name, pagesize=landscape(letter))
    story = []
    styles = getSampleStyleSheet()
    
    # Custom style for context
    context_style = ParagraphStyle(
        'ContextStyle',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
        alignment=TA_CENTER
    )
    
    for capture_id in capture_ids:
        capture = image_manager.get_capture(capture_id)
        if not capture:
            continue
        
        image_path = image_manager.get_image_path(capture_id)
        if not image_path or not os.path.exists(image_path):
            continue
        
        # Add window title and URL
        title_text = capture.get('window_title', '')
        if capture.get('url'):
            title_text += f" - {capture['url']}"
        
        if title_text:
            story.append(Paragraph(title_text, styles['Heading2']))
            story.append(Spacer(1, 0.2*inch))
        
        # Add image - use absolute path and handle PIL Image
        from PIL import Image as PILImage
        abs_image_path = os.path.abspath(image_path)
        
        # Open and potentially resize image to fit landscape page
        pil_img = PILImage.open(abs_image_path)
        img_width, img_height = pil_img.size
        aspect_ratio = img_width / img_height
        
        # Calculate dimensions maintaining aspect ratio for landscape (10.5 x 8 inches)
        max_width = 9.5 * inch
        max_height = 6 * inch
        if aspect_ratio > (max_width / max_height):
            width = max_width
            height = max_width / aspect_ratio
        else:
            height = max_height
            width = max_height * aspect_ratio
        
        img = RLImage(abs_image_path, width=width, height=height)
        story.append(img)
        story.append(Spacer(1, 0.2*inch))
        
        # Add context
        if capture.get('context'):
            story.append(Paragraph(capture['context'], context_style))
        
        # Add page break after each capture (one per page)
        story.append(PageBreak())
    
    doc.build(story)
    
    return send_file(
        temp_file.name,
        mimetype='application/pdf',
        as_attachment=True,
        download_name='docugener_export.pdf'
    )


# Serve static files (CSS, JS, images, etc.)
# Only serve known static file extensions to avoid conflicts with API routes
STATIC_EXTENSIONS = {'.css', '.js', '.html', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.woff', '.woff2', '.ttf', '.eot'}

@app.route('/<path:filename>')
def serve_static_or_spa(filename):
    """Serve static files or index.html for SPA routing."""
    # Don't serve API routes as static files
    if filename.startswith('api/'):
        return jsonify({'error': 'Not found'}), 404
    
    # Security: prevent directory traversal
    if '..' in filename or filename.startswith('/'):
        return jsonify({'error': 'Invalid path'}), 400
    
    # Check if it's a static file request
    file_ext = os.path.splitext(filename)[1].lower()
    if file_ext in STATIC_EXTENSIONS:
        file_path = os.path.join(FRONTEND_PUBLIC, filename)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return send_from_directory(FRONTEND_PUBLIC, filename)
    
    # For SPA routing, serve index.html for any non-API, non-static-file route
    index_path = os.path.join(FRONTEND_PUBLIC, 'index.html')
    if os.path.exists(index_path):
        return send_file(index_path)
    return jsonify({'error': 'Frontend not found'}), 404


# Serve index.html for root route
@app.route('/')
def serve_index():
    """Serve the main index.html file for the SPA."""
    index_path = os.path.join(FRONTEND_PUBLIC, 'index.html')
    if os.path.exists(index_path):
        return send_file(index_path)
    return jsonify({'error': 'Frontend not found'}), 404


if __name__ == '__main__':
    print(f"Frontend files served from: {FRONTEND_PUBLIC}")
    print(f"Server running on http://localhost:5000")
    app.run(port=5000, debug=True)

