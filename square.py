import pygame
import settings

class Square:
    def __init__(self, top_left_x, top_left_y, x, y, color, piece, highlight = False) -> None:
        self.top_left_x = top_left_x
        self.top_left_y = top_left_y
        self.x = x 
        self.y = y
        self.color = color
        self.piece = piece
        self.highlight = highlight
        
    def __str__(self) -> str:
        return f"Square: ({self.x}, {self.y})"

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Square):
            return self.x == o.x and self.y == o.y
        return False
    
    def deep_copy(self):
        return Square(self.top_left_x, self.top_left_y, self.x, self.y, self.color, self.piece.deep_copy() if self.piece != None else None, self.highlight)
    
    def copy(self):
        return Square(self.top_left_x, self.top_left_y, self.x, self.y, self.color, self.piece, self.highlight)
    
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.top_left_x, self.top_left_y, settings.SQUARE_SIZE, settings.SQUARE_SIZE))
        if self.piece != None:
            self.piece.draw(window)
        if self.highlight:
            pygame.draw.rect(window, settings.RED, (self.top_left_x, self.top_left_y, settings.SQUARE_SIZE, settings.SQUARE_SIZE), 5)
            
    def has_piece(self):
        return self.piece != None
    
    def is_highlighted(self):
        return self.highlight