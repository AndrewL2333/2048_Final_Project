import os
import sys

# 
# Suppress the "Hello from the pygame community" message
with open(os.devnull, 'w') as fnull:
    sys.stdout = fnull
    import pygame 
    sys.stdout = sys.__stdout__ 
import random

pygame.init()

class Config:
    # Game board configuration
    SIZE = 4             # Number of rows/columns in the grid
    TILE_SIZE = 100      # Pixel size of each tile
    GAP_SIZE = 10        # Gap between tiles in pixels
    MARGIN = 20          # Margin around the board in pixels

    # Compute the total screen size based on the above values
    SCREEN_SIZE = SIZE * TILE_SIZE + (SIZE + 1) * GAP_SIZE + 2 * MARGIN
    SCREEN_WIDTH = SCREEN_SIZE
    SCREEN_HEIGHT = SCREEN_SIZE

    # Color configuration
    BACKGROUND_COLOR = (255, 251, 240)  # Background color of the game board
    EMPTY_TILE_COLOR = (205, 192, 180)  # Color for empty tiles
    TILE_COLORS = {                      # Different colors for different tile values
        2: (238, 228, 218),
        4: (237, 224, 200),
        8: (242, 177, 121),
        16: (245, 149, 99),
        32: (246, 124, 95),
        64: (246, 94, 59),
        128: (237, 207, 114),
        256: (237, 204, 97),
        512: (237, 200, 80),
        1024: (237, 197, 63),
        2048: (237, 194, 46)
    }

    # Font settings
    FONT_COLOR = (0, 0, 0)  # Color of the text on tiles
    FONT = pygame.font.SysFont('arial', 40)  # Font used to render tile values

    # Animation
    FPS = 60
    MOVE_VEL = 20

class Board:
    """Handles all logic related to the game board state and moves."""
    def __init__(self, size=Config.SIZE):
        self.size = size
        # Initialize a 2D list filled with zeros to represent an empty board
        self.board = [[0] * size for _ in range(size)]
        # Add tracking to positions
        self.positions = {}
        
    def add_new_tile(self):
        """Places a new tile (2 or 4) in a random empty position on the board."""
        empty_tiles = [(r, c) for r in range(self.size) for c in range(self.size) if self.board[r][c] == 0]
        if empty_tiles:
            row, col = random.choice(empty_tiles)
            self.board[row][col] = 2 if random.random() < 0.9 else 4

    def slide_row_left(self, row):
        """Slides and merges a single row to the left according to 2048 rules."""
        # Filter out zeros to compress tiles to the left
        new_row = [i for i in row if i != 0]

        # Merge adjacent tiles of the same value
        for i in range(len(new_row)-1):
            if new_row[i] == new_row[i+1]:
                new_row[i] *= 2
                new_row[i+1] = 0

        # Filter zeros again after merging
        new_row = [i for i in new_row if i != 0]

        # Add trailing zeros to maintain row size
        new_row += [0] * (self.size - len(new_row))
        return new_row

    def move_left(self):
        """Perform a left move on the entire board."""
        self.board = [self.slide_row_left(row) for row in self.board]

    def move_right(self):
        """Perform a right move on the entire board."""
        # Reverse each row, slide left, then reverse back
        self.board = [self.slide_row_left(row[::-1])[::-1] for row in self.board]

    def move_up(self):
        """Perform an upward move on the entire board."""
        # Transpose, slide left, transpose back
        transposed = list(zip(*self.board))
        moved = [self.slide_row_left(list(row)) for row in transposed]
        self.board = [list(row) for row in zip(*moved)]

    def move_down(self):
        """Perform a downward move on the entire board."""
        # Transpose, reverse each row (simulate down as reverse-up), slide, reverse and transpose back
        transposed = list(zip(*self.board))
        moved = [self.slide_row_left(list(row[::-1]))[::-1] for row in transposed]
        self.board = [list(row) for row in zip(*moved)]

    def check_win(self):
        """Check if the board contains a 2048 tile."""
        return any(2048 in row for row in self.board)

    def check_moves_available(self):
        """Check if there are any moves left (either empty spaces or possible merges)."""
        # Check for empty spaces
        for row in self.board:
            if 0 in row:
                return True

        # Check horizontal merges
        for row in self.board:
            for c in range(self.size - 1):
                if row[c] == row[c + 1]:
                    return True

        # Check vertical merges
        for c in range(self.size):
            for r in range(self.size - 1):
                if self.board[r][c] == self.board[r + 1][c]:
                    return True

        # No empty spaces or merges available means no moves left
        return False


