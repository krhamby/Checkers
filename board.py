import pygame
import settings
from typing import List, Tuple

from square import Square
from piece import Piece
class Board:
    def __init__(self) -> None:
        self.squares = []
        self.selected_square = None
        self.possible_moves = []
        
        self.current_player = settings.TAN
        self.just_jumped = False
        
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
    
    def draw(self, window):
        for square in self.squares:
            square.draw(window)

    def select_square(self, x, y):
        square = self.get_square(x, y)
        if self.selected_square == None:
            if square.has_piece() and square.piece.color == self.current_player:
                square.highlight = True
                self.selected_square = square
                self.calculate_possible_moves(currentSquare=(self.selected_square, self.selected_square))
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
    
    # the following five methods could definitely be consolidated
    def calculate_possible_moves(self, currentSquare: Tuple[Square, Square]):
        if self.current_player == settings.TAN:
            self.add_moves_up(currentSquare)
        else:
            self.add_moves_down(currentSquare)
    
    
    def add_moves_up(self, currentSquare: Tuple[Square, Square]):
        if not self.just_jumped:
            for i in range(-1, 2, 2):
                targetSquare = self.get_square_by_index(currentSquare[0].x + i, currentSquare[0].y - 1)
                if targetSquare:
                    if not targetSquare.has_piece() and targetSquare not in self.possible_moves:
                        self.possible_moves.append((targetSquare, targetSquare))
        
        for i in range(-2, 3, 4):
            targetSquare = self.get_square_by_index(currentSquare[0].x + i, currentSquare[0].y - 2)
            jumpedSquare = self.get_square_by_index(currentSquare[0].x + i // 2, currentSquare[0].y - 1)
            if targetSquare and jumpedSquare:
                if (jumpedSquare.has_piece() and not targetSquare.has_piece() 
                    and jumpedSquare.piece.color != self.current_player and targetSquare not in self.possible_moves):
                    self.possible_moves.append((targetSquare, jumpedSquare))
                    
    def add_moves_down(self, currentSquare: Tuple[Square, Square]):
        if not self.just_jumped:
            for i in range(-1, 2, 2):
                targetSquare = self.get_square_by_index(currentSquare[0].x + i, currentSquare[0].y + 1)
                if targetSquare:
                    if not targetSquare.has_piece() and targetSquare not in self.possible_moves:
                        self.possible_moves.append((targetSquare, targetSquare))

        for i in range(-2, 3, 4):
            targetSquare = self.get_square_by_index(currentSquare[0].x + i, currentSquare[0].y + 2)
            jumpedSquare = self.get_square_by_index(currentSquare[0].x + i // 2, currentSquare[0].y + 1)
            if targetSquare and jumpedSquare:
                if (jumpedSquare.has_piece() and not targetSquare.has_piece() 
                    and jumpedSquare.piece.color != self.current_player and targetSquare not in self.possible_moves):
                    self.possible_moves.append((targetSquare, jumpedSquare))
            
    
    def make_move(self, x, y):
        square = self.get_square(x, y)
        if self.selected_square != None:
            found = None
            for s in self.possible_moves:
                if square == s[0]:
                    found = s
                    break
            if found:
                if found[0] != found[1]:
                    self.just_jumped = True
                    found[1].piece = None
                
                self.selected_square.piece.x = square.top_left_x + settings.SQUARE_SIZE / 2
                self.selected_square.piece.y = square.top_left_y + settings.SQUARE_SIZE / 2
                square.piece = self.selected_square.piece
                self.selected_square.piece = None
                self.selected_square.highlight = False
                self.selected_square = None
                
                # reset possible moves
                for possible_move in self.possible_moves:
                    possible_move[0].highlight = False
                self.possible_moves = []
                
                if self.just_jumped:
                    self.calculate_possible_moves(currentSquare=(square, square))
                    if len(self.possible_moves) > 0:
                        self.possible_moves = []
                        self.select_square(square.top_left_x + settings.SQUARE_SIZE / 2, square.top_left_y + settings.SQUARE_SIZE / 2)
                        return
                    else:
                        self.just_jumped = False
                
                # change player
                self.current_player = settings.RED if self.current_player == settings.TAN else settings.TAN
    
    def get_square(self, x, y):
        x = int(x // settings.SQUARE_SIZE)
        y = int(y // settings.SQUARE_SIZE)
        return self.squares[x + y * settings.SIZE]
    
    def get_square_by_index(self, x, y) -> Square | None:
        if x < 0 or y < 0 or x >= settings.SIZE or y >= settings.SIZE:
            return None
        return self.squares[x + y * settings.SIZE]
    