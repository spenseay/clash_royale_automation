"""
Configuration settings for Clash Royale automation.

Adjust these values based on your screen resolution and scrcpy window size.
"""

# =============================================================================
# WINDOW SETTINGS
# =============================================================================

# The title of your scrcpy window (must match exactly)
SCRCPY_WINDOW_TITLE = "ClashRoyale"

# If you want to use a specific window size, set these (None = auto-detect)
WINDOW_WIDTH = None
WINDOW_HEIGHT = None


# =============================================================================
# CARD POSITIONS (as percentages of window size)
# =============================================================================

# Cards are at the bottom of the screen
# These are approximate positions - you may need to fine-tune them

# Y position of card slots (percentage from top)
CARD_SLOT_Y = 0.88  # ~88% down from top (averaged from your readings)

# X positions of the 4 card slots (percentage from left)
CARD_SLOT_X = [
    0.331,  # Card 1 (leftmost)
    0.504,  # Card 2
    0.665,  # Card 3
    0.824,  # Card 4 (rightmost)
]

# Next card position (the small one on the side)
NEXT_CARD_X = 0.22
NEXT_CARD_Y = 0.92


# =============================================================================
# ARENA POSITIONS (drop zones)
# =============================================================================

# Arena boundaries (percentage of window)
ARENA_TOP = 0.15
ARENA_BOTTOM = 0.75
ARENA_LEFT = 0.10
ARENA_RIGHT = 0.90

# Bridge positions (common drop zones)
LEFT_BRIDGE = (0.25, 0.50)   # (x%, y%)
RIGHT_BRIDGE = (0.75, 0.50)

# Behind king tower
BEHIND_KING = (0.50, 0.70)

# Default drop targets for testing
DROP_TARGETS = [
    (0.589, 0.532),  # Your calibrated drop position
    LEFT_BRIDGE,
    RIGHT_BRIDGE,
    (0.50, 0.45),    # Center
    (0.30, 0.55),    # Left side
    (0.70, 0.55),    # Right side
]


# =============================================================================
# TIMING SETTINGS
# =============================================================================

# How long to wait between card deployments (seconds)
DEPLOY_DELAY = 3.0

# How long the drag action takes (seconds)
DRAG_DURATION = 0.3

# Pause after each action (seconds)
ACTION_PAUSE = 0.5

# Emergency stop hotkey
EMERGENCY_STOP_KEY = "escape"


# =============================================================================
# IMAGE RECOGNITION SETTINGS
# =============================================================================

# Confidence threshold for template matching (0.0 to 1.0)
# Higher = more strict matching, Lower = more lenient
MATCH_CONFIDENCE = 0.8

# Path to template images
TEMPLATES_DIR = "assets/templates"


# =============================================================================
# DEBUG SETTINGS
# =============================================================================

# Show debug windows with detected regions
DEBUG_MODE = True

# Save screenshots for debugging
SAVE_SCREENSHOTS = True
SCREENSHOT_DIR = "debug_screenshots"