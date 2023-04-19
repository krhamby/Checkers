import pygame
import settings

class Square:
    def __init__(self, top_left_x, top_left_y, color, piece, highlight = False) -> None:
        self.x = top_left_x
        self.y = top_left_y
        self.color = color
        self.piece = piece
        self.highlight = highlight
    
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, settings.SQUARE_SIZE, settings.SQUARE_SIZE))
        if self.piece != None:
            self.piece.draw(window)
        if self.highlight:
            pygame.draw.rect(window, settings.RED, (self.x, self.y, settings.SQUARE_SIZE, settings.SQUARE_SIZE), 5)
            
    def has_piece(self):
        return self.piece != None