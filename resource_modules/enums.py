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

# class BoxPosAnchor(TextSurfacePosAnchor):
#     """
#     Inherits from TextSurfacePosAnchor. Has functioanlity to calcualte box pos based on given point
#     """
#     def calculate_box_pos(self, point: tuple[int, int], text_width: int) -> tuple[int, int]:
#         """
#         Calculates the top-left position of the box based on the anchor pointand the given point.

#         Parameters:
#             - point: The reference point (x, y)
#             - text_width (int): The width of the menu box's text 
#             - box_height: The height of the box

#         Returns:
#             - A tuple representing the top-left position (x, y) of the box.
#         """
#         match self:
#             case BoxPosAnchor.START:
#                 return (point[0], point[1])
#             case BoxPosAnchor.MIDDLE:
#                 return (point[0] - box_width // 2, point[1])
#             case BoxPosAnchor.END:
#                 return (point[0] + box_width, point[1])
#             case _:
#                 raise ValueError(f"Invalid BoxPosAnchor: {self}")

    
class AbstractSectorPosAnchor(Enum):
    """
    Describes where to position the Menu boxes
    within the sector 
    """
    def calculate_axis_value(self, top_left: tuple[int, int], bottom_right: tuple[int, int]) -> int:
        raise NotImplementedError
        

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


class OnePointLayout(Enum): 
    HORIZONTAL = auto()
    VERTICAL = auto()

