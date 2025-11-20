"""
Global mouse click detector using pynput.
Detects mouse clicks and triggers screen capture callbacks.
Requires Ctrl+Click to capture.
"""
import threading
from pynput import mouse, keyboard
from typing import Callable, Optional


class ClickDetector:
    """Detects global mouse clicks and triggers callbacks."""
    
    def __init__(self, on_click_callback: Callable[[int, int], None]):
        """
        Initialize the click detector.
        
        Args:
            on_click_callback: Function to call when a click is detected.
                              Receives (x, y) coordinates.
        """
        self.on_click_callback = on_click_callback
        self.mouse_listener: Optional[mouse.Listener] = None
        self.keyboard_listener: Optional[keyboard.Listener] = None
        self.is_running = False
        self.ctrl_pressed = False
        
    def _on_key_press(self, key):
        """Handle keyboard events to track Ctrl key."""
        try:
            if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                self.ctrl_pressed = True
        except AttributeError:
            pass
        return True
    
    def _on_key_release(self, key):
        """Handle keyboard events to track Ctrl key."""
        try:
            if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                self.ctrl_pressed = False
        except AttributeError:
            pass
        return True
        
    def _on_click(self, x, y, button, pressed):
        """Handle mouse click events."""
        if pressed and button == mouse.Button.left and self.ctrl_pressed:
            # Trigger callback on Ctrl+Left click
            self.on_click_callback(x, y)
        return True  # Continue listening
    
    def start(self):
        """Start listening for mouse clicks and keyboard."""
        if self.is_running:
            return
            
        # Start keyboard listener to track Ctrl key
        self.keyboard_listener = keyboard.Listener(
            on_press=self._on_key_press,
            on_release=self._on_key_release
        )
        self.keyboard_listener.start()
        
        # Start mouse listener
        self.mouse_listener = mouse.Listener(on_click=self._on_click)
        self.mouse_listener.start()
        self.is_running = True
        
    def stop(self):
        """Stop listening for mouse clicks and keyboard."""
        if self.mouse_listener:
            self.mouse_listener.stop()
            self.mouse_listener = None
        if self.keyboard_listener:
            self.keyboard_listener.stop()
            self.keyboard_listener = None
        self.is_running = False

