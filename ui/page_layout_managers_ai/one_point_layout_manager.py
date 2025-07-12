from typing import Tuple, List, TYPE_CHECKING
from ui.page_layout_managers_ai.base_axis_layout_manager import BaseAxisLayoutManager
from resource_modules.enums import Layout, TextSurfacePosAnchor

if TYPE_CHECKING:
    from ui.components_of_menu import AbstractMenuBox

class OnePointLayoutManager(BaseAxisLayoutManager):
    """
    Layout manager that centers the menu boxes around a point.
    """

    def __init__(
        self,
        point_to_center_on: Tuple[int, int],
        layout: Layout,
        box_pos_anchor: TextSurfacePosAnchor = TextSurfacePosAnchor.MIDDLE,
    ):
        """
        Parameters:
            - (tuple[int, int]) point_to_center_on: The point to center the boxes around
            - (Layout) layout: Vertical or Horizontal
            - (TextSurfacePosAnchor) box_pos_anchor: The anchor for each box's position
        """
        super().__init__(layout)
        self.point_to_center_on = point_to_center_on
        self.box_pos_anchor = box_pos_anchor

    def get_spacing(self, boxes: List['AbstractMenuBox']) -> int:
        # Centered layout, so space is not a concern for spacing,
        # but you could customize this as needed.
        return 0

    def ensure_boxes_can_fit(self, boxes: List['AbstractMenuBox']) -> None:
        # For centering, ensure boxes fit around the central point
        if self.is_vertical():
            half_of_combined_height = self.get_combined_box_size(boxes) // 2
            top_of_all_boxes_y = self.point_to_center_on[1] - half_of_combined_height
            bottom_of_all_boxes_y = self.point_to_center_on[1] + half_of_combined_height
            # Optionally check screen bounds here
        else:
            half_of_combined_width = self.get_combined_box_size(boxes) // 2
            left_of_all_boxes_x = self.point_to_center_on[0] - half_of_combined_width
            right_of_all_boxes_x = self.point_to_center_on[0] + half_of_combined_width
            # Optionally check screen bounds here

    def position_boxes(self, boxes: List['AbstractMenuBox']) -> None:
        self.ensure_boxes_can_fit(boxes)
        if self.is_vertical():
            total_height = self.get_combined_box_size(boxes)
            start_y = self.point_to_center_on[1] - total_height // 2
            for box in boxes:
                box.change_pos((self.point_to_center_on[0], start_y))
                start_y += box.get_height()
        else:
            total_width = self.get_combined_box_size(boxes)
            start_x = self.point_to_center_on[0] - total_width // 2
            for box in boxes:
                box.change_pos((start_x, self.point_to_center_on[1]))
                start_x += box.get_width()