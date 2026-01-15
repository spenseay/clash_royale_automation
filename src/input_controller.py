"""
Input Controller Module

Handles simulating mouse inputs to control the game.
In scrcpy, mouse drags translate to touch drags on the device.
"""

import time
import pyautogui
from typing import Tuple

import config


# Configure PyAutoGUI safety features
pyautogui.FAILSAFE = True  # Move mouse to corner to abort
pyautogui.PAUSE = 0.1      # Small pause between actions


class InputController:
    """
    Controls mouse input for interacting with the game through scrcpy.
    
    Key concept: When you drag the mouse in the scrcpy window,
    it simulates a touch drag on your tablet.
    """
    
    def __init__(self, screen_capture=None):
        """
        Initialize the input controller.
        
        Args:
            screen_capture: Optional ScreenCapture instance for coordinate conversion.
        """
        self.screen_capture = screen_capture
        
    def click(self, x: int, y: int):
        """
        Perform a single click at the specified coordinates.
        
        Args:
            x: X pixel coordinate (screen coordinates)
            y: Y pixel coordinate (screen coordinates)
        """
        pyautogui.click(x, y)
        print(f"Clicked at ({x}, {y})")
        
    def drag(self, 
             start: Tuple[int, int], 
             end: Tuple[int, int], 
             duration: float = None):
        """
        Perform a drag from start to end position.
        
        This is the core action for deploying cards!
        
        Args:
            start: (x, y) starting position in screen pixels
            end: (x, y) ending position in screen pixels  
            duration: How long the drag takes (seconds). 
                     Defaults to config.DRAG_DURATION
        """
        duration = duration or config.DRAG_DURATION
        
        start_x, start_y = start
        end_x, end_y = end
        
        print(f"Dragging: ({start_x}, {start_y}) → ({end_x}, {end_y})")
        
        # Move to start position first
        pyautogui.moveTo(start_x, start_y)
        time.sleep(0.05)
        
        # Perform the drag
        pyautogui.drag(
            end_x - start_x,  # x offset
            end_y - start_y,  # y offset
            duration=duration,
            button='left'
        )
        
        time.sleep(config.ACTION_PAUSE)
        
    def drag_card_to_position(self, 
                               card_slot: int, 
                               target: Tuple[float, float],
                               card_offset: Tuple[float, float] = (0, 0),
                               duration: float = None):
        """
        Drag a card from its slot to a target position.
        
        This is a higher-level function that uses percentage-based positions.
        
        Args:
            card_slot: Which card slot (0-3, left to right)
            target: (x_pct, y_pct) target position as percentages
            card_offset: (x_offset, y_offset) to add to card position for variation
            duration: Drag duration (None = use config default)
        """
        if not self.screen_capture:
            raise ValueError("ScreenCapture required for percentage-based positioning")
        
        if card_slot < 0 or card_slot > 3:
            raise ValueError("card_slot must be 0-3")
        
        # Get card position with optional offset
        card_x_pct = config.CARD_SLOT_X[card_slot] + card_offset[0]
        card_y_pct = config.CARD_SLOT_Y + card_offset[1]
        
        # Convert to pixels
        start = self.screen_capture.convert_percentage_to_pixels(card_x_pct, card_y_pct)
        end = self.screen_capture.convert_percentage_to_pixels(target[0], target[1])
        
        print(f"Deploying card {card_slot + 1} to target ({target[0]:.2f}, {target[1]:.2f})")
        self.drag(start, end, duration=duration)
        
    def drag_card_to_bridge(self, card_slot: int, side: str = "left"):
        """
        Convenience function to drag a card to a bridge.
        
        Args:
            card_slot: Which card slot (0-3)
            side: "left" or "right" bridge
        """
        target = config.LEFT_BRIDGE if side == "left" else config.RIGHT_BRIDGE
        self.drag_card_to_position(card_slot, target)


# =============================================================================
# Command-line interface for testing
# =============================================================================

if __name__ == "__main__":
    import argparse
    from screen_capture import ScreenCapture
    
    parser = argparse.ArgumentParser(description="Input controller test")
    parser.add_argument("--test-drag", action="store_true",
                       help="Test a card drag action")
    parser.add_argument("--card", type=int, default=0, choices=[0,1,2,3],
                       help="Card slot to drag (0-3)")
    parser.add_argument("--side", choices=["left", "right"], default="left",
                       help="Which bridge to target")
    args = parser.parse_args()
    
    # Set up
    capture = ScreenCapture()
    if not capture.find_window():
        print("Cannot test: scrcpy window not found")
        exit(1)
    
    controller = InputController(screen_capture=capture)
    
    if args.test_drag:
        print("\n⚠️  Starting drag test in 3 seconds...")
        print("   Move mouse to corner to abort (failsafe)")
        time.sleep(3)
        
        capture.bring_to_front()
        time.sleep(0.5)
        
        controller.drag_card_to_bridge(args.card, args.side)
        print("✓ Drag complete!")