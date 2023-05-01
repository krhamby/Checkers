import pygame

import settings
from board import Board

class Footer:
    def __init__(self):
        self.font = pygame.font.SysFont("comicsans", 16)
    
    def draw(self, window, current_player):
        """
        Draws a footer displaying the current player
        """
        pygame.draw.rect(window, settings.BLACK, (0, settings.WIDTH, settings.WIDTH, int(settings.FOOTER_HEIGHT)))
        player = "Red" if current_player == settings.RED else "Tan"
        text = self.font.render(f"Current Player: {player}", True, settings.WHITE)
        text_rect = text.get_rect()
        text_rect.center = (int(settings.WIDTH / 2), int(settings.WIDTH + settings.FOOTER_HEIGHT / 2))
        window.blit(text, text_rect)
        
    def draw_winner(self, window, winner):
        """ 
        Draws a footer displaying the winner
        """
        pygame.draw.rect(window, settings.BLACK, (0, settings.WIDTH, settings.WIDTH, int(settings.FOOTER_HEIGHT)))
        text = self.font.render(f"Winner: {winner}", True, settings.WHITE)
        text_rect = text.get_rect()
        text_rect.center = (int(settings.WIDTH / 2), int(settings.WIDTH + settings.FOOTER_HEIGHT / 2))
        window.blit(text, text_rect)
        
    def draw_draw(self, window):
        """
        Draws a footer that says "Draw"
        """
        pygame.draw.rect(window, settings.BLACK, (0, settings.WIDTH, settings.WIDTH, int(settings.FOOTER_HEIGHT)))
        text = self.font.render(f"Draw", True, settings.WHITE)
        text_rect = text.get_rect()
        text_rect.center = (int(settings.WIDTH / 2), int(settings.WIDTH + settings.FOOTER_HEIGHT / 2))
        window.blit(text, text_rect)