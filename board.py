import pygame
import settings
from typing import List, Tuple

from square import Square
from piece import Piece

from math import inf
class Board:
    def __init__(self) -> None:
        self.squares = []
        self.selected_square = None
        self.possible_moves = []
        
        self.current_player = settings.TAN
        self.just_jumped = False
        
        # variables for AI stuff
        self.created_kings_count = 0
        
        self.captured_opponent_kings_count = 0
        self.captured_opponent_pieces_count = 0
        
        self.heuristic: float = -inf
        
        self.force = False
        
        for y in range(settings.SIZE):
            for x in range(settings.SIZE):
                if (y + x) % 2 == 0:
                    color = settings.WHITE
                else:
                    color = settings.BLACK
                
                square_x = x * settings.WIDTH / settings.SIZE
                square_y = y * settings.WIDTH / settings.SIZE
                
                piece_x = square_x + settings.SQUARE_SIZE / 2
                piece_y = square_y + settings.SQUARE_SIZE / 2
                
                piece = None
                if y < 3 and (y + x) % 2 == 1:
                    piece = Piece(piece_x, piece_y, settings.RED, settings.PIECE_RADIUS)
                elif y > 4 and (y + x) % 2 == 1:
                    piece = Piece(piece_x, piece_y, settings.TAN, settings.PIECE_RADIUS)
                
                self.squares.append(Square(square_x, square_y, x, y, color, piece))
                
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Board):
            return False
        
        for i in range(len(self.squares)):
            if self.squares[i].piece != __value.squares[i].piece:
                return False
        
        return True
    
    def draw(self, window):
        for square in self.squares:
            square.draw(window)
            
    def deep_copy(self):
        board_copy = Board()
        board_copy.squares = [] # this was THE bug
        for square in self.squares:
            board_copy.squares.append(square.deep_copy())
        
        # copy other properties (although we may not need them)
        board_copy.just_jumped = self.just_jumped
        board_copy.current_player = self.current_player
        board_copy.selected_square = board_copy.get_square_by_index(self.selected_square.x, self.selected_square.y) if self.selected_square != None else None
        
        for move in self.possible_moves:
            board_copy.possible_moves.append((move[0].deep_copy(), move[1].deep_copy()))
        
        return board_copy
    
    def game_over(self) -> bool:    
        one = self.one_piece_left(self.current_player)    
        
        for square in self.squares:
            if square.has_piece() and square.piece.color == self.current_player:
                if one:
                    self.calculate_possible_moves(currentSquare=(square, square, square))
                    if len(self.possible_moves) > 0:
                        self.possible_moves = []
                        return False
                else:
                    return False
            
        return True
    
    def one_piece_left(self, color) -> bool:
        count = 0
        for square in self.squares:
            if square.has_piece() and square.piece.color == color:
                count += 1
        return count == 1
    
    def get_heuristic(self, color) -> float:
        # do calculations here based on board
        num_pieces = 0
        num_opponent_pieces = 0
        num_kings = 0
        num_opponent_kings = 0
        
        num_center = 0
        num_opponent_center = 0
        
        num_king_center = 0
        num_opponent_king_center = 0
        
        num_opponent_king_row = 0
        
        for square in self.squares:
            if square.has_piece():
                if square.piece.color == color:
                    if square.piece.king:
                        num_kings += 1
                    num_pieces += 1
                    
                    if square.x >= 1 and square.x <= settings.SIZE - 2 and square.y >= 1 and square.y <= settings.SIZE - 2:
                        num_center += 1
                        if square.piece.king:
                            num_king_center += 1
                else:
                    if square.piece.king:
                        num_opponent_kings += 1
                    num_opponent_pieces += 1
                    
                    if square.x >= 1 and square.x <= settings.SIZE - 2 and square.y >= 1 and square.y <= settings.SIZE - 2:
                        num_opponent_center += 1
                        if square.piece.king:
                            num_opponent_king_center += 1
                    
                    if (square.y == 1 and square.piece.color == settings.TAN) or (square.y == settings.SIZE - 2 and square.piece.color == settings.RED):
                        num_opponent_king_row += 1
                        
        if num_pieces < 5 and num_opponent_pieces < 5:
            return num_opponent_pieces - num_pieces * 3
        
        heuristic = 0
        heuristic += num_pieces * 2
        heuristic += num_kings * 4
        heuristic += num_center * 3.5
        heuristic += num_king_center * 3
        
        heuristic -= num_opponent_pieces * 2
        heuristic -= num_opponent_kings * 5
        heuristic -= num_opponent_center * 3.5
        heuristic -= num_opponent_king_center * 2
        heuristic -= num_opponent_king_row * 3
        
        # num_pieces * 2 + num_kings * 5 + num_center * 3.5 - num_opponent_pieces * 1.5 - num_opponent_kings * 5 - num_opponent_center * 3
        
        return heuristic
    
    def get_all_possible_moves(self):
        for square in self.squares:
            if square.has_piece() and square.piece.color == self.current_player:
                self.force = False
                self.calculate_possible_moves(currentSquare=(square, square, square))
                
    def force_capture(self) -> List[Tuple[bool, Square, Square]]:
        temp = []
        for move in self.possible_moves:
            temp.append(move)
        
        force_moves = []
        for square in self.squares:
            if square.has_piece() and square.piece.color == self.current_player:
                self.calculate_possible_moves(currentSquare=(square, square, square))
                for move in self.possible_moves:
                    if move[0] != move[1]:
                        force_moves.append((True, move[2], move[0]))
                self.possible_moves = []
        self.possible_moves = temp
        
        if len(force_moves) > 0:
            return force_moves
        
        return []

    def select_square(self, x = None, y = None, square = None, force = False, force_moves = []):
        if square == None:
            square = self.get_square(x, y)
        if self.selected_square == None:
            if force_moves != []:
                for move in force_moves:
                    if move[1] == square:
                        self.selected_square = square
                        self.selected_square.highlight = True
                        self.force = True
                        self.calculate_possible_moves(currentSquare=(self.selected_square, self.selected_square, self.selected_square))
                        for s in self.possible_moves:
                            s[0].highlight = True
                        break
            elif square.has_piece() and square.piece.color == self.current_player:
                square.highlight = True
                self.selected_square = square
                self.force = force
                self.calculate_possible_moves(currentSquare=(self.selected_square, self.selected_square, self.selected_square))
                for square in self.possible_moves:
                    square[0].highlight = True
        else:
            if square == self.selected_square:
                square.highlight = False
                self.selected_square = None
                
                # reset possible moves
                for square in self.possible_moves:
                    square[0].highlight = False
                self.possible_moves = []
    
    def calculate_possible_moves(self, currentSquare: Tuple[Square, Square, Square]):
        if self.current_player == settings.TAN:
            self.add_moves_up(currentSquare)
            if currentSquare[0].piece.king:
                self.add_moves_down(currentSquare)
        else:
            self.add_moves_down(currentSquare)
            if currentSquare[0].piece.king:
                self.add_moves_up(currentSquare)
    
    
    def add_moves_up(self, currentSquare: Tuple[Square, Square, Square]):
        for i in range(-2, 3, 4):
            targetSquare = self.get_square_by_index(currentSquare[0].x + i, currentSquare[0].y - 2)
            jumpedSquare = self.get_square_by_index(currentSquare[0].x + i // 2, currentSquare[0].y - 1)
            if targetSquare and jumpedSquare:
                if (jumpedSquare.has_piece() and not targetSquare.has_piece() 
                    and jumpedSquare.piece.color != self.current_player and targetSquare not in self.possible_moves):
                    self.possible_moves.append((targetSquare, jumpedSquare, currentSquare[2]))
                    self.force = True
        
        if not self.just_jumped and not self.force:
            for i in range(-1, 2, 2):
                targetSquare = self.get_square_by_index(currentSquare[0].x + i, currentSquare[0].y - 1)
                if targetSquare:
                    if not targetSquare.has_piece() and targetSquare not in self.possible_moves:
                        self.possible_moves.append((targetSquare, targetSquare, currentSquare[2]))
        
        
    def add_moves_down(self, currentSquare: Tuple[Square, Square, Square]):
        for i in range(-2, 3, 4):
            targetSquare = self.get_square_by_index(currentSquare[0].x + i, currentSquare[0].y + 2)
            jumpedSquare = self.get_square_by_index(currentSquare[0].x + i // 2, currentSquare[0].y + 1)
            if targetSquare and jumpedSquare:
                if (jumpedSquare.has_piece() and not targetSquare.has_piece() 
                    and jumpedSquare.piece.color != self.current_player and targetSquare not in self.possible_moves):
                    self.possible_moves.append((targetSquare, jumpedSquare, currentSquare[2]))
                    self.force = True
        
        if not self.just_jumped and not self.force:
            for i in range(-1, 2, 2):
                targetSquare = self.get_square_by_index(currentSquare[0].x + i, currentSquare[0].y + 1)
                if targetSquare:
                    if not targetSquare.has_piece() and targetSquare not in self.possible_moves:
                        self.possible_moves.append((targetSquare, targetSquare, currentSquare[2]))

    
    def player_make_move(self, x = None, y = None, x_index = None, y_index = None, square = None, ai = False):
        if square == None and ai == False:
            square = self.get_square(x, y)
        if x_index != None and y_index != None:
            square = self.get_square_by_index(x_index, y_index)
        if square:
            if self.selected_square != None:
                found = None
                for s in self.possible_moves:
                    if square == s[0]:
                        found = s
                        break
                if found:
                    if found[0] != found[1]:
                        jumped = found[1]
                        
                        if ai:
                            jumped = self.get_square(found[1].top_left_x, found[1].top_left_y)
                        
                        self.just_jumped = True
                        
                        if ai:
                            if jumped.piece.king:
                                self.captured_opponent_kings_count += 1
                            else:
                                self.captured_opponent_pieces_count += 1
                        
                        jumped.piece = None
                    
                    self.selected_square.piece.x = square.top_left_x + settings.SQUARE_SIZE / 2
                    self.selected_square.piece.y = square.top_left_y + settings.SQUARE_SIZE / 2
                    square.piece = self.selected_square.piece
                    
                    # ai fix for reference issue; perhaps fix later
                    if ai:
                        temp = self.get_square(self.selected_square.top_left_x, self.selected_square.top_left_y)
                        temp.piece = None
                        temp.highlight = False
                    
                    self.selected_square.piece = None
                    self.selected_square.highlight = False
                    self.selected_square = None
                    
                    # make king if in end row
                    if self.current_player == settings.TAN and square.y == 0:
                        square.piece.king = True
                        self.created_kings_count += 1
                    elif self.current_player == settings.RED and square.y == settings.SIZE - 1:
                        square.piece.king = True
                        self.created_kings_count += 1
                    
                    # reset possible moves
                    for possible_move in self.possible_moves:
                        possible_move[0].highlight = False
                    self.possible_moves = []
                    
                    if self.just_jumped:
                        self.calculate_possible_moves(currentSquare=(square, square, square))
                        if len(self.possible_moves) > 0:
                            self.possible_moves = []
                            self.select_square(square.top_left_x + settings.SQUARE_SIZE / 2, square.top_left_y + settings.SQUARE_SIZE / 2)
                            
                            if ai:
                                self.player_make_move(square = self.possible_moves[0][0], ai = True)
                                
                            return
                        else:
                            self.just_jumped = False
                    
                    # change player
                    self.current_player = settings.RED if self.current_player == settings.TAN else settings.TAN     
                    
    def ai_make_move(self, initial_x_coord, initial_y_coord, target_x_index, target_y_index, force_moves = []):
        self.selected_square = None
        
        if force_moves != []:
            self.select_square(x=initial_x_coord, y=initial_y_coord, force_moves=force_moves)
        else:
            self.select_square(x=initial_x_coord, y=initial_y_coord)
        target = self.get_square_by_index(target_x_index, target_y_index)
        
        if target and self.selected_square:
            found = None
            for possible_move in self.possible_moves:
                if target == possible_move[0]:
                    found = possible_move
                    break
            if found:
                if found[0] != found[1]:
                    jumped = self.get_square_by_index(found[1].x, found[1].y)
                    if jumped:
                        self.just_jumped = True
                        if jumped.piece.king:
                            self.captured_opponent_kings_count += 1
                        else: 
                            self.captured_opponent_pieces_count += 1
                        jumped.piece = None
                
                target.piece = self.selected_square.piece
                target.piece.x = target.top_left_x + settings.SQUARE_SIZE / 2
                target.piece.y = target.top_left_y + settings.SQUARE_SIZE / 2
                self.selected_square.piece = None
                self.selected_square.highlight = False
                
                if target.piece.color == settings.TAN and target.y == 0:
                    target.piece.king = True
                    self.created_kings_count += 1
                elif target.piece.color == settings.RED and target.y == settings.SIZE - 1:
                    target.piece.king = True
                    self.created_kings_count += 1
                    
                for possible_move in self.possible_moves:
                    possible_move[0].highlight = False
                self.possible_moves = []
                
                if self.just_jumped:
                    self.calculate_possible_moves(currentSquare=(target, target, target))
                    if len(self.possible_moves) > 0:
                        self.ai_make_move(target.top_left_x + settings.SQUARE_SIZE / 2, target.top_left_y + settings.SQUARE_SIZE / 2,
                                          self.possible_moves[0][0].x, self.possible_moves[0][0].y)
                        return
                    else:
                        self.just_jumped = False
                
                self.current_player = settings.RED if self.current_player == settings.TAN else settings.TAN                    
    
    def get_square(self, x, y):
        x = int(x // settings.SQUARE_SIZE)
        y = int(y // settings.SQUARE_SIZE)
        return self.squares[x + y * settings.SIZE]
    
    def get_square_by_index(self, x, y) -> Square | None:
        if x < 0 or y < 0 or x >= settings.SIZE or y >= settings.SIZE:
            return None
        return self.squares[x + y * settings.SIZE]
    