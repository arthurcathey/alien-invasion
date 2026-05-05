# Alien Invasion Game

A complete 2D space shooter game built with Python and Pygame for CSC-121 (Introduction to Computer Science) final project.

## Overview

**Alien Invasion** is a challenging arcade-style game where you control a spaceship at the bottom of the screen and defend against waves of descending aliens. Destroy all aliens to advance to the next level and increase the difficulty!

## Quick Start

### Requirements
- Python 3.7+
- Pygame 2.6.1

### Installation

```bash
# Install dependencies
pip install pygame

# Run the game
python alien_invasion.py
```

## Controls

| Key | Action |
|-----|--------|
| ← / → | Move ship left/right |
| SPACE | Fire bullets |
| Q | Quit game |
| CLICK | Start game / Restart |

## Features

### Core Gameplay
- 60 FPS game loop with smooth animations
- Responsive ship controls with arrow keys
- Collision detection for bullets, aliens, and ship
- Progressive difficulty scaling (10% increase per level)
- Lives system (3 ships to start)

### Enhanced Features (5 Bonus Implementations)
1. **Three Enemy Types** - Scout (fast, 50pts), Normal (balanced, 100pts), Tank (tough, 300pts)
2. **Particle Effects** - Colorful explosions with gravity simulation
3. **Screen Shake** - Visual feedback when hit
4. **High Score System** - Auto-saves top 5 scores to file
5. **Game Over Screen** - Statistics display with high score alert

## File Structure

```
CSC-121/
├── alien_invasion.py           # Main game controller
├── settings.py                 # Game configuration
├── game_stats.py               # Statistics tracking
├── ship.py                     # Player ship class
├── bullet.py                   # Bullet projectile class
├── alien.py                    # Enemy alien class (3 types)
├── game_functions.py           # Core game logic
├── button.py                   # UI button class
├── high_scores.py              # High score persistence
├── particle.py                 # Explosion particle effects
├── create_assets.py            # Asset generator utility
├── ship.bmp                    # Ship sprite image
├── alien.bmp                   # Alien sprite image
├── highscores.txt              # High score file (auto-created)
├── FINAL_PROJECT_DOCUMENTATION.md  # Comprehensive documentation
└── README.md                   # This file
```

## Gameplay Instructions

### Objective
Destroy all aliens to advance to the next level. Survive as long as possible without losing all 3 ships.

### Scoring
| Enemy Type | Health | Points |
|-----------|--------|--------|
| Scout | 1 hit | 50 |
| Normal | 1 hit | 100 |
| Tank | 3 hits | 300 |

### Difficulty Progression
- Each level increases speed by 10%
- Aliens move faster, bullets move faster
- Fleet composition changes randomly
- Game continues until 3 ships are lost

## Code Quality

- **100% Documented**: All modules, classes, and functions have comprehensive docstrings
- **Well-Commented**: Inline comments explain complex game logic
- **Object-Oriented Design**: Clean class hierarchy for Ship, Bullet, Alien, Particle
- **Sprite Groups**: Efficient collision detection using pygame sprite groups
- **Modular Architecture**: Clear separation of concerns across 10 files

## Technologies Used

- **Python 3.13.2** - Programming language
- **Pygame 2.6.1** - Game development library
- **File I/O** - High score persistence
- **OOP** - Object-oriented programming paradigm

## Resources

- [Python Crash Course](https://nostarch.com/pythoncrashcourse2e/) - Primary textbook (Chapters 12-14)
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Python Documentation](https://docs.python.org/3/)

## Project Status

✅ Game completed with all required features  
✅ No syntax or logic errors  
✅ Comprehensive code documentation  
✅ Complete project documentation with architecture diagrams  
✅ Ready for video demonstration and submission  

## Author

**Arthur**  
CSC-121 Final Project  
May 2026

## Notes

The game automatically generates sprite images (ship.bmp and alien.bmp) on first run if they don't exist. High scores are saved to `highscores.txt` and persist between game sessions.

Enjoy the game!
