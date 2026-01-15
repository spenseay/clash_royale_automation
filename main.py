"""
Clash Royale Test Automation - Main Entry Point

Usage:
    python main.py              # Run continuous deployment (legacy)
    python main.py --test       # Single deploy test
    python main.py --calibrate  # Position calibration mode
    python main.py --loop       # Full game loop (menu → battle → repeat)
    python main.py --loop -n 5  # Play 5 games then stop
"""

import argparse
import sys

from src.bot import ClashBot
from src.game_state import UIPositions


def main():
    parser = argparse.ArgumentParser(
        description="Clash Royale Test Arena Automation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python main.py --test              # Test single card deploy  
    python main.py --calibrate         # Find positions for config
    python main.py --loop              # Full game loop (infinite)
    python main.py --loop -n 5         # Play 5 games
    python main.py --loop --duration 120  # 2-minute battles
    python main.py --count 20          # Deploy 20 cards (no game loop)
    python main.py --random            # Randomize card/target selection
    
Calibration positions needed:
    --battle-pos X Y    Set battle button position (e.g., --battle-pos 0.5 0.85)
    --ok-pos X Y        Set OK button position (e.g., --ok-pos 0.5 0.75)
        """
    )
    
    # Mode selection
    parser.add_argument("--test", "-t", action="store_true",
                       help="Run a single test deploy")
    parser.add_argument("--calibrate", "-c", action="store_true",
                       help="Enter calibration mode to find positions")
    parser.add_argument("--loop", "-l", action="store_true",
                       help="Run full game loop (menu → battle → repeat)")
    
    # Game loop options
    parser.add_argument("--count", "-n", type=int, default=None,
                       help="Number of cards to deploy OR games to play (with --loop)")
    parser.add_argument("--delay", "-d", type=float, default=None,
                       help="Base delay between deploys in seconds")
    parser.add_argument("--duration", type=float, default=180,
                       help="Battle duration in seconds (default: 180)")
    parser.add_argument("--random", "-r", action="store_true",
                       help="Randomize card and target selection")
    parser.add_argument("--no-humanize", action="store_true",
                       help="Disable human-like randomness (use exact timing/positions)")
    
    # Position overrides
    parser.add_argument("--battle-pos", nargs=2, type=float, metavar=('X', 'Y'),
                       help="Battle button position as percentages (e.g., 0.5 0.85)")
    parser.add_argument("--ok-pos", nargs=2, type=float, metavar=('X', 'Y'),
                       help="OK button position as percentages (e.g., 0.5 0.75)")
    
    args = parser.parse_args()
    
    # Apply position overrides
    if args.battle_pos:
        UIPositions.set_battle_button(args.battle_pos[0], args.battle_pos[1])
        print(f"Battle button position set to: {args.battle_pos}")
    if args.ok_pos:
        UIPositions.set_ok_button(args.ok_pos[0], args.ok_pos[1])
        print(f"OK button position set to: {args.ok_pos}")
    
    # Create and set up the bot
    bot = ClashBot()
    
    if not bot.setup():
        print("\n❌ Setup failed. Please check that scrcpy is running.")
        sys.exit(1)
    
    # Run the appropriate mode
    if args.test:
        bot.test_single_deploy()
        
    elif args.calibrate:
        bot.calibration_mode()
        
    elif args.loop:
        # Full game loop mode
        bot.run_game_loop(
            num_games=args.count,
            battle_duration=args.duration,
            deploy_delay=args.delay,
            humanize=not args.no_humanize
        )
        
    else:
        # Legacy continuous deployment mode (no game loop)
        bot.run_continuous(
            num_deploys=args.count,
            delay=args.delay,
            randomize=args.random
        )


if __name__ == "__main__":
    main()