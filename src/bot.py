"""
Bot Module

The main automation logic that coordinates screen capture and input.
This is where the "brains" of the automation lives.
"""

import time
import random
from typing import List, Tuple

import config
from src.screen_capture import ScreenCapture
from src.input_controller import InputController


class ClashBot:
    """
    Main bot class that automates Clash Royale actions.
    
    Current capabilities (Phase 1):
    - Continuously drag cards to target positions
    - Cycle through different drop locations
    
    Future capabilities:
    - Detect specific cards
    - Read elixir count
    - Make strategic decisions
    """
    
    def __init__(self):
        """Initialize the bot components."""
        self.screen = ScreenCapture()
        self.input = InputController(screen_capture=self.screen)
        self.running = False
        
        # Track which card/target we're on
        self.current_card = 0
        self.current_target = 0
        
    def setup(self) -> bool:
        """
        Set up the bot by finding the game window.
        
        Returns:
            True if setup successful, False otherwise.
        """
        print("=" * 50)
        print("CLASH ROYALE TEST AUTOMATION")
        print("=" * 50)
        print()
        
        if not self.screen.find_window():
            return False
        
        print()
        print("✓ Bot initialized successfully!")
        print()
        return True
    
    def deploy_card(self, card_slot: int = None, target: Tuple[float, float] = None):
        """
        Deploy a single card to a target position.
        
        Args:
            card_slot: Which card to deploy (0-3). If None, cycles through cards.
            target: Where to deploy (x_pct, y_pct). If None, cycles through targets.
        """
        # Use cycling if not specified
        if card_slot is None:
            card_slot = self.current_card
            self.current_card = (self.current_card + 1) % 4
            
        if target is None:
            target = config.DROP_TARGETS[self.current_target]
            self.current_target = (self.current_target + 1) % len(config.DROP_TARGETS)
        
        # Deploy the card
        self.input.drag_card_to_position(card_slot, target)
        
    def run_continuous(self, 
                       num_deploys: int = None,
                       delay: float = None,
                       randomize: bool = False):
        """
        Continuously deploy cards.
        
        Args:
            num_deploys: Number of cards to deploy. None = infinite
            delay: Seconds between deploys. Defaults to config.DEPLOY_DELAY
            randomize: If True, pick random cards and targets
        """
        delay = delay or config.DEPLOY_DELAY
        self.running = True
        deploy_count = 0
        
        print(f"\n🎮 Starting continuous deployment...")
        print(f"   Delay between deploys: {delay}s")
        print(f"   Total deploys: {'infinite' if num_deploys is None else num_deploys}")
        print(f"   Press Ctrl+C to stop")
        print()
        
        # Bring game to front
        self.screen.bring_to_front()
        time.sleep(0.5)
        
        try:
            while self.running:
                # Check if we've hit our limit
                if num_deploys is not None and deploy_count >= num_deploys:
                    print(f"\n✓ Completed {num_deploys} deploys")
                    break
                
                # Choose card and target
                if randomize:
                    card = random.randint(0, 3)
                    target = random.choice(config.DROP_TARGETS)
                else:
                    card = None  # Use cycling
                    target = None
                
                # Deploy!
                deploy_count += 1
                print(f"[Deploy #{deploy_count}]", end=" ")
                self.deploy_card(card_slot=card, target=target)
                
                # Wait before next deploy
                time.sleep(delay)
                
        except KeyboardInterrupt:
            print(f"\n\n⏹️  Stopped by user after {deploy_count} deploys")
            
        self.running = False
        
    def test_single_deploy(self):
        """
        Deploy a single card for testing.
        Useful for calibrating positions.
        """
        print("\n🧪 TEST: Single card deploy")
        print("   Card: Slot 1 (leftmost)")
        print("   Target: Left bridge")
        print()
        
        self.screen.bring_to_front()
        time.sleep(0.5)
        
        self.input.drag_card_to_bridge(card_slot=0, side="left")
        print("\n✓ Test complete!")

    def calibration_mode(self):
        """
        Interactive mode to help calibrate card and target positions.
        Press SPACE to capture mouse position, ESC to exit.
        """
        print("\n📐 CALIBRATION MODE")
        print("=" * 50)
        print("   Press SPACE to capture mouse position")
        print("   Press ESC to exit")
        print("=" * 50)
        print()
        print("   Hover your mouse over the scrcpy window and press SPACE...")
        print()
        
        import pyautogui
        import keyboard
        
        capture_count = 0
        
        try:
            while True:
                # Wait for spacebar
                event = keyboard.read_event()
                
                if event.event_type == 'down':
                    if event.name == 'space':
                        x, y = pyautogui.position()
                        capture_count += 1
                        
                        # Convert to percentages
                        if self.screen.window_rect:
                            left, top, right, bottom = self.screen.window_rect
                            width = right - left
                            height = bottom - top
                            
                            # Check if mouse is in window
                            if left <= x <= right and top <= y <= bottom:
                                x_pct = (x - left) / width
                                y_pct = (y - top) / height
                                print(f"   [{capture_count}] Pixel: ({x}, {y})")
                                print(f"       Percentage: ({x_pct:.3f}, {y_pct:.3f})")
                                print()
                            else:
                                print(f"   [{capture_count}] ⚠️  Mouse is outside the game window!")
                                print(f"       Raw position: ({x}, {y})")
                                print()
                        else:
                            print(f"   [{capture_count}] Position: ({x}, {y})")
                            print("       (Window not found - showing raw coordinates)")
                            print()
                            
                    elif event.name == 'esc':
                        print(f"\n   ✓ Captured {capture_count} positions. Exiting.")
                        break
                    
        except KeyboardInterrupt:
            print(f"\n   ✓ Captured {capture_count} positions. Exiting.")


# =============================================================================
# Standalone execution
# =============================================================================

if __name__ == "__main__":
    bot = ClashBot()
    
    if bot.setup():
        bot.test_single_deploy()