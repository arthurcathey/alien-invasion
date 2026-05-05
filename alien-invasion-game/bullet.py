"""
Bullet class for Alien Invasion game.

This module contains the Bullet class representing projectiles fired by the player.
Bullets move upward and are removed when they leave the screen.

Author: Arthur (CSC-121 Final Project)
Date: May 2026
"""

import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """
    Manage bullets fired from the ship.
    
    Bullets are projectiles that move upward from the ship's position.
    They are automatically removed when they move off the top of the screen.
    The game limits bullets on screen to 3 at a time to balance difficulty.
    """

    def __init__(self, ai_game):
        """Create a bullet object at the ship's current position (top center)."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Create a bullet rect at (0, 0) and then set correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store the bullet's position as a decimal value
        self.y = float(self.rect.y)

    def update(self):
        """
        Move the bullet up the screen.
        
        Bullets use decimal positioning for smooth animation at high speeds.
        """
        # Update the decimal position of the bullet
        self.y -= self.settings.bullet_speed
        # Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen as a small dark rectangle."""
        pygame.draw.rect(self.screen, self.settings.bullet_color, self.rect)
