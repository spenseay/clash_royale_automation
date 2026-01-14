"""
Game State Module

Detects what screen/state the game is currently in:
- Main menu
- In battle
- Battle ended (victory/defeat)

Uses image recognition (template matching) to detect UI elements.
"""

import os
import time
from enum import Enum
from typing import Optional, Tuple
import cv2
import numpy as np
from PIL import Image

import config


class GameState(Enum):
    """Possible game states we care about."""
    UNKNOWN = "unknown"
    MAIN_MENU = "main_menu"
    IN_BATTLE = "in_battle"
    BATTLE_ENDED = "battle_ended"


class GameStateDetector:
    """
    Detects the current game state using image recognition.
    
    Uses OpenCV template matching to find UI elements like:
    - Victory/Defeat banners (to detect battle end)
    - Battle button (to detect main menu)
    - Card tray (to detect in-battle)
    """
    
    def __init__(self, screen_capture=None):
        """
        Initialize the detector.
        
        Args:
            screen_capture: ScreenCapture instance for taking screenshots.
        """
        self.screen = screen_capture
        self.current_state = GameState.UNKNOWN
        self.battle_start_time = None
        
        # Template images (loaded on demand)
        self.templates = {}
        self.templates_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            "assets", "templates"
        )
        
    def load_template(self, name: str) -> Optional[np.ndarray]:
        """
        Load a template image for matching.
        
        Args:
            name: Template name (e.g., "victory", "defeat", "battle_button")
            
        Returns:
            OpenCV image array, or None if not found.
        """
        if name in self.templates:
            return self.templates[name]
        
        # Try common image extensions
        for ext in ['.png', '.jpg', '.jpeg']:
            path = os.path.join(self.templates_dir, f"{name}{ext}")
            if os.path.exists(path):
                template = cv2.imread(path)
                if template is not None:
                    self.templates[name] = template
                    print(f"   Loaded template: {name}")
                    return template
        
        return None
    
    def find_template(self, 
                      screenshot: Image.Image, 
                      template_name: str,
                      confidence: float = 0.8) -> Optional[Tuple[int, int, float]]:
        """
        Search for a template image within a screenshot.
        
        Args:
            screenshot: PIL Image to search in
            template_name: Name of template to search for
            confidence: Minimum match confidence (0.0 to 1.0)
            
        Returns:
            (x, y, confidence) of best match, or None if not found.
        """
        template = self.load_template(template_name)
        if template is None:
            return None
        
        # Convert PIL to OpenCV format
        screen_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        # Perform template matching
        result = cv2.matchTemplate(screen_cv, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= confidence:
            return (max_loc[0], max_loc[1], max_val)
        
        return None
    
    def detect_state(self) -> GameState:
        """
        Analyze current screenshot to determine game state.
        
        Returns:
            Detected GameState
        """
        if not self.screen:
            return GameState.UNKNOWN
        
        screenshot = self.screen.capture()
        if screenshot is None:
            return GameState.UNKNOWN
        
        # Check for battle end (OK button visible)
        ok_button = self.find_template(screenshot, "ok_button", confidence=0.7)
        if ok_button:
            print(f"   🏁 Game over screen detected! (confidence: {ok_button[2]:.2f})")
            self.current_state = GameState.BATTLE_ENDED
            return GameState.BATTLE_ENDED
        
        # Check for main menu (battle button visible)
        battle_btn = self.find_template(screenshot, "battle_button", confidence=0.7)
        if battle_btn:
            self.current_state = GameState.MAIN_MENU
            return GameState.MAIN_MENU
        
        # If none of the above, assume we're in battle
        if self.current_state == GameState.IN_BATTLE:
            return GameState.IN_BATTLE
        
        return GameState.UNKNOWN
    
    def is_battle_over(self) -> bool:
        """
        Quick check if the battle has ended.
        Looks for the Play Again or OK button that appears on the end-game screen.
        
        Returns:
            True if end-game screen is detected.
        """
        if not self.screen:
            return False
            
        screenshot = self.screen.capture()
        if screenshot is None:
            return False
        
        # Look for the Play Again button (appears on end screen)
        play_again = self.find_template(screenshot, "play_again", confidence=0.7)
        if play_again:
            print(f"   ✓ Play Again button detected! (confidence: {play_again[2]:.2f})")
            self.current_state = GameState.BATTLE_ENDED
            return True
        
        # Also check for OK button as backup
        ok_button = self.find_template(screenshot, "ok_button", confidence=0.7)
        if ok_button:
            print(f"   ✓ OK button detected! (confidence: {ok_button[2]:.2f})")
            self.current_state = GameState.BATTLE_ENDED
            return True
            
        return False
    
    def set_state(self, state: GameState):
        """Manually set the current state."""
        self.current_state = state
        print(f"   State → {state.value}")
        
        if state == GameState.IN_BATTLE:
            self.battle_start_time = time.time()
            
    def get_battle_duration(self) -> float:
        """Get how long the current battle has been going (seconds)."""
        if self.battle_start_time:
            return time.time() - self.battle_start_time
        return 0


# =============================================================================
# Button/UI Positions (calibrated for your screen)
# =============================================================================

class UIPositions:
    """
    Screen positions for various UI elements.
    All values are percentages (0.0 to 1.0).
    """
    
    # Main menu - calibrated!
    BATTLE_BUTTON = (0.531, 0.774)
    
    # Post-battle buttons
    OK_BUTTON = (0.55, 0.92)       # Right button - goes to main menu
    PLAY_AGAIN_BUTTON = (0.28, 0.92)  # Left button - starts new game
    
    @classmethod
    def set_battle_button(cls, x: float, y: float):
        """Update battle button position."""
        cls.BATTLE_BUTTON = (x, y)
        
    @classmethod
    def set_ok_button(cls, x: float, y: float):
        """Update OK button position."""
        cls.OK_BUTTON = (x, y)
        
    @classmethod
    def set_play_again_button(cls, x: float, y: float):
        """Update Play Again button position."""
        cls.PLAY_AGAIN_BUTTON = (x, y)