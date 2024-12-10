from Grid import Grid
from ComputerAI import ComputerAI
from IntelligentAgent import IntelligentAgent
from game_display_2 import Config, draw, WINDOW, generate_tiles, Tile
import pygame
import time
import random
import sys

defaultInitialTiles = 2
defaultProbability = 0.9

actionDic = {
    0: "UP",
    1: "DOWN",
    2: "LEFT",
    3: "RIGHT",
    None: "NONE"  # For error logging
}

(PLAYER_TURN, COMPUTER_TURN) = (0, 1)

timeLimit = 0.4
allowance = 0.05
maxTime = timeLimit + allowance


class GameManager:
    def __init__(self, size=4, intelligentAgent=None, computerAI=None):
        self.grid = Grid(size)
        self.possibleNewTiles = [2, 4]
        self.probability = 0.9
        self.initTiles = 2
        self.over = False

        # Initialize the AI players
        self.computerAI = computerAI or ComputerAI()
        self.intelligentAgent = intelligentAgent or IntelligentAgent()

        # Initialize the GUI
        self.tiles = generate_tiles()
        self.screen = WINDOW

    def getNewTileValue(self):
        """ Returns 2 with probability 0.9 and 4 with 0.1 """
        return self.possibleNewTiles[random.random() > self.probability]

    def insertRandomTiles(self, numTiles):
        """ Insert numTiles number of random tiles. For initialization """
        for _ in range(numTiles):
            tileValue = self.getNewTileValue()
            cells = self.grid.getAvailableCells()
            cell = random.choice(cells) if cells else None
            self.grid.setCellValue(cell, tileValue)

    def update_tiles(self):
        """Sync the grid state with the tiles dictionary for rendering."""
        self.tiles.clear()
        for r in range(Config.ROWS):
            for c in range(Config.COLS):
                value = self.grid.map[r][c]
                if value != 0:
                    self.tiles[f"{r}{c}"] = Tile(value, r, c)

    def animate_move(self, direction):
        """Animates the movement of tiles in the specified direction."""
        clock = pygame.time.Clock()
        updated = True

        while updated:
            updated = False
            clock.tick(Config.FPS)

            for r in range(Config.ROWS):
                for c in range(Config.COLS):
                    tile_value = self.grid.map[r][c]
                    if tile_value != 0:
                        tile = self.tiles.get(f"{r}{c}")
                        if not tile:
                            continue

                        # Calculate target position based on the direction
                        target_row, target_col = r, c
                        if direction == 0:  # UP
                            while target_row > 0 and self.grid.map[target_row - 1][c] == 0:
                                target_row -= 1
                        elif direction == 1:  # DOWN
                            while target_row < Config.ROWS - 1 and self.grid.map[target_row + 1][c] == 0:
                                target_row += 1
                        elif direction == 2:  # LEFT
                            while target_col > 0 and self.grid.map[r][target_col - 1] == 0:
                                target_col -= 1
                        elif direction == 3:  # RIGHT
                            while target_col < Config.COLS - 1 and self.grid.map[r][target_col + 1] == 0:
                                target_col += 1

                        # Move the tile with a fixed speed
                        target_x = target_col * Config.TILE_WIDTH
                        target_y = target_row * Config.TILE_HEIGHT

                        delta_x = target_x - tile.x
                        delta_y = target_y - tile.y

                        if abs(delta_x) > Config.VELOCITY:
                            tile.x += Config.VELOCITY if delta_x > 0 else -Config.VELOCITY
                            updated = True
                        else:
                            tile.x = target_x

                        if abs(delta_y) > Config.VELOCITY:
                            tile.y += Config.VELOCITY if delta_y > 0 else -Config.VELOCITY
                            updated = True
                        else:
                            tile.y = target_y

                        # Update tile position based on the current animation
                        tile.set_pos()

            # Render the board
            draw(self.screen, self.tiles)
            pygame.display.update()



    def show_end_menu(self):
        """Displays the end menu with options to quit or restart."""
        font = pygame.font.SysFont("arial", 30)
        text_quit = font.render("Press Q to Quit", True, (255, 255, 255))
        text_restart = font.render("Press R to Restart", True, (255, 255, 255))

        while True:
            self.screen.fill(Config.BACKGROUND_COLOR)

            # Draw the final state of the grid
            draw(self.screen, self.tiles)

            # Display options
            self.screen.blit(text_quit, (Config.WIDTH // 2 - text_quit.get_width() // 2, Config.HEIGHT // 2 - 50))
            self.screen.blit(text_restart, (Config.WIDTH // 2 - text_restart.get_width() // 2, Config.HEIGHT // 2 + 50))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_r:
                        self.reset_game()
                        return

    def reset_game(self):
        """Resets the game state and starts a new game."""
        self.grid = Grid(self.grid.size)
        self.tiles = generate_tiles()
        self.over = False
        self.start()


    def start(self):
        """Main method that handles running the game of 2048 with animation."""
        clock = pygame.time.Clock()
        turn = PLAYER_TURN  # Player AI Goes First

        while self.grid.canMove() and not self.over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.over = True
                    break

            gridCopy = self.grid.clone()
            move = None

            if turn == PLAYER_TURN:
                move = self.intelligentAgent.getMove(gridCopy)

                if move is not None and 0 <= move < 4 and self.grid.canMove([move]):
                    self.animate_move(move)  # Add animation
                    self.grid.move(move)    # Perform the move on the grid
                else:
                    self.over = True

            else:
                move = self.computerAI.getMove(gridCopy)
                if move and self.grid.canInsert(move):
                    self.grid.setCellValue(move, self.getNewTileValue())
                else:
                    self.over = True

            # Update the tiles dictionary to reflect the grid state
            self.update_tiles()

            # Render the board
            draw(self.screen, self.tiles)
            pygame.display.update()
            clock.tick(Config.FPS)

            turn = 1 - turn

        # Display the final state and show the end menu
        self.show_end_menu()
        return self.grid.getMaxTile()



if __name__ == "__main__":
    intelligentAgent = IntelligentAgent()
    computerAI = ComputerAI()
    gameManager = GameManager(4, intelligentAgent, computerAI)
    maxTile = gameManager.start()
    print("Game Over. Max tile reached:", maxTile)
