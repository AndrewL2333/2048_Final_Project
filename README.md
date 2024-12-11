# 2048_Final_Project

# 2048 Game with AI Player

This project includes a Python implementation of the 2048 game with an AI-driven player. The game is displayed using Pygame, and the logic is contained within `game_display.py` and `AIPlayer.py`.

## Features
- **Multilingual Display**: Utilizes Chinese characters for tile numbers, providing a unique and culturally enriched gaming experience.
- Pygame-based graphical display of the game board.
- Configurable game settings through the `Config` class.
- AI algorithms to control both player and computer moves.

## Usage
Run `AIPlayer.py` to start the game. Ensure Pygame is installed and configured properly on your system.

## Dependencies
- Python 3.x
- Pygame

## Contributors
- Yue Liu, Peijia Ye



 
# Intellengent Agent:
 There are three strategy for rewarding choices of next coupple possible steps:
  1. The bigger the bigest number;
  2. The bigest number should be at the one of corners;
  3. Number should be increased as a snake shape;