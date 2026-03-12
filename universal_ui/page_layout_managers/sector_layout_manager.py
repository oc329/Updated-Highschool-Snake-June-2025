from abc import ABC, abstractmethod

from ui.page_layout_managers.abstract_layout_manager import AbstractTwoPointLayoutManager
from resource_modules.enums import AbstractSectorPosAnchor, Layout, HorizontalSectorPosAnchor, TextSurfacePosAnchor, VerticalSectorPosAnchor

class AbstractSectorLayoutManager(AbstractTwoPointLayoutManager):
    def __init__(self, top_left_pos: tuple[int, int], bottom_right_pos: tuple[int, int],
                layout: Layout, sector_pos_anchor = AbstractSectorPosAnchor, box_pos_anchor = TextSurfacePosAnchor.MIDDLE):
        """
        Sector Layout Managers position the boxes within the sector based on the sector position anchor. 

        Parameters: 
            - (tuple[int, int]) top_left_pos: The top left position of the sector
            - (tuple[int, int]) bottom_right_pos: The bottom right position of the sector
            - (Layout) layout: The layout Enum (Vertical or Horizontal) determines how the boxes are positioned
            - (AbstractSectorPosAnchor) sector_pos_anchor: The string enum value that tells where on the sector the boxes should be displayed (ex. MIDDLE)
            - (TextSurfacePosAnchor) box_pos_anchor: The anchor that tells the box how it should be displayed in relation to its display pos (start, end, middle)
        """
        self.top_left_pos = top_left_pos
        self.bottom_right_pos = bottom_right_pos 
        self.sector_pos_anchor = sector_pos_anchor
        point1, point2, = self.get_points_based_on_sector_pos_anchor()

        super().__init__(layout, point1, point2, box_pos_anchor = box_pos_anchor)

    @abstractmethod
    def get_points_based_on_sector_pos_anchor(self) -> tuple[tuple[int, int], tuple[int, int]]:
        """
        Returns the two points that define the sector based on the sector position anchor.
        """
        raise NotImplementedError()
        
    def get_anchor_axis_value(self) -> int:
        """
        Calculates the axis value for each menu box based on the sector boundaries.
        """
        return self.sector_pos_anchor.calculate_axis_value(self.top_left_pos, self.bottom_right_pos)

    @abstractmethod
    def get_spacing(self, boxes): ...

class VerticalSectorLayoutManager(AbstractSectorLayoutManager):
    def __init__(self, top_left_pos: tuple[int, int], bottom_right_pos: tuple[int, int], 
                sector_pos_anchor: VerticalSectorPosAnchor = VerticalSectorPosAnchor.MIDDLE, box_pos_anchor: TextSurfacePosAnchor = TextSurfacePosAnchor.MIDDLE):
        super().__init__(top_left_pos, bottom_right_pos, Layout.VERTICAL, sector_pos_anchor, box_pos_anchor)

    def get_spacing(self, boxes):
        return (self.bottom_right_pos[1] - self.top_left_pos[1]) // len(boxes)
        
    def ensure_boxes_can_fit(self, boxes: list):
        """
        Ensures the combined box height is less than the sector height
        """
        if self.layout == Layout.VERTICAL:
            self.ensure_boxes_can_fit_btw_two_points(boxes, Layout.VERTICAL, self.top_left_pos, self.bottom_right_pos)
            combined_box_height = self.get_combined_box_height(boxes)
            ## graphics are in 4th sector so y is greater lower down
            sector_height = self.bottom_right_pos[1] - self.top_left_pos[1]

            if combined_box_height > sector_height:
                raise ValueError(f"Boxes do not fit vertically in sector. "
                                f"Sector height: {sector_height}, required: {combined_box_height}")
    def get_points_based_on_sector_pos_anchor(self):
        x = self.sector_pos_anchor.calculate_axis_value(self.top_left_pos, self.bottom_right_pos)
        return (x, self.top_left_pos[1]), (x, self.bottom_right_pos[1])
    
    def position_boxes(self, boxes: list):
        self.position_boxes_vertical(boxes)

class HorizontalSectorLayoutManager(AbstractSectorLayoutManager):
    """
    Positions the menu boxes horizontally from left to right
    """
    def __init__(self, top_left_pos: tuple[int, int], bottom_right_pos: tuple[int, int], 
                sector_pos_anchor: HorizontalSectorPosAnchor = HorizontalSectorPosAnchor.TOP, box_pos_anchor: TextSurfacePosAnchor = TextSurfacePosAnchor.START):
        super().__init__(top_left_pos, bottom_right_pos, Layout.HORIZONTAL, sector_pos_anchor, box_pos_anchor)
    
    def get_points_based_on_sector_pos_anchor(self):
        y = self.sector_pos_anchor.calculate_axis_value(self.top_left_pos, self.bottom_right_pos)
        
        return (self.top_left_pos[0], y), (self.bottom_right_pos[0], y)
    def ensure_boxes_can_fit(self, boxes: list):
        min_sector_width = self.get_combined_box_width(boxes)
        sector_width = self.bottom_right_pos[0] - self.top_left_pos[0]

        if min_sector_width > sector_width:
            raise ValueError(f"Boxes do not fit horizontally in sector. "
                            f"Sector width: {sector_width}, required: {min_sector_width}")

    def position_boxes(self, boxes: list):
        """
        Positions the page's menu boxes into the horizontal sector.
        Raises an error if the combined menu boxes' width is greater than the sector width. 
        """
        self.position_boxes_horizontal(boxes)