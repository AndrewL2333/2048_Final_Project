import pygame

pygame.init()

screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("中文字体测试")

font = pygame.font.Font("chinese.ttf", 40)
text_surface = font.render("一二三四", True, (255, 255, 255))

screen.fill((0, 0, 0))
screen.blit(text_surface, (50, 50))
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
