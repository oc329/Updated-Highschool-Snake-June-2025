from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List
from resource_modules.enums import Layout

if TYPE_CHECKING:
    from ui.components_of_menu import AbstractMenuBox

class BaseAxisLayoutManager(ABC):
    """
    Base layout manager class for handling vertical/horizontal axis logic.
    """

    def __init__(self, layout: Layout):
        """
        (Layout) layout: The layout (Vertical or Horizontal) determines how the boxes are positioned
        """
        assert layout in (Layout.VERTICAL, Layout.HORIZONTAL), f"Invalid layout: {layout}. Must be either Vertical or Horizontal."
        self.layout = layout

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
            return sum(box.get_height() for box in boxes)
        else:
            return sum(box.get_width() for box in boxes)

    @abstractmethod
    def get_spacing(self, boxes: List['AbstractMenuBox']) -> int:
        pass

    @abstractmethod
    def ensure_boxes_can_fit(self, boxes: List['AbstractMenuBox']) -> None:
        pass

    @abstractmethod
    def position_boxes(self, boxes: List['AbstractMenuBox']) -> None:
        pass

class AbstractTwoPointLayoutManager(BaseAxisLayoutManager):
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
