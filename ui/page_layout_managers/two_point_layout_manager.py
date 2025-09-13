from ui.page_layout_managers.abstract_layout_manager import AbstractTwoPointLayoutManager
from resource_modules.enums import Layout, TextSurfacePosAnchor
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.components_of_menu import AbstractMenuBox

class TwoPointLayoutManager(AbstractTwoPointLayoutManager):
    """
    Two points should share share at least one axis (at least x or y should be the same).
    Raises a ValueError if they don't
    """
    def __init__(self, point1: tuple[int, int], point2: tuple[int, int], box_pos_anchor = TextSurfacePosAnchor.MIDDLE):
        self.ensure_points_are_valid(point1, point2) 
        super().__init__(self.get_layout(), point1, point2, box_pos_anchor)
        
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
   