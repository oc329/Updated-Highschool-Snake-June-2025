from ui.page_layout_managers.abstract_layout_manager import AbstractTwoPointLayoutManager
from resource_modules.enums import Layout
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.components_of_menu import AbstractMenuBox

class TwoPointLayoutManager(AbstractTwoPointLayoutManager):
    """
    Two points should share share at least one axis (at least x or y should be the same).
    Raises a ValueError if they don't
    """
    def __init__(self, point1: tuple[int, int], point2: tuple[int, int]):
        self.ensure_points_are_valid(point1, point2) 
        self.point1 = point1
        self.point2 = point2
        super().__init__(self.get_layout())
        
    def get_layout(self) -> Layout:
        """
        Returns a horizontal or vertical layout Enum 
        depending on how the points are positioned
        """
        if self.point1[0] == self.point2[0]:
            return Layout.VERTICAL
        elif self.point[1] == self.point2[1]:
            return Layout.HORIZONTAL
        else: 
            raise ValueError("Points should share a common axis. x or y should be the same"
                             f"point1 = {self.point1} point2 = {self.point2}")                        
    
    def ensure_points_are_valid(self):
        """
        Ensures the points are valid for this layout manager.
        Specifically, it checks that both points share the same axis and aren't the same.
        Raises ValueError if they are not.
        """
        if self.point1 == self.point2:
            raise ValueError("Points cannot be the same. point1 = point2 = {self.point1}")
        self.ensure_points_share_one_axis(self.point1, self.point2)

    @staticmethod
    def ensure_points_share_one_axis(point1: tuple[int, int], point2: tuple[int, int]):
        """
        Raises ValueError if the points don't share a common x or y.
        """
        x_is_same = point1[0] == point2[0]
        y_is_same = point1[1] == point2[1]

        if not (x_is_same and y_is_same):
            raise ValueError("Points should share a common axis. x or y should be the same"
                             f"point1 = {point1} point2 = {point2}")
        
    def position_boxes(self, boxes: list['AbstractMenuBox']):
        self.ensure_there_are_boxes()
        self.ensure_boxes_can_fit(boxes)

    def ensure_boxes_can_fit(self, boxes: list['AbstractMenuBox']):
        """
        Ensures the boxes can fit in the layout manager. 
        If there isn't enough space, it raises an error
        """
        if self.layout is Layout.VERTICAL:
            pass  
        elif self.layout is Layout.HORIZONTAL:
            pass

