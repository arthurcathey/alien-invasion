"""
Game statistics tracking for Alien Invasion.

This module contains the GameStats class which tracks all persistent game
statistics like score, level, lives, and active/inactive state.

Author: Arthur (CSC-121 Final Project)
Date: May 2026
"""


class GameStats:
    """
    Track statistics for Alien Invasion.
    
    Maintains game state and statistics that persist across multiple game
    sessions or can be reset for new games.
    """

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

        # Start Alien Invasion in an active state
        self.game_active = False

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
