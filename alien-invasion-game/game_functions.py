"""
Game functions for Alien Invasion.

This module contains all the core game logic functions including:
- Event handling (keyboard input)
- Bullet management and collision detection
- Alien fleet management and movement
- Collision detection and game state updates
- Game reset functionality

Author: Arthur (CSC-121 Final Project)
Date: May 2026
"""

import pygame
from bullet import Bullet
from alien import Alien
from particle import Particle


# ============================================================================
# INPUT HANDLING
# ============================================================================

def check_keydown_events(event, ai_game):
    """
    Respond to key presses.
    
    Maps keyboard input to game actions:
    - RIGHT ARROW: Move ship right
    - LEFT ARROW: Move ship left
    - SPACE: Fire bullet
    - Q: Quit game
    """
    if event.key == pygame.K_RIGHT:
        ai_game.ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ai_game.ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_game)
    elif event.key == pygame.K_q:
        exit()


def check_keyup_events(event, ai_game):
    """
    Respond to key releases.
    
    Stops ship movement when arrow keys are released.
    """
    if event.key == pygame.K_RIGHT:
        ai_game.ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ai_game.ship.moving_left = False


def fire_bullet(ai_game):
    """
    Fire a bullet if the limit hasn't been reached yet.
    
    The game limits bullets on screen to 3 at a time to balance difficulty.
    Creates a new Bullet sprite and adds it to the bullets group.
    """
    if len(ai_game.bullets) < ai_game.settings.bullets_allowed:
        new_bullet = Bullet(ai_game)
        ai_game.bullets.add(new_bullet)


# ============================================================================
# BULLET MANAGEMENT
# ============================================================================

def update_bullets(ai_game):
    """
    Update position of bullets and remove off-screen bullets.
    
    This function:
    1. Updates all bullet positions (moving them upward)
    2. Removes bullets that have left the top of the screen
    3. Checks for collisions between bullets and aliens
    """
    # Update all bullet positions
    ai_game.bullets.update()

    # Remove bullets that have gone off the screen
    for bullet in ai_game.bullets.copy():
        if bullet.rect.bottom <= 0:  # Top of screen is y=0
            ai_game.bullets.remove(bullet)

    # Check for any collisions between bullets and aliens
    check_bullet_alien_collisions(ai_game)


def check_bullet_alien_collisions(ai_game):
    """
    Respond to bullet-alien collisions.
    
    This function:
    1. Detects which bullets and aliens have collided
    2. Reduces alien health (supports 3-hit tanks)
    3. Creates particle explosions when aliens die
    4. Updates score based on alien type
    5. Checks if the fleet is completely destroyed
    
    Collision handling is more complex now due to multi-hit enemies (tanks).
    """
    # Check for collisions without auto-removing (need to handle health)
    collisions = pygame.sprite.groupcollide(
        ai_game.bullets, ai_game.aliens, False, False
    )

    if collisions:
        # Process each collision
        for bullet, aliens in collisions.items():
            # Remove the bullet (can only hit once)
            if bullet in ai_game.bullets:
                ai_game.bullets.remove(bullet)
            
            # Process each alien hit by this bullet
            for alien in aliens:
                # take_damage() returns True if alien is destroyed
                if alien.take_damage():
                    # Create 8 particles for explosion effect
                    for _ in range(8):
                        particle = Particle(
                            alien.rect.centerx, 
                            alien.rect.centery, 
                            alien.color
                        )
                        ai_game.particles.add(particle)
                    
                    # Award points based on alien type
                    ai_game.stats.score += alien.points
                    ai_game.aliens.remove(alien)
        
        # Check if fleet is completely destroyed
        check_fleet_empty(ai_game)


# ============================================================================
# FLEET MANAGEMENT
# ============================================================================

def check_fleet_empty(ai_game):
    """
    Check if the fleet is empty and create a new one if so.
    
    When the player destroys all aliens:
    1. Clears remaining bullets
    2. Increases game difficulty
    3. Creates a new alien fleet
    4. Increments level counter
    5. Prints difficulty progression to console
    """
    if not ai_game.aliens:
        # Remove all remaining bullets
        ai_game.bullets.empty()
        
        # Increase game difficulty (speeds up aliens, bullets, fleet drop)
        ai_game.settings.increase_difficulty()
        
        # Create new fleet of aliens
        create_fleet(ai_game)
        
        # Increment level
        ai_game.stats.level += 1
        
        # Display difficulty progression to console
        print(f"\n*** LEVEL {ai_game.stats.level} ***")
        print(f"Alien Speed: {ai_game.settings.alien_speed:.2f}")
        print(f"Bullet Speed: {ai_game.settings.bullet_speed:.2f}")
        print(f"Fleet Drop Speed: {ai_game.settings.fleet_drop_speed:.2f}\n")


def create_fleet(ai_game):
    """
    Create a fleet of aliens arranged in rows and columns.
    
    This function:
    1. Creates a temporary alien to determine sizing
    2. Calculates how many aliens fit horizontally
    3. Calculates how many rows fit vertically
    4. Creates aliens in a grid pattern
    5. Limits to max 6 per row and 3 rows for balanced gameplay
    
    The fleet features random alien types:
    - 60% normal aliens
    - 20% scout aliens (fast, less points)
    - 20% tank aliens (slow, more points, 3 hits)
    """
    # Create a temporary alien to get its dimensions
    alien = Alien(ai_game)
    alien_width, alien_height = alien.rect.size
    
    # Calculate how many aliens fit horizontally
    available_space_x = ai_game.settings.screen_width - (2 * alien_width)
    number_aliens_x = available_space_x // (2 * alien_width)
    
    # Limit to maximum 6 aliens per row for balanced gameplay
    number_aliens_x = min(number_aliens_x, 6)

    # Calculate how many rows fit vertically
    ship_height = ai_game.ship.rect.height
    available_space_y = (
        ai_game.settings.screen_height 
        - (3 * alien_height)
        - ship_height
    )
    number_rows = available_space_y // (2 * alien_height)
    
    # Limit to maximum 3 rows for balanced gameplay
    number_rows = min(number_rows, 3)

    # Create the fleet in a grid pattern
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_game, alien_number, row_number)


