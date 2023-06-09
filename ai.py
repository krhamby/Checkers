from node import Node
from board import Board

from math import inf
import random

class AI:    
    def __init__(self, color):
        self.color = color
    
    def generate_graph(self, depth: int, startingState: Board, parent: Node):
        """
        Deprecated method for generating a graph of possible moves. This was the foundation for 
        our minimax algorith. We left it in for fun.
        
        Returns:
            a Node object representing the starting state of the board.
        """
        if depth == 0:
            # base case
            return Node(startingState, parent=parent, children=[])
        else:
            for s in startingState.squares:
                if s.has_piece() and s.piece.color == startingState.current_player:
                    
                    state = startingState.deep_copy()
                    state.select_square(x=s.top_left_x, y=s.top_left_y)
                    
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
                        
    def minimax(self, state: Board, depth: int, alpha, beta, max_player: bool):
        """
        Recursive minimax algorithm with alpha-beta pruning.
        
        Args:
            state: the current state of the board
            depth: the depth of the tree (can also say ply)
            alpha: the alpha value for alpha-beta pruning
            beta: the beta value for alpha-beta pruning
            max_player: whether or not the current player is the maximizing player
        """
        if depth == 0:
            # base case
            h = state.get_heuristic(color=self.color)
            state.heuristic = h
            return (h, state)
        if max_player:
            max_heuristic = -inf
            best_state = state
            
            # check if there are any forced captures
            fc = state.force_capture()
            if len(fc) > 0:
                # consider all forced captures
                for forced_move in fc:
                    child_state = state.deep_copy()
                    
                    child_state.possible_moves = []
                    child_state.ai_make_move(initial_x_coord=forced_move[1].top_left_x, initial_y_coord=forced_move[1].top_left_y,
                                                target_x_index=forced_move[2].x, target_y_index=forced_move[2].y, force_moves=fc)
                    
                    heuristic = self.minimax(child_state, depth - 1, alpha, beta, False)
                    max_heuristic = max(max_heuristic, heuristic[0])
                    best_state = max(best_state, heuristic[1], key=lambda x: x.heuristic)
                    
                    alpha = max(alpha, heuristic[0])
                    if beta <= alpha:
                        # get pruned
                        break
            else:
                # if there are no forced captures, consider all possible moves and recurse
                state.get_all_possible_moves()
                for move in state.possible_moves:
                    child_state = state.deep_copy()
                    child_state.ai_make_move(initial_x_coord=move[2].top_left_x, initial_y_coord=move[2].top_left_y, 
                                            target_x_index=move[0].x, target_y_index=move[0].y)
                    
                    heuristic = self.minimax(child_state, depth - 1, alpha, beta, False)
                    max_heuristic = max(max_heuristic, heuristic[0])
                    best_state = max(best_state, heuristic[1], key=lambda x: x.heuristic) # heuristic[1] is the state
                    
                    alpha = max(alpha, heuristic[0])
                    if beta <= alpha:
                        # get pruned
                        break
            best_state.heuristic = max_heuristic
            return (max_heuristic, best_state)
        else:
            min_heuristic = inf
            best_state = state
            
            # check if there are any forced captures
            fc = state.force_capture()
            if len(fc) > 0:
                for forced_move in fc:
                    child_state = state.deep_copy()
                    
                    child_state.possible_moves = []
                    child_state.ai_make_move(initial_x_coord=forced_move[1].top_left_x, initial_y_coord=forced_move[1].top_left_y,
                                                target_x_index=forced_move[2].x, target_y_index=forced_move[2].y, force_moves=fc)
                    
                    heuristic = self.minimax(child_state, depth - 1, alpha, beta, True)
                    min_heuristic = min(min_heuristic, heuristic[0])
                    best_state = min(best_state, heuristic[1], key=lambda x: x.heuristic)
                    
                    beta = min(beta, heuristic[0])
                    if beta <= alpha:
                        # get pruned
                        break
            else:
                # if there are no forced captures, consider all possible moves and recurse
                state.get_all_possible_moves()
                for move in state.possible_moves:
                    child_state = state.deep_copy()
                    child_state.ai_make_move(initial_x_coord=move[2].top_left_x, initial_y_coord=move[2].top_left_y,
                                            target_x_index=move[0].x, target_y_index=move[0].y)
                    
                    heuristic = self.minimax(child_state, depth - 1, alpha, beta, True)
                    min_heuristic = min(min_heuristic, heuristic[0])
                    best_state = min(best_state, heuristic[1], key=lambda x: x.heuristic) # heuristic[1] is the state
                    
                    beta = min(beta, heuristic[0])
                    if beta <= alpha:
                        # get pruned
                        break
            best_state.heuristic = min_heuristic
            return (min_heuristic, best_state)
    