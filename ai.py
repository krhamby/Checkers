from node import Node
from board import Board

from math import inf

# for debugging
# import pygame
# import settings
# from time import sleep

# pygame.init()
# WINDOW  = pygame.display.set_mode((settings.WIDTH, settings.WIDTH + settings.FOOTER_HEIGHT))
# CLOCK = pygame.time.Clock()
class AI:    
    def __init__(self, color):
        self.color = color
    
    def generate_graph(self, depth: int, startingState: Board, parent: Node):
        if depth == 0:
            # base case
            return Node(startingState, parent=parent, children=[])
        else:
            for s in startingState.squares:
                if s.has_piece() and s.piece.color == startingState.current_player:
                    
                    state = startingState.deep_copy()
                    state.select_square(x=s.top_left_x, y=s.top_left_y)
                    
                    # make_move is tailored for a human player, so we will manually set the selected square and calculate possible moves
                    # startingState.selected_square = s
                    # startingState.calculate_possible_moves(currentSquare=(startingState.selected_square, startingState.selected_square))
                    
                    for move in state.possible_moves:
                        temp = state.deep_copy()
                        temp.selected_square = None
                        temp.select_square(x=s.top_left_x, y=s.top_left_y)
                        temp.player_make_move(x_index=move[0].x, y_index=move[0].y, ai = True)
                        
                        node = Node(temp, parent=parent, children=[])
                        
                        # TODO: add heuristic
                        if startingState.current_player != self.color:
                            # other player's turn
                            node.heuristic = -3 * temp.captured_opponent_kings_count - 2 * temp.captured_opponent_kings_count - temp.captured_opponent_pieces_count
                        else:
                            # my turn
                            node.heuristic = 3 * temp.captured_opponent_kings_count + 2 * temp.captured_opponent_kings_count + temp.captured_opponent_pieces_count
                        
                        parent.children.append(node)
                        
                        self.generate_graph(depth - 1, temp, parent=node)
                        
                    # since we do not make a move in the original board, we need to reset some things
                    # startingState.selected_square = None
                    # startingState.possible_moves = []
                    
    def minimax(self, state: Board, depth: int, alpha, beta, max_player: bool):
        if depth == 0:
            # base case
            h = state.get_heuristic(color=self.color)
            state.heuristic = h
            return (h, state)
        if max_player:
            max_heuristic = -inf
            best_state = state
           
            state.get_all_possible_moves()
            for move in state.possible_moves:
                child_state = state.deep_copy()
                child_state.ai_make_move(initial_x_coord=move[2].top_left_x, initial_y_coord=move[2].top_left_y, 
                                         target_x_index=move[0].x, target_y_index=move[0].y)
                
                heuristic = self.minimax(child_state, depth - 1, alpha, beta, False)
                max_heuristic = max(max_heuristic, heuristic[0])
                best_state = max(best_state, heuristic[1], key=lambda x: x.heuristic)
                
                alpha = max(alpha, heuristic[0])
                if beta <= alpha:
                    # get pruned
                    break
            best_state.heuristic = max_heuristic
            return (max_heuristic, best_state)
        else:
            min_heuristic = inf
            best_state = state
            
            state.get_all_possible_moves()
            for move in state.possible_moves:
                child_state = state.deep_copy()
                child_state.ai_make_move(initial_x_coord=move[2].top_left_x, initial_y_coord=move[2].top_left_y,
                                         target_x_index=move[0].x, target_y_index=move[0].y)
                
                heuristic = self.minimax(child_state, depth - 1, alpha, beta, True)
                min_heuristic = min(min_heuristic, heuristic[0])
                best_state = min(best_state, heuristic[1], key=lambda x: x.heuristic)
                
                beta = min(beta, heuristic[0])
                if beta <= alpha:
                    # get pruned
                    break
            best_state.heuristic = min_heuristic
            return (min_heuristic, best_state)
    
    def get_best_max_move(self):
        pass
    
    def get_best_min_move(self):
        pass
    
   
# if __name__ == "__main__":
#     board = Board()
#     ai = AI(settings.TAN)
#     board.draw(WINDOW)
#     pygame.display.flip()
    
#     ai.minimax(board, 3, -inf, inf, True)[1]
    
     
        
    
    
    