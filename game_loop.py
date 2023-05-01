import pygame
import settings

from board import Board
from footer import Footer

from ai import AI
from node import Node
from math import inf
import random
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
    if not board.game_over():
        if settings.GAME_MODE == settings.GameMode.TWO_PLAYER:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse = pygame.mouse.get_pos()  
                    fc = []
                    if board.selected_square == None: 
                        fc = board.force_capture()
                        
                    if len(fc) > 0 and board.selected_square == None:
                        board.select_square(mouse[0], mouse[1], force_moves=fc)
                    elif not board.just_jumped and fc == []:
                        board.select_square(mouse[0], mouse[1])
                    
                    if board.selected_square != None:
                        board.player_make_move(mouse[0], mouse[1])
        elif settings.GAME_MODE == settings.GameMode.SINGLE_PLAYER_AI:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and board.current_player == settings.TAN:
                    mouse = pygame.mouse.get_pos()  
                    fc = []
                    if board.selected_square == None: 
                        fc = board.force_capture()
                        
                    if len(fc) > 0 and board.selected_square == None:
                        board.possible_moves = []
                        board.select_square(mouse[0], mouse[1], force=True, force_moves=fc)
                        
                    elif not board.just_jumped and fc == []:
                        board.select_square(mouse[0], mouse[1])
                    
                    if board.selected_square != None:
                        board.player_make_move(mouse[0], mouse[1])
                    
                elif board.current_player == settings.RED:
                    fc = board.force_capture()
                    if len(fc) > 0:
                        highest_heuristic = -inf
                        best = board
                        for forced_move in fc:
                            copy = board.deep_copy()
                            copy.ai_make_move(initial_x_coord=forced_move[1].top_left_x, initial_y_coord=forced_move[1].top_left_y,
                                                target_x_index=forced_move[2].x, target_y_index=forced_move[2].y)
                            copy.selected_square = None
                            copy.possible_moves = []
                            
                            highest_heuristic = max(highest_heuristic, copy.get_heuristic(ai_2.color))
                            if highest_heuristic == copy.get_heuristic(ai_2.color):
                                best = copy
                        board = best
                    else:
                        board.heuristic = -inf
                        output = ai_2.minimax(board, settings.PLY, -inf, inf, True)
                        
                        if board != output[1]:
                            print("AI made a move")
                            print("Heuristic: " + str(output[0]))
                            
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
                    if len(fc) > 0:
                        highest_heuristic = -inf
                        best = board
                        for forced_move in fc:
                            copy = board.deep_copy()
                            copy.ai_make_move(initial_x_coord=forced_move[1].top_left_x, initial_y_coord=forced_move[1].top_left_y,
                                                target_x_index=forced_move[2].x, target_y_index=forced_move[2].y)
                            copy.selected_square = None
                            copy.possible_moves = []
                            
                            highest_heuristic = max(highest_heuristic, copy.get_heuristic(ai.color))
                            if highest_heuristic == copy.get_heuristic(ai.color):
                                best = copy
                        board = best
                    else:
                        board.heuristic = -inf
                        output = ai.minimax(board, settings.PLY, -inf, inf, True)
                        
                        if board != output[1]:
                            print("AI1 made a move")
                            print("Heuristic: " + str(output[0]))
                        
                        board = output[1]
                        
                    turn = False
                else:
                    fc = board.force_capture()
                    if len(fc) > 0:
                        highest_heuristic = -inf
                        best = board
                        for forced_move in fc:
                            copy = board.deep_copy()
                            copy.ai_make_move(initial_x_coord=forced_move[1].top_left_x, initial_y_coord=forced_move[1].top_left_y,
                                                target_x_index=forced_move[2].x, target_y_index=forced_move[2].y)
                            copy.selected_square = None
                            copy.possible_moves = []
                            
                            highest_heuristic = max(highest_heuristic, copy.get_heuristic(ai_2.color))
                            if highest_heuristic == copy.get_heuristic(ai_2.color):
                                best = copy
                        board = best
                    else:
                        board.heuristic = -inf
                        output = ai_2.minimax(board, settings.PLY, -inf, inf, True)
                        
                        if board != output[1]:
                            print("AI2 made a move")
                            print("Heuristic: " + str(output[0]))
                            
                        board = output[1]
                    
                    turn = True
        
    footer.draw(WINDOW, board.current_player)
    board.draw(WINDOW)
    
    if board.game_over():
        if board.current_player == settings.TAN:
            footer.draw_winner(WINDOW, "Red")
        else:
            footer.draw_winner(WINDOW, "Tan")
    
    pygame.display.flip()
    CLOCK.tick(60)
    
    if settings.GAME_MODE == settings.GameMode.TWO_PLAYER_AI:
        sleep(0.5)
    
    if board.game_over():
        sleep(5)
        running = False

pygame.quit()
