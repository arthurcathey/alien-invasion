"""
Game settings and constants for Alien Invasion.

This module contains the Settings class which stores all configurable game
parameters like screen dimensions, speeds, colors, and difficulty scaling.

Author: Arthur (CSC-121 Final Project)
Date: May 2026
"""


class Settings:
    """
    Store all settings for Alien Invasion.
    
    This class centralizes all game configuration so adjustments can be made
    easily without modifying game logic. It also handles difficulty progression.
    """

    def __init__(self):
        """Initialize the game settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)  # Light gray background

        # Ship settings
        self.ship_speed = 5  # Pixels per frame
        self.ship_limit = 3  # Number of ships (lives) before game over

        # Bullet settings
        self.bullet_speed = 7  # Pixels per frame (upward)
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)  # Dark gray
        self.bullets_allowed = 3  # Maximum bullets on screen at once

        # Alien settings
        self.alien_speed = 1  # Pixels per frame (horizontal)
        self.fleet_drop_speed = 10  # Pixels dropped when hitting screen edge
        self.fleet_direction = 1  # 1 for right, -1 for left

        # Difficulty settings - used to scale game speed each level
        self.speedup_scale = 1.1  # 10% increase per level
        self.score_scale = 1.5  # Score multiplier (unused in current version)

    def increase_difficulty(self):
        """
        Increase game difficulty with each new fleet.
        
        This is called whenever the player clears all aliens and moves to the
        next level. It increases the speed of aliens, bullets, and fleet drops
        to make the game progressively harder.
        """
        self.alien_speed *= self.speedup_scale
        self.fleet_drop_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