def create_alien(ai_game, alien_number, row_number):
    """
    Create a single alien and place it in the fleet.
    
    Calculates the position for a single alien based on its row and column
    in the grid, then adds it to the aliens group.
    
    Args:
        ai_game: The main game object
        alien_number: Column position in the fleet
        row_number: Row position in the fleet
    """
    # Create new alien with random type
    alien = Alien(ai_game)
    alien_width, alien_height = alien.rect.size
    
    # Calculate x position (horizontal spacing)
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    
    # Calculate y position (vertical spacing)
    alien.rect.y = alien_height + 2 * alien_height * row_number
    
    # Add alien to fleet
    ai_game.aliens.add(alien)


# ============================================================================
# ALIEN MOVEMENT & COLLISION
# ============================================================================

def update_aliens(ai_game):
    """
    Update the positions of all aliens in the fleet.
    
    This function:
    1. Checks if any aliens hit screen edges (triggers direction change)
    2. Updates all alien positions
    3. Checks for alien-ship collisions
    4. Checks if any aliens reached the bottom (player loses life)
    """
    # Check if fleet needs to change direction
    check_fleet_edges(ai_game)
    
    # Move all aliens
    ai_game.aliens.update()

    # Check if any aliens collided with the ship
    if pygame.sprite.spritecollideany(ai_game.ship, ai_game.aliens):
        ship_hit(ai_game)

    # Check if any aliens reached the bottom of the screen
    check_aliens_bottom(ai_game)


def check_fleet_edges(ai_game):
    """
    Check if any aliens have reached screen edges.
    
    If any alien touches the left or right edge, the entire fleet
    changes direction and drops down.
    """
    for alien in ai_game.aliens.sprites():
        if alien.check_edges():
            # Found an alien at the edge - change fleet direction
            change_fleet_direction(ai_game)
            break  # Only need to change once


def change_fleet_direction(ai_game):
    """
    Drop the entire fleet down and reverse their direction.
    
    Called when any alien reaches screen edge. Makes all aliens:
    1. Drop down by fleet_drop_speed pixels
    2. Reverse horizontal direction (right becomes left, etc.)
    """
    for alien in ai_game.aliens.sprites():
        # Drop all aliens down
        alien.rect.y += ai_game.settings.fleet_drop_speed
    
    # Reverse fleet direction (1 becomes -1, -1 becomes 1)
    ai_game.settings.fleet_direction *= -1


# ============================================================================
# COLLISION & GAME OVER
# ============================================================================

def ship_hit(ai_game):
    """
    Respond to the ship being hit by an alien.
    
    This happens when:
    1. An alien touches the player's ship
    2. An alien reaches the bottom of the screen
    
    If lives remain:
    - Lose one life
    - Create screen shake effect
    - Clear bullets and aliens
    - Create new fleet
    - Center the ship
    - Pause briefly for player feedback
    
    If no lives remain:
    - End the game
    - Show game over screen
    """
    if ai_game.stats.ships_left > 0:
        # Still have lives left
        ai_game.stats.ships_left -= 1
        
        # Create screen shake for impact feedback
        ai_game.screen_shake_intensity = 10
        ai_game.screen_shake_duration = 10

        # Clear the screen
        ai_game.aliens.empty()
        ai_game.bullets.empty()

        # Recreate fleet and reset ship position
        create_fleet(ai_game)
        ai_game.ship.center_ship()

        # Pause to let player see they were hit
        pygame.time.wait(500)
    else:
        # No lives left - game over
        ai_game.stats.game_active = False
        ai_game.show_game_over = True


def check_aliens_bottom(ai_game):
    """
    Check if any aliens have reached the bottom of the screen.
    
    If any alien reaches the bottom, it counts as hitting the player
    (same as touching the ship) and the player loses a life.
    """
    screen_rect = ai_game.screen.get_rect()
    for alien in ai_game.aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Alien reached bottom - treat as ship hit
            ship_hit(ai_game)
            break  # Only process one hit per frame


# ============================================================================
# GAME STATE
# ============================================================================

def reset_game(ai_game):
    """
    Reset the game for a new game session.
    
    Clears all game state and recreates the initial conditions:
    1. Resets game settings to default (removes difficulty multipliers)
    2. Resets statistics (score, level, lives)
    3. Clears all sprites (aliens, bullets, particles)
    4. Clears visual effects (screen shake)
    5. Creates new alien fleet
    6. Centers the ship
    7. Sets game to active state
    """
    # Reset settings to default (removes difficulty scaling)
    ai_game.settings = type(ai_game.settings)()
    
    # Reset statistics (score=0, level=1, ships=3)
    ai_game.stats.reset_stats()
    
    # Clear all sprite groups
    ai_game.aliens.empty()
    ai_game.bullets.empty()
    ai_game.particles.empty()
    
    # Clear visual effects
    ai_game.screen_shake_intensity = 0
    ai_game.screen_shake_duration = 0
    
    # Create fresh fleet of aliens
    create_fleet(ai_game)
    
    # Reset ship to center
    ai_game.ship.center_ship()
    
    # Set game to active (start playing)
    ai_game.stats.game_active = True
