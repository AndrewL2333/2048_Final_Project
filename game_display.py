import random
import math
import os
import sys
# Suppress the "Hello from the pygame community" message
with open(os.devnull, 'w') as fnull:
    sys.stdout = fnull
    import pygame 
    sys.stdout = sys.__stdout__ 

pygame.init()

# Animation
FPS = 60
VELOCITY = 50

# Game board size
WIDTH, HEIGHT = 400, 400 # total screen size
ROWS, COLS = 4, 4 # number of rows and columns in grid
TILE_HEIGHT, TILE_WIDTH = 100, 100 # pixel size of each tile
OUTLINE_THICKNESS = 10

# Game board color
OUTLINE_COLOR = (187, 173, 160)
BACKGROUND_COLOR = (205, 192, 180)

# Font setting
FONT = pygame.font.SysFont("arial", 40)
FONT_COLOR = (119, 110, 101)

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")