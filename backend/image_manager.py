"""
Image manager for storing captures with metadata.
"""
import os
import json
from datetime import datetime
from PIL import Image
from typing import List, Dict, Optional


class ImageManager:
    """Manages storage and retrieval of captured images with metadata."""
    
    def __init__(self, storage_dir: str = "captures"):
        """
        Initialize image manager.
        
        Args:
            storage_dir: Directory to store captures
        """
        self.storage_dir = storage_dir
        self.metadata_file = os.path.join(storage_dir, "metadata.json")
        
        # Create storage directory if it doesn't exist
        os.makedirs(storage_dir, exist_ok=True)
        
        # Initialize metadata file if it doesn't exist
        if not os.path.exists(self.metadata_file):
            self._save_metadata([])
    
    def save_capture(self, image: Image.Image, click_x: int, click_y: int, 
                    window_title: str, url: str = "") -> str:
        """
        Save a captured image with metadata.
        
        Args:
            image: PIL Image to save
            click_x: X coordinate of click
            click_y: Y coordinate of click
            window_title: Title of the window
            url: URL if it's a web page
            
        Returns:
            ID of the saved capture
        """
        # Generate unique ID based on timestamp
        capture_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        filename = f"{capture_id}.png"
        filepath = os.path.join(self.storage_dir, filename)
        
        # Save image
        image.save(filepath, "PNG")
        
        # Load existing metadata
        metadata = self._load_metadata()
        
        # Add new capture metadata
        capture_data = {
            'id': capture_id,
            'filename': filename,
            'timestamp': datetime.now().isoformat(),
            'click_x': click_x,
            'click_y': click_y,
            'window_title': window_title,
            'url': url,
            'context': ''  # User-added context text
        }
        
        metadata.append(capture_data)
        
        # Save updated metadata
        self._save_metadata(metadata)
        
        return capture_id
    
    def get_all_captures(self) -> List[Dict]:
        """
        Get all captures with metadata.
        
        Returns:
            List of capture dictionaries
        """
        return self._load_metadata()
    
    def get_capture(self, capture_id: str) -> Optional[Dict]:
        """
        Get a specific capture by ID.
        
        Args:
            capture_id: ID of the capture
            
        Returns:
            Capture dictionary or None if not found
        """
        metadata = self._load_metadata()
        for capture in metadata:
            if capture['id'] == capture_id:
                return capture
        return None
    
    def update_context(self, capture_id: str, context: str) -> bool:
        """
        Update context text for a capture.
        
        Args:
            capture_id: ID of the capture
            context: New context text
            
        Returns:
            True if updated, False if not found
        """
        metadata = self._load_metadata()
        for capture in metadata:
            if capture['id'] == capture_id:
                capture['context'] = context
                self._save_metadata(metadata)
                return True
        return False
    
    def get_image_path(self, capture_id: str) -> Optional[str]:
        """
        Get file path for a capture image.
        
        Args:
            capture_id: ID of the capture
            
        Returns:
            File path or None if not found
        """
        capture = self.get_capture(capture_id)
        if capture:
            return os.path.join(self.storage_dir, capture['filename'])
        return None
    
    def delete_capture(self, capture_id: str) -> bool:
        """
        Delete a capture and its image file.
        
        Args:
            capture_id: ID of the capture to delete
            
        Returns:
            True if deleted, False if not found
        """
        capture = self.get_capture(capture_id)
        if not capture:
            return False
        
        # Delete image file
        image_path = self.get_image_path(capture_id)
        if image_path and os.path.exists(image_path):
            try:
                os.remove(image_path)
            except OSError:
                pass  # Continue even if file deletion fails
        
        # Remove from metadata
        metadata = self._load_metadata()
        metadata = [c for c in metadata if c['id'] != capture_id]
        self._save_metadata(metadata)
        
        return True
    
    def _load_metadata(self) -> List[Dict]:
        """Load metadata from file."""
        if not os.path.exists(self.metadata_file):
            return []
        
        try:
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    
    def _save_metadata(self, metadata: List[Dict]):
        """Save metadata to file."""
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

