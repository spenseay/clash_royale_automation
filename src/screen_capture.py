"""
Screen Capture Module

Handles finding the scrcpy window and capturing screenshots.
This is the foundation for all image-based detection.
"""

import time
from typing import Optional, Tuple
from PIL import Image
import pyautogui

# Windows-specific imports for window management
try:
    import win32gui
    import win32con
    WINDOWS_AVAILABLE = True
except ImportError:
    WINDOWS_AVAILABLE = False
    print("Warning: pywin32 not available. Window management limited.")

import config


class ScreenCapture:
    """
    Manages the scrcpy window and captures screenshots.
    
    The workflow:
    1. Find the scrcpy window by title
    2. Get its position and size
    3. Capture screenshots of just that window
    """
    
    def __init__(self, window_title: str = None):
        """
        Initialize the screen capture.
        
        Args:
            window_title: The title of the scrcpy window to capture.
                         Defaults to config.SCRCPY_WINDOW_TITLE
        """
        self.window_title = window_title or config.SCRCPY_WINDOW_TITLE
        self.window_handle = None
        self.window_rect = None  # (left, top, right, bottom)
        
    def find_window(self) -> bool:
        """
        Find the scrcpy window by its title.
        
        Returns:
            True if window was found, False otherwise.
        """
        if not WINDOWS_AVAILABLE:
            print("Cannot find window: pywin32 not installed")
            return False
            
        def callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                # Match window title but exclude Command Prompt/PowerShell windows
                if self.window_title.lower() in title.lower():
                    title_lower = title.lower()
                    if "command prompt" not in title_lower and "cmd" not in title_lower and "powershell" not in title_lower:
                        windows.append(hwnd)
            return True
        
        windows = []
        win32gui.EnumWindows(callback, windows)
        
        if windows:
            self.window_handle = windows[0]
            self._update_window_rect()
            print(f"✓ Found window: '{win32gui.GetWindowText(self.window_handle)}'")
            print(f"  Position: {self.window_rect}")
            return True
        else:
            print(f"✗ Window not found: '{self.window_title}'")
            print("  Make sure scrcpy is running!")
            return False
    
    def _update_window_rect(self):
        """Update the stored window rectangle."""
        if self.window_handle:
            self.window_rect = win32gui.GetWindowRect(self.window_handle)
    
    def get_window_size(self) -> Optional[Tuple[int, int]]:
        """
        Get the current window size.
        
        Returns:
            (width, height) tuple, or None if window not found.
        """
        if not self.window_rect:
            return None
        left, top, right, bottom = self.window_rect
        return (right - left, bottom - top)
    
    def get_window_position(self) -> Optional[Tuple[int, int]]:
        """
        Get the current window position (top-left corner).
        
        Returns:
            (x, y) tuple, or None if window not found.
        """
        if not self.window_rect:
            return None
        return (self.window_rect[0], self.window_rect[1])
    
    def capture(self, save_path: str = None) -> Optional[Image.Image]:
        """
        Capture a screenshot of the scrcpy window.
        
        Args:
            save_path: If provided, save the screenshot to this path.
            
        Returns:
            PIL Image of the screenshot, or None if failed.
        """
        # Refresh window position in case it moved
        self._update_window_rect()
        
        if not self.window_rect:
            print("Cannot capture: window not found")
            return None
        
        left, top, right, bottom = self.window_rect
        width = right - left
        height = bottom - top
        
        # Capture the region
        screenshot = pyautogui.screenshot(region=(left, top, width, height))
        
        if save_path:
            screenshot.save(save_path)
            print(f"Screenshot saved: {save_path}")
        
        return screenshot
    
    def bring_to_front(self):
        """Bring the scrcpy window to the foreground."""
        if self.window_handle and WINDOWS_AVAILABLE:
            try:
                win32gui.SetForegroundWindow(self.window_handle)
                time.sleep(0.1)  # Brief pause to let it come to front
            except Exception as e:
                print(f"Could not bring window to front: {e}")
    
    def convert_percentage_to_pixels(self, x_pct: float, y_pct: float) -> Tuple[int, int]:
        """
        Convert percentage positions to actual pixel coordinates.
        
        This is useful because card/arena positions are stored as percentages
        to work across different screen sizes.
        
        Args:
            x_pct: X position as percentage (0.0 to 1.0)
            y_pct: Y position as percentage (0.0 to 1.0)
            
        Returns:
            (x, y) pixel coordinates relative to screen (not window).
        """
        if not self.window_rect:
            raise ValueError("Window not found. Call find_window() first.")
        
        left, top, right, bottom = self.window_rect
        width = right - left
        height = bottom - top
        
        x = left + int(width * x_pct)
        y = top + int(height * y_pct)
        
        return (x, y)


# =============================================================================
# Command-line interface for testing
# =============================================================================

if __name__ == "__main__":
    import argparse
    import os
    
    parser = argparse.ArgumentParser(description="Screen capture utility")
    parser.add_argument("--save-reference", action="store_true",
                       help="Save a reference screenshot")
    parser.add_argument("--output", "-o", default="reference_screenshot.png",
                       help="Output filename for screenshot")
    args = parser.parse_args()
    
    # Create screen capture instance
    capture = ScreenCapture()
    
    # Try to find the window
    if capture.find_window():
        print(f"\nWindow size: {capture.get_window_size()}")
        print(f"Window position: {capture.get_window_position()}")
        
        if args.save_reference:
            # Create debug directory if needed
            os.makedirs(config.SCREENSHOT_DIR, exist_ok=True)
            output_path = os.path.join(config.SCREENSHOT_DIR, args.output)
            
            # Capture and save
            capture.bring_to_front()
            time.sleep(0.5)  # Wait for window to be ready
            capture.capture(save_path=output_path)
            print(f"\n✓ Reference screenshot saved to: {output_path}")
    else:
        print("\nTip: Start scrcpy with:")
        print(f'  scrcpy --window-title="{config.SCRCPY_WINDOW_TITLE}"')