import pygame

class Piece:
    def __init__(self, x, y, color, radius) -> None:
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.king = False
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)
        
        if self.king:
            img = pygame.image.load("crown.png")
            img = pygame.transform.scale(img, (self.radius * 2, self.radius * 2))
            img.set_colorkey((255, 255, 255))
            surface.blit(img, (self.x - self.radius, self.y - self.radius))