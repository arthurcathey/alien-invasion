"""
Alien Invasion: A 2D space shooter game.

This module contains the main AlienInvasion class that manages the entire game.
It handles initialization, the main game loop, event processing, screen updates,
and game state management.

Author: Arthur (CSC-121 Final Project)
Date: May 2026
"""

import pygame
import sys
import random
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from button import Button
from ship import Ship
from high_scores import HighScores
import game_functions as gf


class AlienInvasion:
    """
    Overall class to manage game assets and behavior.
    
    This class serves as the main controller for the entire game. It initializes
    all game components (ship, aliens, bullets), manages the game loop, processes
    user input, and handles rendering.
    
    Attributes:
        screen (pygame.Surface): The main game window
        settings (Settings): Game configuration and difficulty settings
        stats (GameStats): Current game statistics (score, level, lives)
        high_scores (HighScores): High score management system
        ship (Ship): Player's controllable spaceship
        bullets (pygame.sprite.Group): Group of active bullets
        aliens (pygame.sprite.Group): Group of active aliens
        particles (pygame.sprite.Group): Group of particle effects
    """

    def __init__(self):
        """Initialize the game and create game resources."""
        # Initialize pygame
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        # Create the game window with title
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Create game statistics tracker and high score system
        self.stats = GameStats(self)
        self.high_scores = HighScores()
        
        # Create UI elements (play button)
        self.sb = Button(self, "Play Game")

        # Create sprite groups for game objects
        self.ship = Ship(self)
        self.bullets = Group()
        self.aliens = Group()
        self.particles = Group()

        # Screen shake variables for impact feedback
        self.screen_shake_intensity = 0
        self.screen_shake_duration = 0
        self.show_game_over = False

        # Create the initial fleet of aliens
        gf.create_fleet(self)

    def run_game(self):
        """
        Start the main game loop.
        
        This is the core of the game. It runs continuously at 60 FPS and:
        1. Checks for user input
        2. Updates game state (if playing)
        3. Renders everything to screen
        4. Maintains consistent frame rate
        """
        while True:
            # Handle all user input
            self._check_events()

            # Update game state if game is active
            if self.stats.game_active:
                self.ship.update()
                gf.update_bullets(self)
                gf.update_aliens(self)
            
            # Update particle effects
            self.particles.update()
            for particle in self.particles.sprites():
                if not particle.is_alive():
                    self.particles.remove(particle)
            
            # Update screen shake effect
            if self.screen_shake_duration > 0:
                self.screen_shake_duration -= 1

            # Render game to screen
            self._update_screen()
            
            # Maintain 60 frames per second
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # User closed the window - exit game
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Detect mouse clicks on buttons
                mouse_x, mouse_y = event.pos
                self._check_play_button(mouse_x, mouse_y)

    def _check_keydown_events(self, event):
        """
        Respond to key presses.
        
        Handles:
        - Arrow keys for ship movement
        - Space bar for firing bullets
        - Q key to quit
        """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            gf.fire_bullet(self)
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases to stop ship movement."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_x, mouse_y):
        """
        Start a new game when the player clicks the Play button.
        
        Also saves the score if the game was over and this is a retry.
        """
        button_clicked = self.sb.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked and not self.stats.game_active:
            # Save score to high score list if game was over
            if self.show_game_over:
                self.high_scores.add_score(self.stats.score)
                self.show_game_over = False
            # Reset game state and start new game
            gf.reset_game(self)

    def _update_screen(self):
        """
        Update images on screen and flip to the new screen.
        
        This handles rendering all game objects, applying screen shake effects,
        and displaying UI elements.
        """
        self.screen.fill(self.settings.bg_color)
        
        # Calculate screen shake offset for impact effects
        shake_x = 0
        shake_y = 0
        if self.screen_shake_duration > 0:
            shake_x = random.randint(-self.screen_shake_intensity, self.screen_shake_intensity)
            shake_y = random.randint(-self.screen_shake_intensity, self.screen_shake_intensity)
        
        # Create temporary surface for applying shake effect
        temp_surface = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
        temp_surface.fill(self.settings.bg_color)
        
        # Draw all game objects to temporary surface
        self.ship.screen = temp_surface
        self.ship.blitme()
        self.ship.screen = self.screen

        for bullet in self.bullets.sprites():
            bullet.screen = temp_surface
            bullet.draw_bullet()
            bullet.screen = self.screen

        for alien in self.aliens.sprites():
            alien.screen = temp_surface
            alien.blitme()
            alien.screen = self.screen
        
        # Draw particle effects
        for particle in self.particles.sprites():
            temp_surface.blit(particle.image, particle.rect)

        # Apply shake effect by blitting with offset
        self.screen.blit(temp_surface, (shake_x, shake_y))

        # Draw HUD (heads-up display) with score, level, lives
        self._draw_stats()

        # Draw UI elements
        if not self.stats.game_active:
            if self.show_game_over:
                self._draw_game_over()
            else:
                self.sb.draw_button()

        # Update the display with all rendered elements
        pygame.display.flip()

    def _draw_game_over(self):
        """
        Draw game over screen with statistics and high scores.
        
        Displays:
        - "GAME OVER" text in red
        - Final score
        - Level reached
        - Current high score
        - "NEW HIGH SCORE" notification if applicable
        - Play button to restart
        """
        # Semi-transparent dark overlay
        overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
        overlay.set_alpha(200)
        overlay.fill((50, 50, 50))
        self.screen.blit(overlay, (0, 0))
        
        # "GAME OVER" text in large red font
        font_large = pygame.font.SysFont(None, 72)
        game_over_text = font_large.render("GAME OVER", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect()
        game_over_rect.center = (self.settings.screen_width // 2, 100)
        self.screen.blit(game_over_text, game_over_rect)
        
        # Display final stats
        font_med = pygame.font.SysFont(None, 48)
        score_text = font_med.render(f"Final Score: {self.stats.score}", True, (255, 255, 255))
        level_text = font_med.render(f"Level Reached: {self.stats.level}", True, (255, 255, 255))
        
        score_rect = score_text.get_rect()
        score_rect.center = (self.settings.screen_width // 2, 250)
        self.screen.blit(score_text, score_rect)
        
        level_rect = level_text.get_rect()
        level_rect.center = (self.settings.screen_width // 2, 320)
        self.screen.blit(level_text, level_rect)
        
        # Display high score
        high_score = self.high_scores.get_high_score()
        high_score_text = font_med.render(f"High Score: {high_score}", True, (255, 215, 0))
        high_score_rect = high_score_text.get_rect()
        high_score_rect.center = (self.settings.screen_width // 2, 390)
        self.screen.blit(high_score_text, high_score_rect)
        
        # Highlight if this is a new personal best
        if self.high_scores.is_high_score(self.stats.score):
            new_high_text = font_med.render("*** NEW HIGH SCORE ***", True, (0, 255, 0))
            new_high_rect = new_high_text.get_rect()
            new_high_rect.center = (self.settings.screen_width // 2, 460)
            self.screen.blit(new_high_text, new_high_rect)
        
        # Show Play button to restart
        self.sb.draw_button()

    def _draw_stats(self):
        """Draw score, level, and ships left on screen during gameplay."""
        font = pygame.font.SysFont(None, 36)
        
        # Display current score
        score_text = font.render(f"Score: {self.stats.score}", True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))
        
        # Display current level
        level_text = font.render(f"Level: {self.stats.level}", True, (0, 0, 0))
        self.screen.blit(level_text, (10, 50))
        
        # Display remaining ships/lives
        ships_text = font.render(f"Ships: {self.stats.ships_left}", True, (0, 0, 0))
        self.screen.blit(ships_text, (10, 90))


# Main execution
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()

    def run_game(self):
        """Start the main game loop."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                gf.update_bullets(self)
                gf.update_aliens(self)
            
            # Update particles
            self.particles.update()
            for particle in self.particles.sprites():
                if not particle.is_alive():
                    self.particles.remove(particle)
            
            # Update screen shake
            if self.screen_shake_duration > 0:
                self.screen_shake_duration -= 1

            self._update_screen()
            self.clock.tick(60)  # 60 FPS

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                self._check_play_button(mouse_x, mouse_y)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            gf.fire_bullet(self)
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_x, mouse_y):
        """Start a new game when the player clicks Play."""
        button_clicked = self.sb.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked and not self.stats.game_active:
            # Save score if game was over
            if self.show_game_over:
                self.high_scores.add_score(self.stats.score)
                self.show_game_over = False
            gf.reset_game(self)

    def _update_screen(self):
        """Update images on screen and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        
        # Apply screen shake offset
        shake_x = 0
        shake_y = 0
        if self.screen_shake_duration > 0:
            import random
            shake_x = random.randint(-self.screen_shake_intensity, self.screen_shake_intensity)
            shake_y = random.randint(-self.screen_shake_intensity, self.screen_shake_intensity)
        
        # Create a temporary surface for shake offset
        temp_surface = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
        temp_surface.fill(self.settings.bg_color)
        
        # Draw game objects to temp surface
        self.ship.screen = temp_surface
        self.ship.blitme()
        self.ship.screen = self.screen

        for bullet in self.bullets.sprites():
            bullet.screen = temp_surface
            bullet.draw_bullet()
            bullet.screen = self.screen

        for alien in self.aliens.sprites():
            alien.screen = temp_surface
            alien.blitme()
            alien.screen = self.screen
        
        # Draw particles
        for particle in self.particles.sprites():
            temp_surface.blit(particle.image, particle.rect)

        # Blit temp surface to main screen with shake offset
        self.screen.blit(temp_surface, (shake_x, shake_y))

        # Draw the score and level info
        self._draw_stats()

        # Draw the play button if the game is inactive
        if not self.stats.game_active:
            if self.show_game_over:
                self._draw_game_over()
            else:
                self.sb.draw_button()

        pygame.display.flip()

    def _draw_game_over(self):
        """Draw game over screen with stats."""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
        overlay.set_alpha(200)
        overlay.fill((50, 50, 50))
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        font_large = pygame.font.SysFont(None, 72)
        game_over_text = font_large.render("GAME OVER", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect()
        game_over_rect.center = (self.settings.screen_width // 2, 100)
        self.screen.blit(game_over_text, game_over_rect)
        
        # Stats
        font_med = pygame.font.SysFont(None, 48)
        score_text = font_med.render(f"Final Score: {self.stats.score}", True, (255, 255, 255))
        level_text = font_med.render(f"Level Reached: {self.stats.level}", True, (255, 255, 255))
        
        score_rect = score_text.get_rect()
        score_rect.center = (self.settings.screen_width // 2, 250)
        self.screen.blit(score_text, score_rect)
        
        level_rect = level_text.get_rect()
        level_rect.center = (self.settings.screen_width // 2, 320)
        self.screen.blit(level_text, level_rect)
        
        # High score
        high_score = self.high_scores.get_high_score()
        high_score_text = font_med.render(f"High Score: {high_score}", True, (255, 215, 0))
        high_score_rect = high_score_text.get_rect()
        high_score_rect.center = (self.settings.screen_width // 2, 390)
        self.screen.blit(high_score_text, high_score_rect)
        
        # Check if new high score
        if self.high_scores.is_high_score(self.stats.score):
            new_high_text = font_med.render("*** NEW HIGH SCORE ***", True, (0, 255, 0))
            new_high_rect = new_high_text.get_rect()
            new_high_rect.center = (self.settings.screen_width // 2, 460)
            self.screen.blit(new_high_text, new_high_rect)
        
        # Play again button
        self.sb.draw_button()

    def _draw_stats(self):
        """Draw score, level, and ships left on screen."""
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {self.stats.score}", True, (0, 0, 0))
        level_text = font.render(f"Level: {self.stats.level}", True, (0, 0, 0))
        ships_text = font.render(f"Ships: {self.stats.ships_left}", True, (0, 0, 0))

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 50))
        self.screen.blit(ships_text, (10, 90))


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
