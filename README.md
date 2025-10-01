# Bullet-Hell-Minigame

A bullet hell minigame built with pygame featuring controller support, dynamic enemy spawning, and a progressive leveling system.

## Features

- **Dual-stick controller support** with Xbox controller compatibility
- **Dynamic enemy system** with multiple enemy types (normal, fast, tank)
- **Progressive leveling** that increases difficulty and introduces new enemy types
- **Component-based architecture** with modular entity classes
- **Real-time collision detection** using circle-based physics

## Getting Started

### Prerequisites

- Python 3.x
- pygame library
- Xbox controller or compatible gamepad (recommended)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Bullet-Hell-Minigame
   ```

2. Set up a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install pygame
   ```

*Note: To continue development later, simply repeat step 2 from above.

### Running the Game

```bash
# Run the main game
python3 game.py

# Run the legacy version (original prototype)
python3 ball_game.py

# Test controller input (debugging)
python3 debug/controller_util.py
```

## Controls

**Controller (Recommended):**
- **Left stick**: Move player
- **Right stick**: Aim and shoot bullets

**Note**: The game is designed primarily for controller input with deadzone handling for smooth gameplay.

## Game Mechanics

### Enemy Types
- **Red enemies**: Basic type with moderate speed and health
- **Orange enemies**: Fast enemies (unlock at level 3+) with less health but higher speed
- **Purple enemies**: Tank enemies (unlock at level 5+) with high health and damage but slower movement

### Progression System
- Level up based on score thresholds
- Higher levels increase enemy spawn rates and bullet fire rates
- New enemy types unlock at specific levels

## Project Structure

```
├── game.py          # Main game with modern architecture
├── ball_game.py     # Legacy/prototype version
├── player.py        # Player entity class
├── enemy.py         # Enemy entity classes
├── bullet.py        # Bullet projectile class
├── particle.py      # Particle entity class
├── constants.py     # Color definitions and screen dimensions
└── debug/controller_util.py    # Controller input debugging utility
```

## Architecture

The game uses a component-based architecture where each game entity is represented by its own class:

- **Player**: Handles movement, controller input, and shooting mechanics
- **Enemy**: Multiple enemy types with different behaviors and stats
- **Bullet**: Player projectiles that move based on right stick direction
- **Constants**: Centralized configuration for colors and screen dimensions

### Technical Details

- **Screen Resolution**: 1500x900 pixels
- **Frame Rate**: 60 FPS
- **Collision Detection**: Circle-based using distance calculations
- **Input Handling**: pygame joystick API with configurable deadzones

## Development

### Code Patterns

All game entities follow a consistent pattern:
- `__init__()`: Initialize position and properties
- `draw(screen)`: Render entity to pygame surface
- `update()` or `update(target)`: Update entity state per frame

### Controller Configuration

The game supports multiple controller layouts:
- Primary: Axis 0/1 (left stick), Axis 2/3 (right stick)
- Fallback: Axis 4/5 for right stick on some controllers
- Deadzone thresholds: 0.15 for movement, 0.3 for aiming

## Contributing

When contributing to this project:
1. Follow the existing component-based architecture
2. Use the established collision detection patterns
3. Maintain 60 FPS performance standards
4. Test with controller input for optimal experience

