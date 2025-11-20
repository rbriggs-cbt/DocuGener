"""
Main entry point for the DocuGener application.
Initializes click detector, screen capture, and API server.
"""
import threading
import time
from click_detector import ClickDetector
from screen_capture import ScreenCapture
from window_info import WindowInfo
from image_manager import ImageManager
from api_server import app, is_paused
import os


# Global components
screen_capture = ScreenCapture()
window_info = WindowInfo()
image_manager = ImageManager()


def on_click_detected(x, y):
    """Callback when a click is detected."""
    global is_paused
    
    # Check if paused
    if is_paused:
        return
    
    try:
        # Get window information
        window_data = window_info.get_window_at_point(x, y)
        window_title = window_data.get('title', 'Unknown Window')
        url = window_data.get('url', '')
        
        # Small delay to ensure window state is updated
        time.sleep(0.1)
        
        # Capture screen with highlight
        image = screen_capture.capture_with_highlight(x, y)
        
        # Save capture
        capture_id = image_manager.save_capture(
            image=image,
            click_x=x,
            click_y=y,
            window_title=window_title,
            url=url
        )
        
        print(f"Capture saved: {capture_id} - {window_title}")
        
    except Exception as e:
        print(f"Error capturing screenshot: {e}")


def main():
    """Main function to start the application."""
    print("Starting DocuGener...")
    print("Click detection is active. Press Ctrl+Click to capture screenshots.")
    print("Press Ctrl+C to stop.")
    print("Web interface available at http://localhost:5000")
    
    # Initialize click detector
    click_detector = ClickDetector(on_click_detected)
    click_detector.start()
    
    # Start API server in a separate thread
    api_thread = threading.Thread(
        target=lambda: app.run(port=5000, debug=False, use_reloader=False),
        daemon=True
    )
    api_thread.start()
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping...")
        click_detector.stop()
        print("Stopped.")


if __name__ == '__main__':
    main()

