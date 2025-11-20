"""
Flask API server for DocuGener.
Provides REST endpoints for captures, context updates, export, and pause/resume.
"""
import os
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from image_manager import ImageManager
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from pptx import Presentation
from pptx.util import Inches
import tempfile


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*", "methods": ["GET", "POST", "DELETE", "OPTIONS"]}})  # Enable CORS for frontend

# Global state
image_manager = ImageManager()
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
        
        # Create slide with title
        slide = prs.slides.add_slide(prs.slide_layouts[5])  # Blank layout
        
        # Add image
        left = Inches(0.5)
        top = Inches(1)
        width = Inches(9)
        height = Inches(5)
        slide.shapes.add_picture(image_path, left, top, width, height)
        
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
    
    doc = SimpleDocTemplate(temp_file.name, pagesize=letter)
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
        
        # Add image
        img = RLImage(image_path, width=7*inch, height=5*inch)
        story.append(img)
        story.append(Spacer(1, 0.2*inch))
        
        # Add context
        if capture.get('context'):
            story.append(Paragraph(capture['context'], context_style))
        
        story.append(Spacer(1, 0.5*inch))
    
    doc.build(story)
    
    return send_file(
        temp_file.name,
        mimetype='application/pdf',
        as_attachment=True,
        download_name='docugener_export.pdf'
    )


if __name__ == '__main__':
    app.run(port=5000, debug=True)

