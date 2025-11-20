"""
Window information detection for Windows.
Gets window title and web URL for browser windows.
"""
import win32gui
import re


class WindowInfo:
    """Detects window title and web URL information."""
    
    def __init__(self):
        """Initialize window info detector."""
        pass
    
    def get_active_window_info(self) -> dict:
        """
        Get information about the currently active window.
        
        Returns:
            Dictionary with 'title' and 'url' keys
        """
        hwnd = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(hwnd)
        
        # Try to get URL for browser windows
        url = self._get_browser_url(hwnd, title)
        
        return {
            'title': title,
            'url': url
        }
    
    def _get_browser_url(self, hwnd, title) -> str:
        """
        Attempt to get URL from browser windows.
        
        Args:
            hwnd: Window handle
            title: Window title
            
        Returns:
            URL string or empty string if not found
        """
        # Check if it's a browser window by title
        browser_patterns = [
            r'chrome',
            r'edge',
            r'firefox',
            r'opera',
            r'safari',
            r'brave'
        ]
        
        is_browser = any(re.search(pattern, title, re.IGNORECASE) for pattern in browser_patterns)
        
        if not is_browser:
            return ""
        
        # Try to extract URL from window title (many browsers include it)
        # Format: "Page Title - Browser Name" or "Page Title | URL"
        url_patterns = [
            r'https?://[^\s]+',
            r'www\.[^\s]+',
        ]
        
        for pattern in url_patterns:
            match = re.search(pattern, title)
            if match:
                url = match.group(0)
                if not url.startswith('http'):
                    url = 'https://' + url
                return url
        
        # Alternative: Try using Windows UI Automation (more complex)
        # For now, return empty if URL not found in title
        return ""
    
    def get_window_at_point(self, x: int, y: int) -> dict:
        """
        Get window information at a specific screen point.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            Dictionary with 'title' and 'url' keys
        """
        hwnd = win32gui.WindowFromPoint((x, y))
        if hwnd:
            title = win32gui.GetWindowText(hwnd)
            url = self._get_browser_url(hwnd, title)
            return {
                'title': title,
                'url': url
            }
        return {'title': '', 'url': ''}

