import pygame

class Piece:
    def __init__(self, x, y, color, radius) -> None:
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)