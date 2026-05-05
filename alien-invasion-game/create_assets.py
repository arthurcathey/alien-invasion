"""Generate image assets for Alien Invasion game."""

import pygame
import os
import math

# Change to the correct directory
os.chdir(r'c:\Users\arthu\OneDrive\Desktop\CSC-121')

pygame.init()

# Create detailed ship image (spaceship with fins)
ship_surface = pygame.Surface((50, 60), pygame.SRCALPHA)

# Main body (triangle pointing up)
pygame.draw.polygon(ship_surface, (0, 220, 0), [(25, 5), (5, 55), (45, 55)])

# Left fin
pygame.draw.polygon(ship_surface, (0, 180, 0), [(5, 55), (0, 60), (10, 50)])

# Right fin
pygame.draw.polygon(ship_surface, (0, 180, 0), [(45, 55), (50, 60), (40, 50)])

# Cockpit window
pygame.draw.circle(ship_surface, (100, 255, 255), (25, 20), 4)

# Engine glow
pygame.draw.circle(ship_surface, (255, 150, 0), (18, 52), 3)
pygame.draw.circle(ship_surface, (255, 150, 0), (32, 52), 3)

pygame.image.save(ship_surface, 'ship.bmp')
print("Created detailed ship.bmp")

# Create detailed alien image (insectoid creature)
alien_surface = pygame.Surface((45, 35), pygame.SRCALPHA)

# Body (main green oval)
pygame.draw.ellipse(alien_surface, (150, 220, 100), (8, 10, 29, 18))

# Head (darker green circle)
pygame.draw.circle(alien_surface, (100, 180, 80), (22, 8), 7)

# Large left eye (white with black pupil)
pygame.draw.circle(alien_surface, (255, 255, 255), (16, 6), 4)
pygame.draw.circle(alien_surface, (0, 0, 0), (16, 6), 2)

# Large right eye (white with black pupil)
pygame.draw.circle(alien_surface, (255, 255, 255), (28, 6), 4)
pygame.draw.circle(alien_surface, (0, 0, 0), (28, 6), 2)

# Mouth/mandibles
pygame.draw.line(alien_surface, (0, 0, 0), (18, 14), (15, 18), 2)
pygame.draw.line(alien_surface, (0, 0, 0), (26, 14), (29, 18), 2)

# Left arm
pygame.draw.line(alien_surface, (150, 220, 100), (10, 16), (2, 16), 3)

# Right arm
pygame.draw.line(alien_surface, (150, 220, 100), (34, 16), (42, 16), 3)

# Left legs
pygame.draw.line(alien_surface, (150, 220, 100), (12, 28), (8, 34), 2)
pygame.draw.line(alien_surface, (150, 220, 100), (18, 28), (16, 34), 2)

# Right legs
pygame.draw.line(alien_surface, (150, 220, 100), (26, 28), (28, 34), 2)
pygame.draw.line(alien_surface, (150, 220, 100), (32, 28), (36, 34), 2)

pygame.image.save(alien_surface, 'alien.bmp')
print("Created detailed alien.bmp")

print("\nDetailed image assets created successfully!")

