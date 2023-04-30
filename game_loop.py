import pygame
import settings

from board import Board
from footer import Footer

from ai import AI
from node import Node
from math import inf
from time import sleep

pygame.init()
pygame.display.set_caption("Checkers")
WINDOW = pygame.display.set_mode((settings.WIDTH, settings.WIDTH + settings.FOOTER_HEIGHT))
CLOCK = pygame.time.Clock()
running = True

board = Board()
footer = Footer()

turn = True

ai, ai_2 = AI(settings.TAN), AI(settings.RED)

while running:
    if settings.GAME_MODE == settings.GameMode.TWO_PLAYER:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()  
                fc = (False, None)
                if board.selected_square == None: 
                    fc = board.force_capture()
                if fc[0] and fc[1] != None and board.selected_square == None:
                    board.select_square(fc[1].top_left_x, fc[1].top_left_y)
                    
                    # if board.selected_square != None:
                    #     board.player_make_move(mouse[0], mouse[1])
                    # board.player_make_move(mouse[0], mouse[1])
                elif not board.just_jumped and not fc[0]:
                    board.select_square(mouse[0], mouse[1])
                
                if board.selected_square != None:
                    board.player_make_move(mouse[0], mouse[1])
    elif settings.GAME_MODE == settings.GameMode.SINGLE_PLAYER_AI:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and board.current_player == settings.TAN:
                mouse = pygame.mouse.get_pos()  
                fc = (False, None)
                if board.selected_square == None: 
                    fc = board.force_capture()
                if fc[0] and fc[1] != None and board.selected_square == None:
                    board.possible_moves = []
                    board.select_square(fc[1].top_left_x, fc[1].top_left_y, force=True)
                    
                    # if board.selected_square != None:
                    #     board.player_make_move(mouse[0], mouse[1])
                    # board.player_make_move(mouse[0], mouse[1])
                elif not board.just_jumped and not fc[0]:
                    board.select_square(mouse[0], mouse[1])
                
                if board.selected_square != None:
                    board.player_make_move(mouse[0], mouse[1])
                
            elif board.current_player == settings.RED:
                fc = board.force_capture()
                if fc[0] and fc[1] != None and fc[2] != None:
                    board.ai_make_move(initial_x_coord=fc[1].top_left_x, initial_y_coord=fc[1].top_left_y,
                                        target_x_index=fc[2].x, target_y_index=fc[2].y)
                    board.selected_square = None
                    board.possible_moves = []
                else:
                    board.heuristic = -inf
                    output = ai_2.minimax(board, settings.PLY, -inf, inf, True)
                    
                    print(output[0])
                    
                    if board != output[1]:
                        print("AI made a move")
                        
                    board = output[1]
                    board.selected_square = None
                    board.possible_moves = []
    else:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False
        else:
            if turn:
                fc = board.force_capture()
                if fc[0] and fc[1] != None and fc[2] != None:
                    board.ai_make_move(initial_x_coord=fc[1].top_left_x, initial_y_coord=fc[1].top_left_y,
                                        target_x_index=fc[2].x, target_y_index=fc[2].y)
                else:
                    board.heuristic = -inf
                    output = ai.minimax(board, settings.PLY, -inf, inf, True)
                    
                    if board != output[1]:
                        print("AI1 made a move")
                        print(output[0])
                    
                    board = output[1]
                    
                turn = False
            else:
                fc = board.force_capture()
                if fc[0] and fc[1] != None and fc[2] != None:
                    board.ai_make_move(initial_x_coord=fc[1].top_left_x, initial_y_coord=fc[1].top_left_y,
                                        target_x_index=fc[2].x, target_y_index=fc[2].y)
                else:
                    board.heuristic = -inf
                    output = ai_2.minimax(board, settings.PLY, -inf, inf, True)
                    
                    if board != output[1]:
                        print("AI2 made a move")
                        
                    board = output[1]
                
                turn = True
    
    footer.draw(WINDOW, board.current_player)
    board.draw(WINDOW)
    pygame.display.flip()
    CLOCK.tick(60)
    
    if settings.GAME_MODE == settings.GameMode.TWO_PLAYER_AI:
        sleep(0.5)

pygame.quit()
