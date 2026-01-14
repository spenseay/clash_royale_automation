"""
Diagnostic script to check window detection
"""
import win32gui
import pyautogui
import keyboard
import time

def find_all_windows_with_title(search_text):
    """Find all windows containing search_text in title."""
    windows = []
    
    def callback(hwnd, results):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if search_text.lower() in title.lower():
                rect = win32gui.GetWindowRect(hwnd)
                results.append({
                    'hwnd': hwnd,
                    'title': title,
                    'rect': rect
                })
        return True
    
    win32gui.EnumWindows(callback, windows)
    return windows

print("=" * 60)
print("WINDOW DIAGNOSTIC")
print("=" * 60)

# Find windows
windows = find_all_windows_with_title("ClashRoyale")

if not windows:
    print("\n❌ No windows found with 'ClashRoyale' in title!")
    print("\nLet's search for 'scrcpy' instead...")
    windows = find_all_windows_with_title("scrcpy")

if not windows:
    print("\n❌ No windows found with 'scrcpy' either!")
    print("\nListing ALL visible windows with their titles...")
    
    all_windows = []
    def list_all(hwnd, results):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:  # Only windows with titles
                results.append(title)
        return True
    win32gui.EnumWindows(list_all, all_windows)
    
    print("\nVisible windows:")
    for w in all_windows[:20]:  # First 20
        print(f"  - {w}")
else:
    print(f"\n✓ Found {len(windows)} matching window(s):\n")
    
    for i, w in enumerate(windows):
        left, top, right, bottom = w['rect']
        width = right - left
        height = bottom - top
        print(f"  Window {i+1}:")
        print(f"    Title: '{w['title']}'")
        print(f"    Position: ({left}, {top})")
        print(f"    Size: {width} x {height}")
        print(f"    Bounds: left={left}, top={top}, right={right}, bottom={bottom}")
        print()

    # Use the first window for testing
    target = windows[0]
    left, top, right, bottom = target['rect']
    
    print("=" * 60)
    print("MOUSE POSITION TEST")
    print("Press SPACE to check mouse position, ESC to quit")
    print("=" * 60)
    print()
    
    while True:
        event = keyboard.read_event()
        if event.event_type == 'down':
            if event.name == 'space':
                x, y = pyautogui.position()
                
                in_window = left <= x <= right and top <= y <= bottom
                
                print(f"Mouse at: ({x}, {y})")
                print(f"Window bounds: x=[{left} to {right}], y=[{top} to {bottom}]")
                print(f"In window: {in_window}")
                
                if in_window:
                    x_pct = (x - left) / (right - left)
                    y_pct = (y - top) / (bottom - top)
                    print(f"Percentage: ({x_pct:.3f}, {y_pct:.3f})")
                print()
                
            elif event.name == 'esc':
                print("Exiting.")
                break