class Renderer:
    """Handles all the drawing and rendering of the game to the screen."""
    def __init__(self, screen, font=Config.FONT):
        self.screen = screen
        self.font = font

    def draw_tile(self, value, x, y):
        """Draw a single tile with its value at position (x, y)."""
        # Get tile color from dictionary or default color for large numbers
        color = Config.TILE_COLORS.get(value, (60, 58, 50))
        rect = pygame.Rect(x, y, Config.TILE_SIZE, Config.TILE_SIZE)
        pygame.draw.rect(self.screen, color, rect)
        # Render the tile number if it's not empty
        if value != 0:
            text = self.font.render(str(value), True, Config.FONT_COLOR)
            text_rect = text.get_rect(center=(x + Config.TILE_SIZE / 2, y + Config.TILE_SIZE / 2))
            self.screen.blit(text, text_rect)

    def draw_board(self, board):
        """Draw the entire board with all the tiles."""
        self.screen.fill(Config.BACKGROUND_COLOR)
        for r in range(Config.SIZE):
            for c in range(Config.SIZE):
                value = board[r][c]
                # Calculate the tile position based on margins, gaps, and tile size
                x = Config.MARGIN + Config.GAP_SIZE + c * (Config.TILE_SIZE + Config.GAP_SIZE)
                y = Config.MARGIN + Config.GAP_SIZE + r * (Config.TILE_SIZE + Config.GAP_SIZE)
                self.draw_tile(value, x, y)

    def draw_message(self, message):
        """Draw a message (like 'You won!' or 'You lost!') in the center of the screen."""
        text = self.font.render(message, True, (255, 0, 0))
        text_rect = text.get_rect(center=(Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)


class Game:
    """Manages the main game loop, event handling, and orchestrates Board and Renderer."""
    def __init__(self):
        # Initialize the game window
        self.screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        pygame.display.set_caption("2048 Game")
        self.clock = pygame.time.Clock()

        # Create the board and renderer
        self.board = Board(Config.SIZE)
        self.renderer = Renderer(self.screen)

        # Add the initial two tiles
        self.board.add_new_tile()
        self.board.add_new_tile()

        self.running = True   # Game loop control
        self.won = False      # Track if the player has won
        self.lost = False     # Track if the player has lost

    def handle_input(self):
        """Handle player input from the keyboard and other events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False  # Exit the game loop
            elif event.type == pygame.KEYDOWN and not self.won and not self.lost:
                # If the player hasn't won or lost, handle arrow keys to move tiles
                moved = False
                if event.key == pygame.K_LEFT:
                    self.board.move_left()
                    moved = True
                elif event.key == pygame.K_RIGHT:
                    self.board.move_right()
                    moved = True
                elif event.key == pygame.K_UP:
                    self.board.move_up()
                    moved = True
                elif event.key == pygame.K_DOWN:
                    self.board.move_down()
                    moved = True

                if moved:
                    # After a valid move, add a new tile
                    self.board.add_new_tile()
                    # Check if the player has won by getting 2048
                    self.won = self.board.check_win()
                    # Check if there are still moves available; if not, player lost
                    self.lost = not self.board.check_moves_available()

    def update(self):
        """Update game logic if needed. 
        Currently, all logic is handled directly in handle_input for simplicity."""
        pass

    def render(self):
        """Render the current board state and messages to the screen."""
        self.renderer.draw_board(self.board.board)

        # Display messages if the game is won or lost
        if self.won:
            self.renderer.draw_message("You won!")
        elif self.lost:
            self.renderer.draw_message("You lost!")

        # Update the display
        pygame.display.flip()

    def run(self):
        """Run the main game loop until the player quits."""
        while self.running:
            self.handle_input()
            self.update()
            self.render()
            # Limit the frame rate to 30 FPS
            self.clock.tick(30)

        pygame.quit()


if __name__ == "__main__":
    # Create a Game instance and start the loop
    Game().run()
