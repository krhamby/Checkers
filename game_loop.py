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

game_draw = False

while running:
    if not board.game_over():
        if settings.GAME_MODE == settings.GameMode.TWO_PLAYER:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse = pygame.mouse.get_pos() 
                    
                    # if mouse is in footer, don't do anything (used to crash game) 
                    if mouse[1] >= settings.WIDTH:
                        break
                    
                    # if there isn't a square selected, see if the player must capture an opponent piece
                    fc = []
                    if board.selected_square == None: 
                        fc = board.force_capture()
                    
                    # if there is a forced capture, select the square and force the player to make the capture
                    if len(fc) > 0 and board.selected_square == None:
                        board.select_square(mouse[0], mouse[1], force_moves=fc)
                    elif not board.just_jumped and fc == []:
                        board.select_square(mouse[0], mouse[1])
                    
                    # once a square is selected based on the above, make a move
                    if board.selected_square != None:
                        board.player_make_move(mouse[0], mouse[1])
        elif settings.GAME_MODE == settings.GameMode.SINGLE_PLAYER_AI:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and board.current_player == settings.TAN:
                    mouse = pygame.mouse.get_pos() 
                    
                    # if mouse is in footer, don't do anything (used to crash game)
                    if mouse[1] >= settings.WIDTH:
                        break
                    
                    # if there isn't a square selected, see if the player must capture an opponent piece
                    fc = []
                    if board.selected_square == None: 
                        fc = board.force_capture()
                        
                    # if there is a forced capture, select the square and force the player to make the capture
                    # otherwise, select the square
                    if len(fc) > 0 and board.selected_square == None:
                        board.possible_moves = []
                        board.select_square(mouse[0], mouse[1], force=True, force_moves=fc)
                    elif not board.just_jumped and fc == []:
                        board.select_square(mouse[0], mouse[1])
                    
                    # once a square is selected based on the above, make a move
                    if board.selected_square != None:
                        board.player_make_move(mouse[0], mouse[1])
                    
                elif board.current_player == settings.RED:
                    # since we don't need to waste time running minimax if the AI must capture, we check for that first
                    fc = board.force_capture()
                    if len(fc) > 0:
                        highest_heuristic = -inf
                        best = board
                        
                        # loop through all possible captures and find the one with the highest heuristic
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
                    # since we don't need to waste time running minimax if the AI must capture, we check for that first
                    fc = board.force_capture()
                    if len(fc) > 0:
                        highest_heuristic = -inf
                        best = board
                        
                        # loop through all possible captures and find the one with the highest heuristic
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
                        
                        if output[0] == inf or output[0] == -inf:
                            print("Draw")
                            game_draw = True
                        
                    turn = False
                else:
                    # since we don't need to waste time running minimax if the AI must capture, we check for that first
                    fc = board.force_capture()
                    if len(fc) > 0:
                        highest_heuristic = -inf
                        best = board
                        
                        # loop through all possible captures and find the one with the highest heuristic
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
                        
                        if output[0] == inf or output[0] == -inf:
                            print("Draw")
                            game_draw = True
                    
                    turn = True
        
    footer.draw(WINDOW, board.current_player)
    board.draw(WINDOW)
    
    # if the game is over, draw the winner
    if board.game_over():
        if board.current_player == settings.TAN:
            footer.draw_winner(WINDOW, "Red")
        else:
            footer.draw_winner(WINDOW, "Tan")
    
    # if the game is a draw, draw the draw message
    if game_draw:
        footer.draw_draw(WINDOW)
    
    pygame.display.flip()
    CLOCK.tick(60)
    
    if settings.GAME_MODE == settings.GameMode.TWO_PLAYER_AI:
        sleep(0.5)
    
    # if the game is over, wait 5 seconds and then quit
    if board.game_over() or game_draw:
        sleep(5)
        running = False

pygame.quit()
