from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from resource_modules.enums import Layout

if TYPE_CHECKING:
    from ui.components_of_menu import AbstractMenuBox 

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List
from resource_modules.enums import Layout, TextSurfacePosAnchor

if TYPE_CHECKING:
    from ui.components_of_menu import AbstractMenuBox


    
class AbstractLayoutManager(ABC):
    def __init__(self, layout: Layout, box_pos_anchor = TextSurfacePosAnchor.MIDDLE):
        """
        (Layout) layout: The layout (Vertical or Horizontal) determines how the boxes are positioned
        """
        self.layout = layout
        self.box_pos_anchor = box_pos_anchor
        
    @staticmethod
    def ensure_there_are_boxes(boxes: list):
        """
        Raises an error if thee menu boxes list is empty. 
        
        Parameters: 
            - (list) boxes: The list of menu boxes layout manager
        """
        if not boxes:
            raise IndexError("Page has no menu boxes; cannot select a box.")
        

    def get_combined_box_width(boxes: list['AbstractMenuBox']):
        """
        Adds up the width of each box and 
        returns the combined width of all the boxes in the given boxes list.

        Parameters: 
            - (list) boxes: List of all the menu boxes layout manager
        """
        return sum(box.get_width() for box in boxes)
    
    def get_combined_box_height(boxes: list['AbstractMenuBox']):
        """
        Returns the combined height of all the boxes.
        Parameters: 
            - (list) boxes: List of all the menu boxes in this layout manager
        """
        return sum(box.get_height() for box in boxes)
    
    def is_vertical(self) -> bool:
        return self.layout == Layout.VERTICAL
    
    def is_horizontal(self) -> bool:
        return self.layout == Layout.HORIZONTAL
    
    def get_combined_box_size(self, boxes: List['AbstractMenuBox']) -> int:
        """
        Returns the combined size of all the boxes along the axis.
        (height for vertical, width for horizontal)
        """
        if self.is_vertical():
            return self.get_combined_box_height(boxes)
        elif self.is_horizontal():
            return self.get_combined_box_width(boxes)
        
    @abstractmethod
    def position_boxes(self, boxes: list['AbstractMenuBox']):
        """
        Method for positioning menu boxes based on this layout manager.
        """
        pass
    
    @abstractmethod
    def ensure_boxes_can_fit(self, boxes: list['AbstractMenuBox']):
        """
        Ensures the boxes can fit in the layout manager. 
        If there isn't enough space, it raises an error
        """
        pass

