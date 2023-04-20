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
        # print(event)
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse = pygame.mouse.get_pos()
            board.select_square(mouse[0], mouse[1])
            
            if board.selected_square != None:
                board.make_move(mouse[0], mouse[1])
        
        
    board.draw(WINDOW)
    pygame.display.flip()
    CLOCK.tick(60)

pygame.quit()
