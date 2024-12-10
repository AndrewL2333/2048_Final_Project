from Grid import Grid
from ComputerAI import ComputerAI
from IntelligentAgent import IntelligentAgent
from game_display_2 import Config, draw, WINDOW, generate_tiles, Tile
import pygame
import time
import random

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

    def start(self):
        """ Main method that handles running the game of 2048 """
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
                    self.grid.move(move)
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

        pygame.quit()
        return self.grid.getMaxTile()


if __name__ == "__main__":
    intelligentAgent = IntelligentAgent()
    computerAI = ComputerAI()
    gameManager = GameManager(4, intelligentAgent, computerAI)
    maxTile = gameManager.start()
    print("Game Over. Max tile reached:", maxTile)
