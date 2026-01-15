"""
Human-Like Behavior Module

Adds randomness and variation to make automation look more natural.
Humans are imprecise, inconsistent, and sometimes pause to think.
"""

import random
import time
from typing import Tuple


class HumanBehavior:
    """
    Adds human-like randomness to bot actions.
    
    Humans:
    - Don't click exact same spot every time
    - Have variable reaction times
    - Sometimes pause to think
    - Drag at different speeds
    - Make small mistakes
    - Sometimes hesitate before acting
    """
    
    def __init__(self, 
                 position_variance: float = 0.02,
                 timing_variance: float = 0.5,
                 think_chance: float = 0.1,
                 think_duration: Tuple[float, float] = (1.0, 3.0),
                 long_pause_chance: float = 0.05,
                 long_pause_duration: Tuple[float, float] = (4.0, 8.0)):
        """
        Initialize human behavior settings.
        
        Args:
            position_variance: Max random offset for positions (as percentage, 0.02 = 2%)
            timing_variance: How much to vary timing (multiplier, 0.5 = ±50%)
            think_chance: Probability of a "thinking" pause (0.1 = 10%)
            think_duration: (min, max) seconds for thinking pauses
            long_pause_chance: Probability of a longer pause (distracted, checking phone, etc.)
            long_pause_duration: (min, max) seconds for long pauses
        """
        self.position_variance = position_variance
        self.timing_variance = timing_variance
        self.think_chance = think_chance
        self.think_duration = think_duration
        self.long_pause_chance = long_pause_chance
        self.long_pause_duration = long_pause_duration
        
    def add_position_noise(self, x: float, y: float) -> Tuple[float, float]:
        """
        Add small random offset to a position.
        
        Args:
            x: X position (percentage 0-1)
            y: Y position (percentage 0-1)
            
        Returns:
            (x, y) with random offset applied
        """
        x_offset = random.uniform(-self.position_variance, self.position_variance)
        y_offset = random.uniform(-self.position_variance, self.position_variance)
        
        # Keep within bounds
        new_x = max(0.05, min(0.95, x + x_offset))
        new_y = max(0.05, min(0.95, y + y_offset))
        
        return (new_x, new_y)
    
    def add_button_jitter(self, x: float, y: float) -> Tuple[float, float]:
        """
        Add jitter specifically for button clicks (smaller variance).
        
        Args:
            x: X position (percentage 0-1)
            y: Y position (percentage 0-1)
            
        Returns:
            (x, y) with small random offset
        """
        # Smaller variance for buttons (we need to actually hit them)
        x_offset = random.uniform(-0.01, 0.01)
        y_offset = random.uniform(-0.01, 0.01)
        
        return (x + x_offset, y + y_offset)
    
    def vary_delay(self, base_delay: float) -> float:
        """
        Add randomness to a delay time.
        
        Args:
            base_delay: The base delay in seconds
            
        Returns:
            Varied delay time
        """
        variance = base_delay * self.timing_variance
        return base_delay + random.uniform(-variance, variance)
    
    def get_drag_duration(self, base_duration: float = 0.3) -> float:
        """
        Get a randomized drag duration.
        
        Args:
            base_duration: Base drag time in seconds
            
        Returns:
            Randomized duration (humans drag at different speeds)
        """
        # Sometimes fast, sometimes slow
        speed_multiplier = random.uniform(0.7, 1.5)
        return base_duration * speed_multiplier
    
    def should_think(self) -> bool:
        """
        Randomly decide if we should pause to "think".
        
        Returns:
            True if we should pause
        """
        return random.random() < self.think_chance
    
    def should_long_pause(self) -> bool:
        """
        Randomly decide if we should take a longer pause.
        (Like checking phone, getting distracted, etc.)
        
        Returns:
            True if we should take a long pause
        """
        return random.random() < self.long_pause_chance
    
    def think(self):
        """
        Pause for a random "thinking" duration.
        Call this occasionally to simulate human decision-making.
        """
        duration = random.uniform(self.think_duration[0], self.think_duration[1])
        print(f"   💭 (thinking for {duration:.1f}s...)")
        time.sleep(duration)
    
    def long_pause(self):
        """
        Take a longer pause (distraction, etc.)
        """
        duration = random.uniform(self.long_pause_duration[0], self.long_pause_duration[1])
        print(f"   📱 (distracted for {duration:.1f}s...)")
        time.sleep(duration)
    
    def maybe_think(self):
        """
        Maybe pause to think (based on think_chance probability).
        """
        if self.should_long_pause():
            self.long_pause()
        elif self.should_think():
            self.think()
    
    def pre_drag_hesitation(self):
        """
        Brief hesitation before starting a drag.
        Humans don't instantly start dragging - they position, then drag.
        """
        if random.random() < 0.3:  # 30% chance
            hesitation = random.uniform(0.1, 0.4)
            time.sleep(hesitation)
    
    def get_card_offset(self) -> Tuple[float, float]:
        """
        Get a random offset for grabbing a card.
        Humans don't always grab the exact center.
        
        Returns:
            (x_offset, y_offset) in percentage
        """
        x_off = random.uniform(-0.015, 0.015)
        y_off = random.uniform(-0.01, 0.01)
        return (x_off, y_off)
    
    def random_deploy_delay(self, 
                            min_delay: float = 2.0, 
                            max_delay: float = 5.0) -> float:
        """
        Get a random delay between card deploys.
        
        Uses a slight bias toward shorter delays (humans are generally
        eager to play cards when they have elixir).
        
        Args:
            min_delay: Minimum delay
            max_delay: Maximum delay
            
        Returns:
            Random delay in seconds
        """
        # Use beta distribution for more natural feel
        # This biases slightly toward lower values
        alpha, beta = 2, 3
        normalized = random.betavariate(alpha, beta)
        return min_delay + normalized * (max_delay - min_delay)
    
    def random_wait_between_games(self, base_wait: float = 3.0) -> float:
        """
        Random wait time between games.
        
        Args:
            base_wait: Base wait time
            
        Returns:
            Randomized wait time
        """
        return base_wait + random.uniform(-1.0, 3.0)


# Create a default instance for easy access
default_human = HumanBehavior()


def humanize_position(x: float, y: float) -> Tuple[float, float]:
    """Convenience function to add position noise."""
    return default_human.add_position_noise(x, y)


def humanize_button(x: float, y: float) -> Tuple[float, float]:
    """Convenience function to add button click jitter."""
    return default_human.add_button_jitter(x, y)


def humanize_delay(delay: float) -> float:
    """Convenience function to vary a delay."""
    return default_human.vary_delay(delay)


def random_delay(min_d: float = 2.0, max_d: float = 5.0) -> float:
    """Convenience function for random deploy delay."""
    return default_human.random_deploy_delay(min_d, max_d)