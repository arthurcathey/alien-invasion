"""
Alien class with variety types for Alien Invasion.

This module contains the Alien class representing enemy spacecraft.
Three different alien types exist with different speeds, health, and point values.

Alien Types:
- Scout: Fast, 1 hit to kill, 50 points
- Normal: Standard speed, 1 hit to kill, 100 points
- Tank: Slow, 3 hits to kill, 300 points

Author: Arthur (CSC-121 Final Project)
Date: May 2026
"""

import pygame
from pygame.sprite import Sprite
import random


class Alien(Sprite):
    """
    A class to represent a single alien in the fleet.
    
    Aliens move horizontally and drop down when hitting screen edges.
    Three different types provide variety in gameplay and scoring.
    """

    # Class variable defining three alien types with different properties
    # Each type has: speed multiplier, health (hit points), color, and points
    TYPES = {
        'scout': {'speed_mult': 1.5, 'health': 1, 'color': (100, 200, 100), 'points': 50},
        'normal': {'speed_mult': 1.0, 'health': 1, 'color': (150, 220, 100), 'points': 100},
        'tank': {'speed_mult': 0.6, 'health': 3, 'color': (200, 100, 100), 'points': 300},
    }

    def __init__(self, ai_game, alien_type=None):
        """
        Initialize the alien and set its starting position.
        
        If no type is specified, randomly selects one weighted toward 'normal'.
        """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Choose alien type (weighted towards normal)
        if alien_type is None:
            rand = random.random()
            if rand < 0.6:
                alien_type = 'normal'
            elif rand < 0.8:
                alien_type = 'scout'
            else:
                alien_type = 'tank'
        
        self.type = alien_type
        self.type_data = self.TYPES[alien_type]
        self.health = self.type_data['health']
        self.max_health = self.type_data['health']
        self.points = self.type_data['points']
        self.color = self.type_data['color']

        # Create alien based on type
        self._create_image()
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position
        self.x = float(self.rect.x)

    def _create_image(self):
        """Create alien image based on type."""
        if self.type == 'scout':
            # Small, thin alien
            size = (35, 25)
        elif self.type == 'tank':
            # Large, bulky alien
            size = (55, 45)
        else:  # normal
            # Medium alien
            size = (45, 35)

        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.base_image = self.image.copy()

        # Draw based on type
        if self.type == 'scout':
            self._draw_scout()
        elif self.type == 'tank':
            self._draw_tank()
        else:  # normal
            self._draw_normal()

    def _draw_normal(self):
        """Draw normal alien."""
        size = self.image.get_size()
        mid_x, mid_y = size[0] // 2, size[1] // 2
        
        # Body
        pygame.draw.ellipse(self.image, self.color, (6, 8, 23, 14))
        # Head
        pygame.draw.circle(self.image, self.color, (mid_x, 6), 5)
        # Eyes
        pygame.draw.circle(self.image, (255, 255, 255), (mid_x - 4, 4), 3)
        pygame.draw.circle(self.image, (255, 255, 255), (mid_x + 4, 4), 3)
        pygame.draw.circle(self.image, (0, 0, 0), (mid_x - 4, 4), 1)
        pygame.draw.circle(self.image, (0, 0, 0), (mid_x + 4, 4), 1)

    def _draw_scout(self):
        """Draw fast scout alien."""
        size = self.image.get_size()
        mid_x, mid_y = size[0] // 2, size[1] // 2
        
        # Thin pointed body
        pygame.draw.polygon(self.image, self.color, [(mid_x, 2), (3, 20), (size[0]-3, 20)])
        # Large eyes
        pygame.draw.circle(self.image, (255, 255, 255), (mid_x - 3, 8), 2)
        pygame.draw.circle(self.image, (255, 255, 255), (mid_x + 3, 8), 2)

    def _draw_tank(self):
        """Draw strong tank alien."""
        size = self.image.get_size()
        
        # Large body
        pygame.draw.ellipse(self.image, self.color, (8, 12, 39, 26))
        # Head
        pygame.draw.circle(self.image, self.color, (27, 8), 8)
        # Big threatening eyes
        pygame.draw.circle(self.image, (255, 100, 100), (21, 5), 4)
        pygame.draw.circle(self.image, (255, 100, 100), (33, 5), 4)
        pygame.draw.circle(self.image, (0, 0, 0), (21, 5), 2)
        pygame.draw.circle(self.image, (0, 0, 0), (33, 5), 2)

    def take_damage(self):
        """
        Reduce health when hit by a bullet.
        
        Returns:
            True if alien is destroyed (health <= 0), False otherwise.
        """
        self.health -= 1
        return self.health <= 0

    def update(self):
        """Move the alien right or left."""
        speed_mult = self.type_data['speed_mult']
        self.x += self.settings.alien_speed * self.settings.fleet_direction * speed_mult
        self.rect.x = self.x

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        return False

    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)
