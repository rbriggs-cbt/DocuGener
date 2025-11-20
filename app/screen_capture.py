"""
Screen capture functionality with click pointer highlight overlay.
"""
import pyautogui
from PIL import Image, ImageDraw
import threading


class ScreenCapture:
    """Handles screen capture with click pointer highlight."""
    
    def __init__(self):
        """Initialize screen capture."""
        # Use a lock to ensure thread-safe capture
        self._lock = threading.Lock()
    
    def capture_with_highlight(self, click_x: int, click_y: int) -> Image.Image:
        """
        Capture the entire screen and add a click pointer highlight.
        
        Args:
            click_x: X coordinate of the click
            click_y: Y coordinate of the click
            
        Returns:
            PIL Image with click highlight overlay
        """
        # Use lock to ensure thread-safe capture
        with self._lock:
            # Capture entire screen using pyautogui (thread-safe)
            screenshot = pyautogui.screenshot()
            img = screenshot.copy()
        
        # Add click pointer highlight
        img = self._add_click_highlight(img, click_x, click_y)
        
        return img
    
    def _add_click_highlight(self, img: Image.Image, x: int, y: int) -> Image.Image:
        """
        Add a visible click pointer highlight to the image.
        
        Args:
            img: PIL Image to modify
            x: X coordinate of click
            y: Y coordinate of click
            
        Returns:
            Modified PIL Image with highlight
        """
        # Convert to RGBA for alpha blending
        if img.mode != 'RGBA':
            img_with_highlight = img.convert('RGBA')
        else:
            img_with_highlight = img.copy()
        
        # Create overlay for highlight
        overlay = Image.new('RGBA', img_with_highlight.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Draw outer circle (white/light) for visibility on dark backgrounds
        outer_radius = 25
        draw.ellipse(
            [x - outer_radius, y - outer_radius, x + outer_radius, y + outer_radius],
            fill=(255, 255, 255, 180),
            outline=(255, 255, 255, 255),
            width=3
        )
        
        # Draw inner circle (red) for visibility on light backgrounds
        inner_radius = 15
        draw.ellipse(
            [x - inner_radius, y - inner_radius, x + inner_radius, y + inner_radius],
            fill=(255, 0, 0, 200),
            outline=(255, 0, 0, 255),
            width=2
        )
        
        # Draw center dot
        dot_radius = 5
        draw.ellipse(
            [x - dot_radius, y - dot_radius, x + dot_radius, y + dot_radius],
            fill=(255, 255, 255, 255)
        )
        
        # Composite overlay onto image
        img_with_highlight = Image.alpha_composite(img_with_highlight, overlay)
        
        # Convert back to RGB for saving
        return img_with_highlight.convert('RGB')

