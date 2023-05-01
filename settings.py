from enum import Enum

WIDTH = 720
FOOTER_HEIGHT = WIDTH * 0.05

# game mode
class GameMode(Enum):
    SINGLE_PLAYER_AI = 1
    TWO_PLAYER_AI = 2
    TWO_PLAYER = 3

GAME_MODE = GameMode.TWO_PLAYER_AI

# ply
PLY = 8

# board size
SIZE = 8

# square size
SQUARE_SIZE = int(WIDTH / SIZE)

# piece radius
PIECE_RADIUS = SQUARE_SIZE / 2 * 0.8

# colors for squares
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# colors for pieces
RED = (255, 0, 0) # also used for highlighting
TAN = (210, 180, 140)


