from enum import Enum, auto
from abc import abstractmethod

class Direction(Enum):
    """
    Enum that holds the snake tuple e.g (1, 0) of the row and column direction.
    """
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class MenuSnakeTeleportationType(Enum):
    """
    Enum for the different teleportation states for the menu snake (instant, wrapping, etc.)
    """
    INSTANT = auto()
    WRAPPING = auto()
    
class PageName(Enum):
    MAIN_MENU = 'Main Menu'
    TRANSITION_TO_SETTINGS = "Settings" 
    SNAKE_SKIN_SETTINGS = 'Snake Skins'
    SCREEN_SETTINGS = 'Screen Settings'

class LayoutMangerTypes(Enum):
    """
    Enum for the different layout manager types.
    """
    ONE_POINT = auto()
    TWO_POINT = auto()
    VERTICAL_SECTOR = auto()
    HORIZONTAL_SECTOR = auto()

class Layout(Enum):
    HORIZONTAL = auto()
    VERTICAL = auto()

class TextSurfacePosAnchor(Enum):
    START = 'start'
    MIDDLE = 'middle'
    END = 'end'


class AbstractSectorPosAnchor(Enum):
    """
    Describes where to position the Menu boxes
    within the sector 
    """
    def calculate_axis_value(self, top_left: tuple[int, int], bottom_right: tuple[int, int]) -> int:
        raise NotImplementedError("Must be implemented by subclasses")
        

class HorizontalSectorPosAnchor(AbstractSectorPosAnchor): 
    TOP = auto()
    MIDDLE = auto()
    BOTTOM = auto()

    def calculate_axis_value(self, top_left: tuple[int, int], bottom_right: tuple[int, int]) -> int:
        top_y, bottom_y = top_left[1], bottom_right[1]
        match self:
            case HorizontalSectorPosAnchor.TOP:
                return top_y
            case HorizontalSectorPosAnchor.MIDDLE:
                return (top_y + bottom_y) // 2
            case HorizontalSectorPosAnchor.BOTTOM:
                return bottom_y     

class VerticalSectorPosAnchor(AbstractSectorPosAnchor): 
    LEFT = auto()
    MIDDLE = auto()
    RIGHT = auto()

    def calculate_axis_value(self, top_left: tuple[int, int], bottom_right: tuple[int, int]) -> int:
        left_x, right_x = top_left[0], bottom_right[0]
        match self:
            case VerticalSectorPosAnchor.LEFT:
                return left_x
            case VerticalSectorPosAnchor.MIDDLE:
                return (left_x + right_x) // 2
            case VerticalSectorPosAnchor.RIGHT:
                return right_x


