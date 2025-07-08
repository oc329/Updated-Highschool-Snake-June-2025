from enum import Enum, auto

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

class SectorType(Enum):
    VERTICAL = 'vertical'
    HORIZONTAL = 'horizontal'

class TextSurfacePosAnchor(Enum):
    START = 'start'
    MIDDLE = 'middle'
    END = 'end'

class AbstractSectorPosAnchor(Enum):
    """
    Describes where to position the Menu boxes
    within the sector 
    """
    pass

class HorizontalSectorPosAnchor(AbstractSectorPosAnchor): 
    TOP = 'top'
    MIDDLE = 'middle' 
    BOTTOM = 'bottom'

class VerticalSectorPosAnchor(AbstractSectorPosAnchor): 
    LEFT = 'left'
    MIDDLE = 'middle' 
    RIGHT = 'right'

