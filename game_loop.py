import pygame
import settings

from board import Board
from footer import Footer

pygame.init()
pygame.display.set_caption("Checkers")
WINDOW = pygame.display.set_mode((settings.WIDTH, settings.WIDTH + settings.FOOTER_HEIGHT))
CLOCK = pygame.time.Clock()
running = True

board = Board()
footer = Footer()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse = pygame.mouse.get_pos()
            if not board.just_jumped:
                board.select_square(mouse[0], mouse[1])
            
            if board.selected_square != None:
                board.make_move(mouse[0], mouse[1])
        
    footer.draw(WINDOW, board.current_player)
    board.draw(WINDOW)
    pygame.display.flip()
    CLOCK.tick(60)

pygame.quit()
