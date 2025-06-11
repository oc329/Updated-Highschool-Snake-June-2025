from enum import Enum

class Direction(Enum):
    """
    Enum that holds the snake tuple e.g (1, 0) of the row and column direction.
    """
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class PageName(Enum):
    MAIN_MENU = "Main Menu"
    SNAKE_SKIN_SETTINGS = "Snake Skins"
    SCREEN_SETTINGS = "Screen Settings"

print()