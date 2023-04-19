import pygame
import settings

from board import Board

pygame.init()
pygame.display.set_caption("Checkers")
WINDOW = pygame.display.set_mode((settings.WIDTH, settings.WIDTH))
CLOCK = pygame.time.Clock()
running = True

board = Board()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            board.highlight_square(mouse[0], mouse[1])
            
    board.draw(WINDOW)
    pygame.display.flip()
    CLOCK.tick(60)

pygame.quit()
