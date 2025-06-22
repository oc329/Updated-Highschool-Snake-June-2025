from abc import ABC, abstractmethod

from enums import SectorType, HorizontalSectorPosAnchor, TextSurfacePosAnchor, VerticalSectorPosAnchor

class AbstractSectorLayoutManager(ABC):
    def __init__(self, top_left_pos: tuple[int, int], bottom_right_pos: tuple[int, int],
                sector_type = SectorType.VERTICAL, sector_pos_anchor = VerticalSectorPosAnchor.MIDDLE, box_pos_anchor = TextSurfacePosAnchor.MIDDLE):
        """
        Sector Layout Managers position the boxes within the sector based on the sector position anchor. 

        Parameters: 
            - (tuple[int, int]) top_left_pos: The top left position of the sector
            - (tuple[int, int]) bottom_right_pos: The bottom right position of the sector
            - (SectorType) sector_type: The sector type (horizontal, vertical, etc) determines how the boxes are displayed in the boxes list
            - (AbstractSectorPosAnchor) sector_pos_anchor: The string enum value that tells where on the sector the boxes should be displayed (ex. MIDDLE)
            - (TextSurfacePosAnchor) box_pos_anchor: The anchor that tells the box how it should be displayed in relation to its display pos (start, end, middle)
        """
        self.top_left_pos = top_left_pos
        self.bottom_right_pos = bottom_right_pos 
        self.sector_type = sector_type
        self.sector_pos_anchor = sector_pos_anchor
        self.box_pos_anchor = box_pos_anchor

    @property
    def top_of_sector_y(self) -> int:
        """
        Returns the y coordinate of the top of the sector
        """
        return self.top_left_pos[1]
    
    # def calculate_spacing_btw_boxes(start: int, end: int, num_boxes: int, box_size: int) -> int:
    #     """
    #     Calculates the spacing btw boxes based on the start and end (x for horizontal, y for vertical)
    #     """
    #     total_space = end - start
    #     total_box_space = box_size * num_boxes
    #     leftover_space = total_space - total_box_space

    #     spacing = leftover_space // (num_boxes - 1)
    #     return spacing
    
    def ensure_there_are_boxes(self, boxes: list):
        """
        Raises an error if thee menu boxes list is empty. 
        
        Parameters: 
            - (list) boxes: The list of menu boxes on the page
        """
        if not boxes:
            raise IndexError("Page has no menu boxes; cannot select a box.")
    
    @abstractmethod
    def position_boxes(self, boxes: list):
        """
        Abstract method for positioning boxes in the sector.
        """
        pass

class VerticalSectorLayoutManager(AbstractSectorLayoutManager):
    def __init__(self, top_left_pos: tuple[int, int], bottom_right_pos: tuple[int, int], 
                sector_pos_anchor = VerticalSectorPosAnchor.MIDDLE, box_pos_anchor = TextSurfacePosAnchor.MIDDLE):
        super().__init__(top_left_pos, bottom_right_pos, SectorType.VERTICAL, sector_pos_anchor, box_pos_anchor)

    def ensure_boxes_fit_in_vertical_sector(self, boxes: list):
        box_height = boxes[0].get_height()
        num_boxes = len(boxes)
        min_sector_height = num_boxes * box_height 
        ## graphics are in 4th sector so y is greater lower down
        sector_height = self.bottom_right_pos[1] - self.top_left_pos[1]

        if min_sector_height > sector_height:
            raise ValueError(f"Boxes do not fit vertically in sector. "
                            f"Sector height: {sector_height}, required: {min_sector_height}")

    def get_menu_box_x(self) -> int:
        """
        Returns the x coordinate of each menu box in the sector 
        based on the position anchor and the top left position.
        From top left pos, how much to add: left is 0, Middle is half the sector width, and right is sector width

        Returns: 
            - The x coordinate of each menu box
        """
        if self.sector_pos_anchor == VerticalSectorPosAnchor.LEFT:
            menu_box_x = self.top_left_pos[0]
        elif self.sector_pos_anchor == VerticalSectorPosAnchor.MIDDLE:
            half_of_sector_width = self.top_left_pos[0] + (self.top_left_pos[0] - self.bottom_right_pos[0]) // 2
            menu_box_x = half_of_sector_width
        elif self.sector_pos_anchor == VerticalSectorPosAnchor.RIGHT:
            sector_width = self.top_left_pos[0] + (self.top_left_pos[0] - self.bottom_right_pos[0])
            menu_box_x = sector_width
        else: 
            raise ValueError("Given Vertical Sector Anchor Position isn't valid")
        
        return menu_box_x

    def position_boxes(self, boxes: list):
        self.ensure_there_are_boxes(boxes)
        box_height = boxes[0].get_height()
        self.ensure_boxes_fit_in_vertical_sector(boxes)

        bottom_y, top_y = self.bottom_right_pos[1], self.top_left_pos[1]
        display_interval = (bottom_y - top_y) // len(boxes)
        menu_box_x = self.get_menu_box_x()

        for box_i, box in enumerate(boxes):
            box.change_pos_anchor(self.box_pos_anchor)
            pos = (menu_box_x, top_y + display_interval * box_i)
            box.change_pos(pos)

