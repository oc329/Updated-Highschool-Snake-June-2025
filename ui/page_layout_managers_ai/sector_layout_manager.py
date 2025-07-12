from typing import Tuple, List, TYPE_CHECKING
from ui.page_layout_managers_ai.base_axis_layout_manager import AbstractTwoPointLayoutManager
from resource_modules.enums import Layout, AbstractSectorPosAnchor, TextSurfacePosAnchor

if TYPE_CHECKING:
    from ui.components_of_menu import AbstractMenuBox

class SectorLayoutManager(AbstractTwoPointLayoutManager):
    """
    Sector Layout Managers position the boxes within the sector based on the sector position anchor.
    """

    def __init__(
        self,
        top_left_pos: Tuple[int, int],
        bottom_right_pos: Tuple[int, int],
        layout: Layout,
        sector_pos_anchor: AbstractSectorPosAnchor = AbstractSectorPosAnchor,
        box_pos_anchor: TextSurfacePosAnchor = TextSurfacePosAnchor.MIDDLE,
    ):
        """
        Parameters:
            - (tuple[int, int]) top_left_pos: The top left position of the sector
            - (tuple[int, int]) bottom_right_pos: The bottom right position of the sector
            - (Layout) layout: The layout Enum (Vertical or Horizontal) determines how the boxes are positioned
            - (AbstractSectorPosAnchor) sector_pos_anchor: The value that tells where on the sector the boxes should be displayed (ex. MIDDLE)
            - (TextSurfacePosAnchor) box_pos_anchor: The anchor that tells the box how it should be displayed in relation to its display pos (start, end, middle)
        """
        super().__init__(layout)
        self.top_left_pos = top_left_pos
        self.bottom_right_pos = bottom_right_pos
        self.sector_pos_anchor = sector_pos_anchor
        self.box_pos_anchor = box_pos_anchor

    def get_anchor_axis_value(self) -> int:
        """
        Calculates the axis value for each menu box based on the sector boundaries.
        """
        return self.sector_pos_anchor.calculate_axis_value(self.top_left_pos, self.bottom_right_pos)
    
    def get_spacing(self, boxes: List['AbstractMenuBox']) -> int:
        if self.is_vertical():
            total_space = self.bottom_right_pos[1] - self.top_left_pos[1]
        else:
            total_space = self.bottom_right_pos[0] - self.top_left_pos[0]
        combined_size = self.get_combined_box_size(boxes)
        return (total_space - combined_size) // (len(boxes) + 1)

    def ensure_boxes_can_fit(self, boxes: List['AbstractMenuBox']) -> None:
        self.ensure_boxes_can_fit_btw_points(boxes, self.layout, self.top_left_pos, self.bottom_right_pos)

    def position_boxes(self, boxes: List['AbstractMenuBox']) -> None:
        self.ensure_boxes_can_fit(boxes)
        axis_value = self.get_anchor_axis_value()
        spacing = self.get_spacing(boxes)
        start_value = (self.top_left_pos[1] if self.is_vertical() else self.top_left_pos[0]) + spacing
        if self.is_vertical():
            changing_y = start_value
            for box in boxes:
                box.change_pos((axis_value, changing_y))
                changing_y += box.get_height() + spacing
        else:
            changing_x = start_value
            for box in boxes:
                box.change_pos((changing_x, axis_value))
                changing_x += box.get_width() + spacing