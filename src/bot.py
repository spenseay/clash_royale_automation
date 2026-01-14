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
from src.game_state import GameState, GameStateDetector, UIPositions


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
        self.state = GameStateDetector(screen_capture=self.screen)
        self.running = False
        
        # Track which card/target we're on
        self.current_card = 0
        self.current_target = 0
        
        # Game loop settings
        self.games_played = 0
        self.max_games = None  # None = infinite
        
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

    # =========================================================================
    # GAME LOOP METHODS
    # =========================================================================
    
    def click_position(self, position: Tuple[float, float], description: str = ""):
        """
        Click a position on screen (percentage-based).
        
        Args:
            position: (x_pct, y_pct) percentage position
            description: What we're clicking (for logging)
        """
        x, y = self.screen.convert_percentage_to_pixels(position[0], position[1])
        if description:
            print(f"   Clicking: {description}")
        self.input.click(x, y)
        
    def click_battle_button(self):
        """Click the battle button on the main menu."""
        print("⚔️  Clicking Battle button...")
        self.click_position(UIPositions.BATTLE_BUTTON, "Battle button")
    
    def click_play_again_button(self):
        """Click the Play Again button to start a new game."""
        print("   Clicking Play Again...")
        self.click_position(UIPositions.PLAY_AGAIN_BUTTON, "Play Again button")
        
    def click_ok_button(self):
        """Click OK button (goes to main menu)."""
        print("   Clicking OK...")
        self.click_position(UIPositions.OK_BUTTON, "OK button")
        
    def wait_for_battle_start(self, timeout: float = 30):
        """
        Wait for the battle to start.
        
        In test arena, this is usually instant.
        In real matches, there's matchmaking time.
        
        Args:
            timeout: Max seconds to wait
        """
        print("   Waiting for battle to start...")
        # For now, just wait a fixed amount
        # Future: detect the battle UI appearing
        time.sleep(5)
        print("   Battle started!")
        self.state.set_state(GameState.IN_BATTLE)
        
    def play_battle(self, 
                    max_duration: float = 300,
                    deploy_delay: float = None,
                    randomize: bool = True,
                    check_interval: int = 3,
                    skip_initial_checks: int = 5):
        """
        Play a single battle by deploying cards until game ends.
        
        Args:
            max_duration: Maximum battle length in seconds (safety limit)
            deploy_delay: Seconds between card deploys
            randomize: Randomize card/target selection
            check_interval: Check for battle end every N deploys
            skip_initial_checks: Don't check for game over until this many deploys
        """
        deploy_delay = deploy_delay or config.DEPLOY_DELAY
        start_time = time.time()
        deploy_count = 0
        
        print(f"\n🎮 Playing battle...")
        print(f"   Deploy delay: {deploy_delay}s")
        print(f"   Checking for battle end every {check_interval} deploys (after {skip_initial_checks} deploys)")
        print()
        
        while True:
            elapsed = time.time() - start_time
            
            # Safety limit - battles shouldn't last more than 5 min
            if elapsed > max_duration:
                print(f"\n   ⏰ Safety limit reached ({max_duration}s)")
                break
            
            # Deploy a card
            if randomize:
                card = random.randint(0, 3)
                target = random.choice(config.DROP_TARGETS)
            else:
                card = None
                target = None
                
            deploy_count += 1
            elapsed_str = f"{int(elapsed)}s"
            print(f"   [{elapsed_str}] Deploy #{deploy_count}", end=" ")
            self.deploy_card(card_slot=card, target=target)
            
            # Check if battle is over (skip first few deploys to avoid false positives)
            if deploy_count >= skip_initial_checks and deploy_count % check_interval == 0:
                print(f"   Checking game state...")
                if self.state.is_battle_over():
                    print(f"\n   🏁 Battle ended detected!")
                    break
            
            # Wait before next deploy
            time.sleep(deploy_delay)
        
        print(f"\n   Battle complete! Deployed {deploy_count} cards in {int(elapsed)}s")
        self.state.set_state(GameState.BATTLE_ENDED)
        return deploy_count
    
    def handle_battle_end(self, play_again: bool = True):
        """
        Handle the post-battle screen.
        
        Args:
            play_again: If True, click Play Again. If False, click OK to go to menu.
        """
        print("\n🏁 Battle ended!")
        
        # Wait for end screen to fully appear
        time.sleep(2)
        
        if play_again:
            self.click_play_again_button()
            print("   Waiting for new game to load...")
            time.sleep(5)  # Wait longer for new game to load
            
            # Verify the Play Again button is gone (new game started)
            if self.state.is_battle_over():
                print("   ⚠️ Still on end screen, clicking again...")
                self.click_play_again_button()
                time.sleep(5)
            
            print("   New game ready!")
            self.state.set_state(GameState.IN_BATTLE)
        else:
            self.click_ok_button()
            time.sleep(2)
            # Sometimes there are multiple screens to dismiss
            if self.state.is_battle_over():
                self.click_ok_button()
                time.sleep(2)
            print("   Returned to menu")
            self.state.set_state(GameState.MAIN_MENU)
    
    def run_game_loop(self, 
                      num_games: int = None,
                      battle_duration: float = 180,
                      deploy_delay: float = None):
        """
        Run the full game loop: Menu → Battle → Play → End → Repeat
        
        Args:
            num_games: Number of games to play. None = infinite
            battle_duration: How long to play each battle (seconds)
            deploy_delay: Seconds between card deploys
        """
        self.running = True
        self.games_played = 0
        self.max_games = num_games
        
        print("\n" + "=" * 50)
        print("🤖 STARTING GAME LOOP")
        print("=" * 50)
        print(f"   Games to play: {'infinite' if num_games is None else num_games}")
        print(f"   Battle duration: {battle_duration}s")
        print(f"   Press Ctrl+C to stop")
        print()
        
        # Bring game to front
        self.screen.bring_to_front()
        time.sleep(1)
        
        try:
            while self.running:
                # Check if we've hit our game limit
                if num_games is not None and self.games_played >= num_games:
                    print(f"\n✓ Completed {num_games} games!")
                    break
                
                self.games_played += 1
                print(f"\n{'='*50}")
                print(f"📍 GAME {self.games_played}" + (f" of {num_games}" if num_games else ""))
                print(f"{'='*50}")
                
                # First game: need to click Battle button from main menu
                # Subsequent games: we're already in battle from "Play Again"
                if self.games_played == 1:
                    self.click_battle_button()
                    self.wait_for_battle_start()
                else:
                    # Already starting from Play Again click
                    print("   New battle starting...")
                    time.sleep(2)
                
                # Play the battle
                self.play_battle(
                    max_duration=battle_duration,
                    deploy_delay=deploy_delay
                )
                
                # Handle end screen (clicks Play Again for next game)
                is_last_game = (num_games is not None and self.games_played >= num_games)
                self.handle_battle_end(play_again=not is_last_game)
                
        except KeyboardInterrupt:
            print(f"\n\n⏹️  Stopped by user after {self.games_played} games")
        
        self.running = False
        print("\n🏁 Game loop ended.")


# =============================================================================
# Standalone execution
# =============================================================================

if __name__ == "__main__":
    bot = ClashBot()
    
    if bot.setup():
        bot.test_single_deploy()