class HorizontalSectorLayoutManager(AbstractSectorLayoutManager):
    """
    Positions the menu boxes horizontally from left to right
    """
    def __init__(self, top_left_pos: tuple[int, int], bottom_right_pos: tuple[int, int], 
                sector_pos_anchor = HorizontalSectorPosAnchor.TOP, box_pos_anchor = TextSurfacePosAnchor.START):
        super().__init__(top_left_pos, bottom_right_pos, SectorType.HORIZONTAL, sector_pos_anchor, box_pos_anchor)
    
    def _calculate_combined_boxes_width(self, boxes: list):
        """
        Adds up the width of each box and 
        returns the combined width of all the boxes in the given boxes list.

        Parameter: 
            - (list) boxes: List of all the menu boxes on the page
        """
        return sum(box.get_width for box in boxes)
     
    def ensure_boxes_fit_in_horizontal_sector(self, boxes: list):
        min_sector_width = self._calculate_combined_boxes_width(boxes)
        sector_width = self.top_left_pos[0] - self.bottom_right_pos[0]

        if min_sector_width > sector_width:
            raise ValueError(f"Boxes do not fit horizontally in sector. "
                            f"Sector width: {sector_width}, required: {min_sector_width}")
        
    def get_menu_box_y(self) -> int:
        """
        Returns the t coordinate of each menu box in the sector 
        based on the position anchor and the top left position.
        From top left pos, how much to add to y: top is 0, middle is half the sector height, and bottom is sector height

        Returns: 
            - The y coordinate of each menu box
        """
        if self.sector_pos_anchor == HorizontalSectorPosAnchor.TOP:
            menu_box_y = self.top_left_pos[1]
        elif self.sector_pos_anchor == HorizontalSectorPosAnchor.MIDDLE:
            half_of_sector_height = self.top_left_pos[1] + (self.top_left_pos[1] - self.bottom_right_pos[1]) // 2
            menu_box_y = half_of_sector_height
        elif self.sector_pos_anchor == HorizontalSectorPosAnchor.BOTTOM:
            sector_height = self.top_left_pos[1] + (self.top_left_pos[1] - self.bottom_right_pos[1])
            menu_box_y = sector_height

        return menu_box_y
    def position_boxes(self, boxes: list):
        """
        Positions the page's menu boxes into the horizontal sector.
        Raises an error if the combined menu boxes' width is greater than the sector width. 
        """
        self.ensure_there_are_boxes(boxes)
        self.ensure_boxes_fit_in_horizontal_sector(boxes)
        display_interval = (self.bottom_right_pos[0] - self.top_left_pos[0]) // len(boxes)
        menu_box_y = self.get_menu_box_y()
        for box_i, box in enumerate(boxes):
            box.change_pos_anchor(self.box_pos_anchor
            )
            pos = (self.top_left_pos[0] + display_interval * box_i, menu_box_y)
            box.change_pos(pos)


