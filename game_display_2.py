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

class Config:
    # Animation 
    FPS = 60
    VELOCITY = 5

    # Game board size
    WIDTH, HEIGHT = 400, 400 # total screen size
    ROWS, COLS = 4, 4 # number of ROWS and columns in grid
    TILE_HEIGHT, TILE_WIDTH = 100, 100 # pixel size of each tile
    OUTLINE_THICKNESS = 10

    # Game board color
    OUTLINE_COLOR = (187, 173, 160)
    BACKGROUND_COLOR = (205, 192, 180)

    # Config.FONT setting
    FONT = pygame.font.SysFont("arial", 40)
    FONT_COLOR = (119, 110, 101)

WINDOW = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
pygame.display.set_caption("2048")


class Tile:
    TILE_COLORS = [
        (237, 229, 218),
        (238, 225, 201),
        (243, 178, 122),
        (246, 150, 101),
        (247, 124, 95),
        (247, 95, 59),
        (237, 208, 115),
        (237, 204, 99),
        (236, 202, 80),
        (237, 197, 63),
        (237, 194, 46)
    ]

    def __init__(self, value, row, col):
        self.value = value # 2, 4, 8, etc
        self.row = row # grid position
        self.col = col # grid position
        self.x = col * Config.TILE_WIDTH # pixel position
        self.y = row * Config.TILE_HEIGHT # pixel position

    def get_color(self):
        color_index = int(math.log2(self.value)) - 1
        color = self.TILE_COLORS[color_index]
        return color

    def draw(self, window):
        pygame.draw.rect(
            window, 
            self.get_color(), 
            (self.x, self.y, Config.TILE_WIDTH, Config.TILE_HEIGHT),
            border_radius=10)

        text = Config.FONT.render(str(self.value), 1, Config.FONT_COLOR)
        window.blit(
            text,
            (
                self.x + (Config.TILE_WIDTH / 2 - text.get_width() / 2),
                self.y + (Config.TILE_HEIGHT / 2 - text.get_height() / 2),
            ),
        )

    def set_pos(self, ceil=False):
        if ceil:
            self.row = math.ceil(self.y / Config.TILE_HEIGHT)
            self.col = math.ceil(self.x / Config.TILE_WIDTH)
        else:
            self.row = math.floor(self.y / Config.TILE_HEIGHT)
            self.col = math.floor(self.x / Config.TILE_WIDTH)

    def move(self, delta):
        self.x += delta[0]
        self.y += delta[1]


def draw_grid(window):
    for row in range(1, Config.ROWS):
        y = row * Config.TILE_HEIGHT
        pygame.draw.line(window, Config.OUTLINE_COLOR, (0, y), (Config.WIDTH, y), Config.OUTLINE_THICKNESS)

    for col in range(1, Config.COLS):
        x = col * Config.TILE_WIDTH
        pygame.draw.line(window, Config.OUTLINE_COLOR, (x, 0), (x, Config.HEIGHT), Config.OUTLINE_THICKNESS)

    pygame.draw.rect(window, Config.OUTLINE_COLOR, (0, 0, Config.WIDTH, Config.HEIGHT), Config.OUTLINE_THICKNESS)


def draw(window, tiles):
    window.fill(Config.BACKGROUND_COLOR)

    for tile in tiles.values():
        tile.draw(window)

    draw_grid(window)

    pygame.display.update()


def get_random_pos(tiles):
    row = None
    col = None
    while True:
        row = random.randrange(0, Config.ROWS)
        col = random.randrange(0, Config.COLS)

        if f"{row}{col}" not in tiles:
            break

    return row, col


def move_tiles(window, tiles, clock, direction):
    updated = True
    blocks = set()

    if direction == "left":
        sort_func = lambda x: x.col
        reverse = False
        delta = (-Config.VELOCITY, 0)
        boundary_check = lambda tile: tile.col == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col - 1}")
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + Config.VELOCITY
        move_check = (
            lambda tile, next_tile: tile.x > next_tile.x + Config.TILE_WIDTH + Config.VELOCITY
        )
        ceil = True
    elif direction == "right":
        sort_func = lambda x: x.col
        reverse = True
        delta = (Config.VELOCITY, 0)
        boundary_check = lambda tile: tile.col == Config.COLS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col + 1}")
        merge_check = lambda tile, next_tile: tile.x < next_tile.x - Config.VELOCITY
        move_check = (
            lambda tile, next_tile: tile.x + Config.TILE_WIDTH + Config.VELOCITY < next_tile.x
        )
        ceil = False
    elif direction == "up":
        sort_func = lambda x: x.row
        reverse = False
        delta = (0, -Config.VELOCITY)
        boundary_check = lambda tile: tile.row == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row - 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y > next_tile.y + Config.VELOCITY
        move_check = (
            lambda tile, next_tile: tile.y > next_tile.y + Config.TILE_HEIGHT + Config.VELOCITY
        )
        ceil = True
    elif direction == "down":
        sort_func = lambda x: x.row
        reverse = True
        delta = (0, Config.VELOCITY)
        boundary_check = lambda tile: tile.row == Config.ROWS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row + 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y < next_tile.y - Config.VELOCITY
        move_check = (
            lambda tile, next_tile: tile.y + Config.TILE_HEIGHT + Config.VELOCITY < next_tile.y
        )
        ceil = False

    while updated:
        clock.tick(Config.FPS)
        updated = False
        sorted_tiles = sorted(tiles.values(), key=sort_func, reverse=reverse)

        for i, tile in enumerate(sorted_tiles):
            if boundary_check(tile):
                continue

            next_tile = get_next_tile(tile)
            if not next_tile:
                tile.move(delta)
            elif (
                tile.value == next_tile.value
                and tile not in blocks
                and next_tile not in blocks
            ):
                if merge_check(tile, next_tile):
                    tile.move(delta)
                else:
                    next_tile.value *= 2
                    sorted_tiles.pop(i)
                    blocks.add(next_tile)
            elif move_check(tile, next_tile):
                tile.move(delta)
            else:
                continue

            tile.set_pos(ceil)
            updated = True

        update_tiles(window, tiles, sorted_tiles)

    return end_move(tiles)


def end_move(tiles):
    if len(tiles) == 16:
        return "lost"

    row, col = get_random_pos(tiles)
    tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)
    return "continue"


def update_tiles(window, tiles, sorted_tiles):
    tiles.clear()
    for tile in sorted_tiles:
        tiles[f"{tile.row}{tile.col}"] = tile

    draw(window, tiles)


def generate_tiles():
    tiles = {}
    for _ in range(2):
        row, col = get_random_pos(tiles)
        tiles[f"{row}{col}"] = Tile(2, row, col)

    return tiles


def main(window):
    clock = pygame.time.Clock()
    run = True

    tiles = generate_tiles()

    while run:
        clock.tick(Config.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_tiles(window, tiles, clock, "left")
                if event.key == pygame.K_RIGHT:
                    move_tiles(window, tiles, clock, "right")
                if event.key == pygame.K_UP:
                    move_tiles(window, tiles, clock, "up")
                if event.key == pygame.K_DOWN:
                    move_tiles(window, tiles, clock, "down")

        draw(window, tiles)

    pygame.quit()


if __name__ == "__main__":
    main(WINDOW)