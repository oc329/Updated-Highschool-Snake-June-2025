from typing import Tuple, List
from ui.page_layout_managers_ai.base_axis_layout_manager import BaseAxisLayoutManager
from resource_modules.enums import Layout, AbstractSectorPosAnchor, TextSurfacePosAnchor

if TYPE_CHECKING:
    from ui.components_of_menu import AbstractMenuBox

class TwoPointLayoutManager(BaseAxisLayoutManager):
    """
    Layout manager that positions boxes between two points, either vertically or horizontally.
    """

    def __init__(
        self,
        point1: Tuple[int, int],
        point2: Tuple[int, int],
        sector_pos_anchor: AbstractSectorPosAnchor = AbstractSectorPosAnchor,
        box_pos_anchor: TextSurfacePosAnchor = TextSurfacePosAnchor.MIDDLE,
    ):
        """
        Parameters:
            - (tuple[int, int]) point1: The first point in the sector
            - (tuple[int, int]) point2: The second point in the sector
            - (AbstractSectorPosAnchor) sector_pos_anchor: Where boxes should be displayed in the sector
            - (TextSurfacePosAnchor) box_pos_anchor: The anchor for each box's position
        """
        layout = Layout.VERTICAL if point1[0] == point2[0] else Layout.HORIZONTAL
        super().__init__(layout)
        self.point1 = point1
        self.point2 = point2
        self.sector_pos_anchor = sector_pos_anchor
        self.box_pos_anchor = box_pos_anchor

    def get_spacing(self, boxes: List['AbstractMenuBox']) -> int:
        if self.is_vertical():
            total_space = abs(self.point2[1] - self.point1[1])
        else:
            total_space = abs(self.point2[0] - self.point1[0])
        combined_size = self.get_combined_box_size(boxes)
        return (total_space - combined_size) // (len(boxes) + 1)

    def ensure_boxes_can_fit(self, boxes: List['AbstractMenuBox']) -> None:
        self.ensure_boxes_can_fit_btw_points(boxes, self.layout, self.point1, self.point2)

    def position_boxes(self, boxes: List['AbstractMenuBox']) -> None:
        self.ensure_boxes_can_fit(boxes)
        spacing = self.get_spacing(boxes)
        pos = (self.point1[1] if self.is_vertical() else self.point1[0]) + spacing
        for box in boxes:
            if self.is_vertical():
                box.change_pos((self.sector_pos_anchor, pos))
                pos += box.get_height() + spacing
            else:
                box.change_pos((pos, self.sector_pos_anchor))
                pos += box.get_width() + spacing