class AbstractTwoPointLayoutManager(AbstractLayoutManager):
    """
    Base layout manager class for handling vertical/horizontal axis logic.
    """
    def __init__(self, layout: Layout, point1: tuple[int, int], point2: tuple[int, int], box_pos_anchor= TextSurfacePosAnchor.MIDDLE):
        """
        Two point layout managers position the boxes between two points. 
        The points should share at least one axis (at least x or y should be the same).

        Parameters: 
            - (Layout) layout: The layout (Vertical or Horizontal) determines how the boxes are positioned
            - (tuple[int, int]) point1: The first point to position the boxes between
            - (tuple[int, int]) point2: The second point to position the boxes between
        """
        assert layout in (Layout.VERTICAL, Layout.HORIZONTAL), f"Invalid layout: {layout}. Must be either Vertical or Horizontal"
        self.point1 = point1
        self.point2 = point2
        super().__init__(layout, box_pos_anchor)

    def get_spacing(self, boxes): 
        if self.is_vertical():
            diff_btw_points = abs(self.point1[1] - self.point2[1])
            return abs(self.point1[1] - self.point2[1]) // len(boxes)
        elif self.is_horizontal():
            diff_btw_points = abs(self.point1[0] - self.point2[0])
            return abs(self.point1[0] - self.point2[0]) // len(boxes)
        return diff_btw_points // len(boxes)
    
    def ensure_boxes_can_fit_btw_two_points(self, boxes: list, layout: Layout,
                                        point1: tuple[int, int], point2: tuple[int, int]):
        """
        Raises a Value Error if the boxes don't fit between the two points.
        Is called in subclasses to help with their ensure_boxes_can_fit methods.

        Parameters: 
            - (list) boxes: List of all the menu boxes in this layout manager
            - (Layout) layout: The Vertical or Horizontal Layout Enum of the layout manager 
            - (tuple[int, int]) point1: The first point in the sector
            - (tuple[int, int]) point2: The second point in the sector
        """
        if layout is Layout.VERTICAL: 
            combined_box_height = self.get_combined_box_height(boxes)
            sector_height = abs(point1[1] - point2[1])

            if combined_box_height > sector_height:
                raise ValueError(f"Boxes do not fit vertically in sector. "
                                f"Sector height: {sector_height}, required: {combined_box_height}")
            
        elif layout is Layout.HORIZONTAL: 
            min_sector_width = self.get_combined_box_width(boxes)
            sector_width = abs(point1[0] - point2[0])

        if min_sector_width > sector_width:
            raise ValueError(f"Boxes do not fit horizontally in sector. "
                            f"Sector width: {sector_width}, required: {min_sector_width}")
    
    def ensure_boxes_can_fit(self, boxes: List['AbstractMenuBox']) -> None:
        self.ensure_boxes_can_fit_btw_two_points(boxes, self.layout, self.point1, self.point2)

    @staticmethod
    def ensure_points_share_one_axis(point1: tuple[int, int], point2: tuple[int, int]):
        """
        Raises ValueError if the 2 points don't share a common x or y.
        """
        x_is_same = point1[0] == point2[0]
        y_is_same = point1[1] == point2[1]

        if not (x_is_same or y_is_same):
            raise ValueError("Points should share a common axis. x or y should be the same"
                             f"point1 = {point1} point2 = {point2}")
        
    def ensure_points_are_valid(self):
        """
        Ensures the points are valid for this layout manager.
        Specifically, it checks that both points share the same axis don't have the same coordinates.
        Raises ValueError if they are don't.
        """
        if self.point1 == self.point2:
            raise ValueError("Points cannot be the same. point1 = point2 = {self.point1}")
        self.ensure_points_share_one_axis(self.point1, self.point2)


    def position_boxes_vertical(self, boxes: list['AbstractMenuBox']):
        """
        Positions the page's menu boxes for a vertical sector.
        Raises an error if the combined menu boxes' height is greater than the sector height.
        """
        self.ensure_there_are_boxes(boxes)
        self.ensure_boxes_can_fit(boxes)
        self.ensure_points_are_valid()

        top_y = min(self.point1[1], self.point2[1])
        spacing = self.get_spacing(boxes)
        menu_box_x = self.point1[0]
        for box_i, box in enumerate(boxes):
            pos = (menu_box_x, top_y + spacing * box_i)
            box.change_pos_anchor(self.box_pos_anchor)
            box.change_pos(pos)
    
    def position_boxes_horizontal(self, boxes: list['AbstractMenuBox']):
        """
        Positions the page's menu boxes for a horizontal sector.
        Raises an error if the combined menu boxes' width is greater than the sector width.
        """
        self.ensure_there_are_boxes(boxes)
        self.ensure_boxes_can_fit(boxes)
        self.ensure_points_are_valid()
        
        left_x = min(self.point1[0], self.point2[0])
        spacing = self.get_spacing(boxes)
        menu_box_y = self.point1[1]
        for box_i, box in enumerate(boxes):
            pos = (left_x + spacing * box_i, menu_box_y)
            box.change_pos_anchor(self.box_pos_anchor)
            box.change_pos(pos)

    def ensure_points_and_boxes_are_valid(self, boxes: list['AbstractMenuBox']):
        """
        Ensures the points and boxes are valid for positioning.
        Raises an error if they are not.
        """
        self.ensure_there_are_boxes(boxes)
        self.ensure_boxes_can_fit(boxes)
        self.ensure_points_are_valid()

    def position_boxes(self, boxes: list['AbstractMenuBox']):
        if self.layout == Layout.VERTICAL:
            self.position_boxes_vertical(boxes)
        elif self.layout == Layout.HORIZONTAL:
            self.position_boxes_horizontal(boxes)
