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
            if square.has_piece():
                square.highlight = True
                self.selected_square = square
                self.calculate_possible_moves(currentSquare=(self.selected_square, list()))
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
    def calculate_possible_moves(self, currentSquare: Tuple[Square, List[Square]] , justJumped = False):
        if not justJumped:
            if targetSquare := self.can_move_up_left(currentSquare):
                if targetSquare not in self.possible_moves:
                    self.possible_moves.append(targetSquare)
            if targetSquare := self.can_move_up_right(currentSquare):
                if targetSquare not in self.possible_moves:
                    self.possible_moves.append(targetSquare)
        if targetSquare := self.can_jump_up_left(currentSquare):
            if targetSquare not in self.possible_moves:
                self.possible_moves.append(targetSquare)
                self.calculate_possible_moves(targetSquare, True)
        if targetSquare := self.can_jump_up_right(currentSquare):
            if targetSquare not in self.possible_moves:
                self.possible_moves.append(targetSquare)
                self.calculate_possible_moves(targetSquare, True)
        
    def can_move_up_left(self, currentSquare: Tuple[Square, List[Square]]) -> Tuple[Square, List[Square]] | None:
        targetSquare = self.get_square_by_index(currentSquare[0].x - 1, currentSquare[0].y - 1)
        if targetSquare:
            if targetSquare.has_piece():
                return None
            else:
                return (targetSquare, currentSquare[1])
        return None
    
    def can_move_up_right(self, currentSquare: Tuple[Square, List[Square]]):
        targetSquare = self.get_square_by_index(currentSquare[0].x + 1, currentSquare[0].y - 1)
        if targetSquare:
            if targetSquare.has_piece():
                return None
            else:
                return (targetSquare, currentSquare[1])
        return None
    
    def can_jump_up_left(self, currentSquare: Tuple[Square, List[Square]]) -> Tuple[Square, List[Square]] | None:
        targetSquare = self.get_square_by_index(currentSquare[0].x - 2, currentSquare[0].y - 2)
        jumpedSquare = self.get_square_by_index(currentSquare[0].x - 1, currentSquare[0].y - 1)
        if targetSquare != None and jumpedSquare != None:
            if targetSquare.has_piece() or not jumpedSquare.has_piece():
                return None
            else:
                currentSquare[1].append(jumpedSquare)
                return (targetSquare, currentSquare[1]) 
        return None
    
    def can_jump_up_right(self, currentSquare: Tuple[Square, List[Square]]) -> Tuple[Square, List[Square]] | None:
        targetSquare = self.get_square_by_index(currentSquare[0].x + 2, currentSquare[0].y - 2)
        jumpedSquare = self.get_square_by_index(currentSquare[0].x + 1, currentSquare[0].y - 1)
        if targetSquare and jumpedSquare:
            if targetSquare.has_piece() or not jumpedSquare.has_piece():
                return None
            else:
                currentSquare[1].append(jumpedSquare)
                return (targetSquare, currentSquare[1])
        return None
    
    def make_move(self, x, y):
        square = self.get_square(x, y)
        for s in self.possible_moves:
            print(s[0])
        if self.selected_square != None:
            found = None
            for s in self.possible_moves:
                if square == s[0]:
                    found = s
                    break
            if found:
                self.selected_square.piece.x = square.top_left_x + settings.SQUARE_SIZE / 2
                self.selected_square.piece.y = square.top_left_y + settings.SQUARE_SIZE / 2
                square.piece = self.selected_square.piece
                self.selected_square.piece = None
                self.selected_square.highlight = False
                self.selected_square = None
                
                # remove jumped pieces
                for jumpedSquare in found[1]:
                    jumpedSquare.piece = None
                
                # reset possible moves
                for square in self.possible_moves:
                    square[0].highlight = False
                self.possible_moves = []
        
    def get_square(self, x, y):
        x = int(x // settings.SQUARE_SIZE)
        y = int(y // settings.SQUARE_SIZE)
        return self.squares[x + y * settings.SIZE]
    
    def get_square_by_index(self, x, y) -> Square | None:
        if x < 0 or y < 0 or x >= settings.SIZE or y >= settings.SIZE:
            return None
        return self.squares[x + y * settings.SIZE]
    