import pygame
import settings

from square import Square
from piece import Piece
class Board:
    def __init__(self) -> None:
        self.squares = []
        for i in range(settings.SIZE):
            for j in range(settings.SIZE):
                if (i + j) % 2 == 0:
                    color = settings.WHITE
                else:
                    color = settings.BLACK
                
                square_x = j * settings.WIDTH / settings.SIZE
                square_y = i * settings.WIDTH / settings.SIZE
                
                piece_x = square_x + settings.SQUARE_SIZE / 2
                piece_y = square_y + settings.SQUARE_SIZE / 2
                
                piece = None
                if i < 3 and (i + j) % 2 == 1:
                    piece = Piece(piece_x, piece_y, settings.RED, settings.PIECE_RADIUS)
                elif i > 4 and (i + j) % 2 == 1:
                    piece = Piece(piece_x, piece_y, settings.TAN, settings.PIECE_RADIUS)
                
                self.squares.append(Square(square_x, square_y, color, piece))
    
    def draw(self, window):
        for square in self.squares:
            square.draw(window)
            
    def highlight_square(self, x, y):
        square = self.get_square(x, y)
        if square.has_piece():
            for s in self.squares:
                s.highlight = False
            square.highlight = not square.highlight
            return square
        return None
        
    def get_square(self, x, y):
        x = int(x // settings.SQUARE_SIZE)
        y = int(y // settings.SQUARE_SIZE)
        return self.squares[x + y * settings.SIZE]