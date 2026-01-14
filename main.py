"""
Clash Royale Test Automation - Main Entry Point

Usage:
    python main.py              # Run continuous deployment
    python main.py --test       # Single deploy test
    python main.py --calibrate  # Position calibration mode
    python main.py --count 10   # Deploy exactly 10 cards
"""

import argparse
import sys

from src.bot import ClashBot


def main():
    parser = argparse.ArgumentParser(
        description="Clash Royale Test Arena Automation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python main.py              # Run continuous deployment
    python main.py --test       # Test single card deploy  
    python main.py --calibrate  # Find positions for config
    python main.py --count 20   # Deploy 20 cards then stop
    python main.py --delay 2    # 2 second delay between deploys
    python main.py --random     # Randomize card/target selection
        """
    )
    
    parser.add_argument("--test", "-t", action="store_true",
                       help="Run a single test deploy")
    parser.add_argument("--calibrate", "-c", action="store_true",
                       help="Enter calibration mode to find positions")
    parser.add_argument("--count", "-n", type=int, default=None,
                       help="Number of cards to deploy (default: infinite)")
    parser.add_argument("--delay", "-d", type=float, default=None,
                       help="Delay between deploys in seconds")
    parser.add_argument("--random", "-r", action="store_true",
                       help="Randomize card and target selection")
    
    args = parser.parse_args()
    
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
        
    else:
        # Continuous deployment mode
        bot.run_continuous(
            num_deploys=args.count,
            delay=args.delay,
            randomize=args.random
        )


if __name__ == "__main__":
    main()
