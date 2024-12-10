from Grid import Grid
from ComputerAI import ComputerAI
from IntelligentAgent import IntelligentAgent
from game_display import Config, Renderer
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
        self.probability = defaultProbability
        self.initTiles = defaultInitialTiles
        self.over = False

        # Initialize the AI players
        self.computerAI = computerAI or ComputerAI()
        self.intelligentAgent = intelligentAgent or IntelligentAgent()

        # Initialize the GUI
        pygame.init()
        self.screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        pygame.display.set_caption("2048 Game")
        self.renderer = Renderer(self.screen)

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

    def start(self):
        """ Main method that handles running the game of 2048 """

        # Initialize the game
        self.insertRandomTiles(self.initTiles)
        self.renderer.draw_board(self.grid.map)
        pygame.display.flip()

        turn = PLAYER_TURN  # Player AI Goes First

        while self.grid.canMove() and not self.over:
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
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

            self.renderer.draw_board(self.grid.map)
            pygame.display.flip()
            turn = 1 - turn

        pygame.quit()
        return self.grid.getMaxTile()


if __name__ == "__main__":
    intelligentAgent = IntelligentAgent()
    computerAI = ComputerAI()
    gameManager = GameManager(4, intelligentAgent, computerAI)
    maxTile = gameManager.start()
    print("Game Over. Max tile reached:", maxTile)
