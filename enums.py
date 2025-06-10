from enum import Enum

class Direction(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

class PageName(Enum):
    MAIN_MENU = "Main Menu"
    SNAKE_SKIN_SETTINGS = "Snake Skins"
    SCREEN_SETTINGS = "Screen Settings"