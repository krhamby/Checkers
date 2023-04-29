import pygame

class Piece:
    def __init__(self, x, y, color, radius, king = False) -> None:
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.king = king
        
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Piece):
            return self.x == __value.x and self.y == __value.y and self.color == __value.color and self.radius == __value.radius
        return False
        
    def deep_copy(self):
        return Piece(self.x, self.y, self.color, self.radius, self.king)
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)
        
        if self.king:
            img = pygame.image.load("crown.png")
            img = pygame.transform.scale(img, (self.radius * 2, self.radius * 2))
            img.set_colorkey((255, 255, 255))
            surface.blit(img, (self.x - self.radius, self.y - self.radius))
            