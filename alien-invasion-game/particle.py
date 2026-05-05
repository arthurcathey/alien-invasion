"""
Particle effects for Alien Invasion.

This module contains the Particle class for creating visual explosion effects
when aliens are destroyed. Particles fade out and fall with simulated gravity.

Author: Arthur (CSC-121 Final Project)
Date: May 2026
"""

import pygame
import random
from pygame.sprite import Sprite


class Particle(Sprite):
    """
    A particle for explosion effects.
    
    Particles are small colored circles that burst outward when an alien dies.
    They simulate gravity and fade out over time for a satisfying visual effect.
    """

    def __init__(self, x, y, color=None):
        """Initialize a particle at the given position with optional color."""
        super().__init__()
        
        # Random color if not specified (yellow/orange/red tones)
        if color is None:
            color = random.choice([
                (255, 200, 0),    # Yellow
                (255, 150, 0),    # Orange
                (255, 100, 0),    # Dark Orange
                (255, 255, 100),  # Light Yellow
            ])
        
        # Create particle as small circle
        self.size = random.randint(3, 8)
        self.image = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (self.size, self.size), self.size)
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Velocity - random direction
        angle = random.uniform(0, 2 * 3.14159)
        speed = random.uniform(2, 6)
        self.vx = speed * (angle * 0.5)
        self.vy = speed * (angle * 0.5) - 3  # Bias upward
        
        # Lifetime
        self.lifetime = random.randint(20, 40)
        self.age = 0

    def update(self):
        """Update particle position and fade."""
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.vy += 0.1  # Gravity
        
        self.age += 1
        
        # Fade out
        alpha = int(255 * (1 - self.age / self.lifetime))
        self.image.set_alpha(alpha)

    def is_alive(self):
        """Return True if particle hasn't exceeded its lifetime yet."""
        return self.age < self.lifetime
