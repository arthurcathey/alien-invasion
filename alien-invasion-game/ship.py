"""
Player ship for Alien Invasion game.

This module contains the Ship class which represents the player's controllable
spacecraft. The ship can move left and right and fire bullets.

Author: Arthur (CSC-121 Final Project)
Date: May 2026
"""

import pygame


class Ship:
    """
    Manage the player's ship.
    
    The ship is controlled by the player using arrow keys and can fire bullets
    with the spacebar. It stays within the screen boundaries and updates position
    based on movement flags set by keyboard input.
    """

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load and scale the ship image (green triangle with details)
        self.image = pygame.image.load('ship.bmp')
        self.image = pygame.transform.scale(self.image, (50, 60))
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal x value for smooth fractional pixel movement
        # Using decimals instead of integers allows smooth animation
        self.x = float(self.rect.x)

        # Movement flags - set by keyboard input, used to update position
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """
        Update the ship's position based on movement flags.
        
        Movement uses decimal positioning for smooth animation. The ship cannot
        move beyond the left or right screen edges.
        """
        # Update the ship's x value, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Update rect object from self.x
        self.rect.x = self.x

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen. Called after losing a life."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
