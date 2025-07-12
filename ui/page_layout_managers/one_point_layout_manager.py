from typing import TYPE_CHECKING


from ui.page_layout_managers.abstract_layout_manager import AbstractLayoutManager
from resource_modules.screen_info import SCREEN_WIDTH, SCREEN_HEIGHT, MENU_BOX_DEFAULT_FONT_SIZE
from resource_modules.enums import TextSurfacePosAnchor, OnePointLayout


if TYPE_CHECKING:
    from ui.components_of_menu import AbstractMenuBox

class OnePointLayoutManager(AbstractLayoutManager):
    """
    Layout manager that centers the Menu boxes around a point. 
    """
    def __init__(self, point: tuple[int, int], layout: OnePointLayout = OnePointLayout.VERTICAL):
        """
        Parameters: 
            - point: The point to horizontally and vertically center the menu boxes around
        """
        self.point_to_center_on = point
        self.layout = layout
        self.box_pos_anchor = TextSurfacePosAnchor.MIDDLE 
        self.spacing = MENU_BOX_DEFAULT_FONT_SIZE * 2
    
    def get_combined_box_height(self, boxes): 
        return sum(box.get_height() for box in boxes) + self.spacing * (len(boxes) - 1)
    
    def get_combined_box_width(self, boxes: list['AbstractMenuBox']):
        return sum(box.get_width() for box in boxes) + self.spacing * len(boxes) - 1
    
    def ensure_boxes_can_fit(self, boxes: list['AbstractMenuBox']):
        if self.layout == OnePointLayout.VERTICAL: 
            half_of_combined_height = self.get_combined_box_height(boxes) // 2 
            point_y = self.point_to_center_on[1]
            top_of_all_boxes_y = point_y + half_of_combined_height
            bottom_of_all_boxes_y = point_y - half_of_combined_height
            if bottom_of_all_boxes_y < 0 or top_of_all_boxes_y > SCREEN_HEIGHT:
                raise ValueError("Boxes do not fit vertically around point."
                                 f"End of boxes y = {self.top_of_all_boxes_y}. Point = {self.point_to_center_on}")
        if self.layout == OnePointLayout.HORIZONTAL: 
            half_of_combined_height = self.get_combined_box_height(boxes) // 2 
            point_y = self.point_to_center_on[1]
            top_of_all_boxes_y = point_y + half_of_combined_height
            bottom_of_all_boxes_y = point_y - half_of_combined_height
            if bottom_of_all_boxes_y < 0 or top_of_all_boxes_y > SCREEN_HEIGHT:
                raise ValueError("Boxes do not fit vertically around point."
                                 f"End of boxes y = {self.top_of_all_boxes_y}. Point = {self.point_to_center_on}")
    def position_boxes(self, boxes: list['AbstractMenuBox']):
        self.ensure_boxes_can_fit(boxes)
        spacing = 10  # Pixels between each box

        if self.layout == OnePointLayout.VERTICAL:
            # Compute total height (boxes + spacing)
            total_height = sum(box.get_height() for box in boxes) + spacing * (len(boxes) - 1)
            start_y = self.point_to_center_around[1] - total_height // 2
            center_x = self.point_to_center_around[0]

            current_y = start_y
            for box in boxes:
                box.change_display_pos((center_x, current_y))
                current_y += box.get_height() + spacing
                box.change_pos_anchor(TextSurfacePosAnchor.MIDDLE)

        elif self.layout == OnePointLayout.HORIZONTAL:
            # Compute total width (boxes + spacing)
            total_width = sum(box.get_width() for box in boxes) + spacing * (len(boxes) - 1)
            start_x = self.point_to_center_around[0] - total_width // 2
            center_y = self.point_to_center_around[1]

            current_x = start_x
            for box in boxes:
                box.change_display_pos((current_x, center_y))

                current_x += box.get_width() + spacing

        else:
            raise ValueError(f"Unsupported layout: {self.layout}")