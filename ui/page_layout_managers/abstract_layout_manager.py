from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from resource_modules.enums import Layout

if TYPE_CHECKING:
    from ui.components_of_menu import AbstractMenuBox 

class AbstractLayoutManager(ABC):
    def __init__(self, layout: Layout):
        """
        (Layout) layout: The layout (Vertical or Horizontal) determines how the boxes are positioned
        """
        self.layout = layout

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
        total_height = sum(box.get_height() for box in boxes)
        return total_height 
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
    def ensure_boxes_can_fit_btw_points(self, boxes: list, layout: Layout,
                                        point1: tuple[int, int], point2: tuple[int, int]):
        """
        Raises a Value Error if the boxes don't fit between the two points

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

class layoutManagerFactory: 
    def create_layout_manager(self, OnePointLayout):
        pass
