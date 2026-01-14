"""
Template Capture Tool

Captures screenshots for use as templates in image recognition.
Helps you save reference images of victory screens, defeat screens, etc.

Usage:
    python capture_template.py --name victory
    python capture_template.py --name defeat
    python capture_template.py --name battle_button
"""

import os
import sys
import time
import argparse
import keyboard
import pyautogui

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.screen_capture import ScreenCapture


def capture_region(screen: ScreenCapture, name: str, output_dir: str):
    """
    Interactive tool to capture a region of the screen.
    
    Press SPACE to capture corner 1, then SPACE again for corner 2.
    """
    print(f"\n📸 TEMPLATE CAPTURE: {name}")
    print("=" * 50)
    print("  1. Position mouse at TOP-LEFT corner of the element")
    print("  2. Press SPACE")
    print("  3. Position mouse at BOTTOM-RIGHT corner")
    print("  4. Press SPACE again")
    print("  5. Template will be saved!")
    print()
    print("  Press ESC to cancel")
    print("=" * 50)
    print()
    
    corner1 = None
    corner2 = None
    
    while True:
        event = keyboard.read_event()
        
        if event.event_type == 'down':
            if event.name == 'escape':
                print("  Cancelled.")
                return None
                
            elif event.name == 'space':
                x, y = pyautogui.position()
                
                if corner1 is None:
                    corner1 = (x, y)
                    print(f"  ✓ Corner 1: ({x}, {y})")
                    print("    Now move to BOTTOM-RIGHT corner and press SPACE...")
                else:
                    corner2 = (x, y)
                    print(f"  ✓ Corner 2: ({x}, {y})")
                    break
    
    # Ensure corner1 is top-left and corner2 is bottom-right
    left = min(corner1[0], corner2[0])
    top = min(corner1[1], corner2[1])
    right = max(corner1[0], corner2[0])
    bottom = max(corner1[1], corner2[1])
    
    width = right - left
    height = bottom - top
    
    print(f"\n  Capturing region: ({left}, {top}) to ({right}, {bottom})")
    print(f"  Size: {width} x {height} pixels")
    
    # Capture the region
    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    
    # Save it
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{name}.png")
    screenshot.save(output_path)
    
    print(f"\n  ✓ Saved: {output_path}")
    return output_path


def capture_full_screenshot(screen: ScreenCapture, name: str, output_dir: str):
    """
    Capture full scrcpy window screenshot.
    Press SPACE when ready.
    """
    print(f"\n📸 FULL SCREENSHOT: {name}")
    print("=" * 50)
    print("  Press SPACE to capture the current screen")
    print("  Press ESC to cancel")
    print("=" * 50)
    print()
    
    while True:
        event = keyboard.read_event()
        
        if event.event_type == 'down':
            if event.name == 'escape':
                print("  Cancelled.")
                return None
            elif event.name == 'space':
                break
    
    # Capture
    screen.bring_to_front()
    time.sleep(0.2)
    
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{name}.png")
    screenshot = screen.capture(save_path=output_path)
    
    if screenshot:
        print(f"\n  ✓ Saved: {output_path}")
        return output_path
    else:
        print("\n  ✗ Failed to capture screenshot")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Capture template images for game state detection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python capture_template.py --name victory
    python capture_template.py --name defeat  
    python capture_template.py --name battle_button
    python capture_template.py --name victory --full  # Full screen, not region

Tips:
    - For victory/defeat: Capture just the word or a distinctive icon
    - Smaller templates match faster and more reliably
    - Avoid capturing areas that might change (like your username)
        """
    )
    
    parser.add_argument("--name", "-n", required=True,
                       help="Name for the template (e.g., victory, defeat)")
    parser.add_argument("--full", "-f", action="store_true",
                       help="Capture full window instead of a region")
    parser.add_argument("--output", "-o", default="assets/templates",
                       help="Output directory (default: assets/templates)")
    
    args = parser.parse_args()
    
    # Set up screen capture
    screen = ScreenCapture()
    if not screen.find_window():
        print("\n❌ scrcpy window not found. Make sure it's running!")
        sys.exit(1)
    
    # Capture
    if args.full:
        capture_full_screenshot(screen, args.name, args.output)
    else:
        capture_region(screen, args.name, args.output)


if __name__ == "__main__":
    main()