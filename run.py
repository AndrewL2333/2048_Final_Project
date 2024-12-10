import pygame
from game_display_2 import main, Tile, update_tiles, move_tiles, generate_tiles, end_move
from IntelligentAgent import IntelligentAgent

def ai_game_loop(window):
    clock = pygame.time.Clock()
    run = True
    tiles = generate_tiles()
    agent = IntelligentAgent()

    while run:
        clock.tick(60)  # Set to desired game speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        move = agent.getMove(tiles)  # Get the move from the IntelligentAgent
        if move is not None:
            move_tiles(window, tiles, clock, move)

        update_tiles(window, tiles)  # Update the tiles on the game display
        status = end_move(tiles)  # Check if the game is lost or can continue
        if status == "lost":
            print("Game Over!")
            run = False

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    WINDOW = pygame.display.set_mode((400, 400))
    pygame.display.set_caption("2048 AI Version")
    ai_game_loop(WINDOW)
