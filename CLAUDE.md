# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a bullet hell minigame built with pygame that supports controller input. The game features a player that can move and shoot at enemies that spawn and chase the player. The game has a leveling system that increases difficulty over time.

## Architecture

The codebase uses a component-based architecture with separate classes for each game entity:

- **Player** (`player.py`): Handles player movement, controller input, and shooting mechanics
- **Enemy** (`enemy.py`): Different enemy types (normal, fast, tank) that spawn and chase the player
- **Bullet** (`bullet.py`): Player projectiles that move in the direction of the right analog stick
- **Constants** (`constants.py`): Centralized color definitions and screen dimensions

### Game Files

- `game.py` - Main game loop with modern architecture using entity classes
- `ball_game.py` - Legacy/simpler version of the game (appears to be the original prototype)
- `debug/controller_util.py` - Utility for debugging controller input

### Input System

The game uses dual-stick controller controls:
- Left stick: Player movement (with deadzone handling)
- Right stick: Shooting direction (with deadzone handling)
- Supports Xbox controllers and similar gamepad layouts

### Enemy System

Enemies have different types based on player level:
- **Red enemies**: Basic type, moderate speed and health
- **Orange enemies**: Fast type (levels 3+), less health but higher speed
- **Purple enemies**: Tank type (levels 5+), slow but high health and damage

### Leveling System

- Player levels up based on score thresholds
- Higher levels spawn more enemies and introduce new enemy types
- Spawn rates and bullet fire rates increase with level progression

## Development Commands

### Running the Game

```bash
# Run the main game
python3 game.py

# Run the legacy version
python3 ball_game.py

# Debug controller input
python3 controller.py
```

### Dependencies

The project uses a virtual environment located at `path/to/venv/`. The main dependency is pygame.

```bash
# Activate virtual environment (if needed)
source path/to/venv/bin/activate

# Install pygame (if not already installed)
pip install pygame
```

## Code Patterns

### Entity Structure

All game entities follow a similar pattern:
- `__init__()`: Initialize position, properties, and type-specific attributes
- `draw(screen)`: Render the entity to the pygame screen
- `update()` or `update(target)`: Update entity state per frame
- Collision detection methods using distance calculations

### Collision Detection

The codebase uses circle-based collision detection with distance calculations:
```python
distance = sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
return distance < self.radius + other.radius
```

### Controller Input

Controller input uses pygame's joystick API with deadzone handling:
- Axis 0/1: Left stick (movement)
- Axis 2/3: Right stick (aiming) - with fallback to axis 4/5 for different controllers
- Deadzone threshold of 0.15 for movement, 0.3 for aiming

## File Structure Notes

- `constants.py` defines screen dimensions (1500x900) and color constants
- Game runs at 60 FPS using pygame's clock
- Uses pygame's built-in collision detection and rendering systems