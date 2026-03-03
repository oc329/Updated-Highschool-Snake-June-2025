# ===== abstract_layout_manager.py =====

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List
from resource_modules.enums import Layout, TextSurfacePosAnchor

if TYPE_CHECKING:
    from ui.components_of_menu import AbstractMenuBox


class AbstractLayoutManager(ABC):
    """Base class for all layout managers."""
    
    def __init__(self, box_pos_anchor: TextSurfacePosAnchor = TextSurfacePosAnchor.MIDDLE):
        self.box_pos_anchor = box_pos_anchor

    @staticmethod
    def ensure_there_are_boxes(boxes: List['AbstractMenuBox']) -> None:
        if not boxes:
            raise IndexError("Page has no menu boxes; cannot select a box.")

    @staticmethod
    def get_combined_box_width(boxes: List['AbstractMenuBox']) -> int:
        return sum(box.get_width() for box in boxes)
    
    @staticmethod
    def get_combined_box_height(boxes: List['AbstractMenuBox']) -> int:
        return sum(box.get_height() for box in boxes)

    def _apply_box_positioning(self, box: 'AbstractMenuBox', pos: tuple[int, int]) -> None:
        """Helper method to apply positioning to a box."""
        box.change_pos_anchor(self.box_pos_anchor)
        box.change_pos(pos)

    @abstractmethod
    def position_boxes(self, boxes: List['AbstractMenuBox']) -> None:
        pass
    
    @abstractmethod
    def ensure_boxes_can_fit(self, boxes: List['AbstractMenuBox']) -> None:
        pass


# ===== two_point_layout_manager.py =====

from typing import TYPE_CHECKING, List
from resource_modules.enums import Layout, TextSurfacePosAnchor
from ui.page_layout_managers.abstract_layout_manager import AbstractLayoutManager

if TYPE_CHECKING:
    from ui.components_of_menu import AbstractMenuBox


class TwoPointLayoutManager(AbstractLayoutManager):
    """Handles both vertical and horizontal layouts with clean, shared logic."""
    
    def __init__(self, start_point: tuple[int, int], end_point: tuple[int, int],
                 box_pos_anchor: TextSurfacePosAnchor = TextSurfacePosAnchor.MIDDLE):
        super().__init__(box_pos_anchor)
        
        # Validate and determine layout
        self._validate_points(start_point, end_point)
        self.start_point = start_point
        self.end_point = end_point
        self.layout = self._determine_layout()
        
        # Store computed values for efficiency
        self.fixed_axis_value = self._get_fixed_axis_value()
        self.variable_axis_range = self._get_variable_axis_range()
    
    def _validate_points(self, start: tuple[int, int], end: tuple[int, int]) -> None:
        """Ensure points share exactly one axis."""
        if start == end:
            raise ValueError(f"Points cannot be identical: {start}")
        
        same_x = start[0] == end[0]
        same_y = start[1] == end[1]
        
        if not (same_x or same_y):
            raise ValueError(f"Points must share an axis: {start}, {end}")
        if same_x and same_y:
            raise ValueError(f"Points are identical: {start}, {end}")
    
    def _determine_layout(self) -> Layout:
        """Determine if this is vertical or horizontal layout."""
        return Layout.VERTICAL if self.start_point[0] == self.end_point[0] else Layout.HORIZONTAL
    
    def _get_fixed_axis_value(self) -> int:
        """Get the value for the axis that doesn't change (x for vertical, y for horizontal)."""
        return self.start_point[0] if self.layout == Layout.VERTICAL else self.start_point[1]
    
    def _get_variable_axis_range(self) -> tuple[int, int]:
        """Get (min, max) for the axis that varies."""
        if self.layout == Layout.VERTICAL:
            return min(self.start_point[1], self.end_point[1]), max(self.start_point[1], self.end_point[1])
        else:
            return min(self.start_point[0], self.end_point[0]), max(self.start_point[0], self.end_point[0])
    
    def get_available_space(self) -> int:
        """Get available space along the variable axis."""
        min_val, max_val = self.variable_axis_range
        return max_val - min_val
    
    def get_spacing(self, num_boxes: int) -> int:
        """Calculate spacing between boxes."""
        return self.get_available_space() // num_boxes
    
    def ensure_boxes_can_fit(self, boxes: List['AbstractMenuBox']) -> None:
        available = self.get_available_space()
        
        if self.layout == Layout.VERTICAL:
            required = self.get_combined_box_height(boxes)
            axis_name = "vertically"
        else:
            required = self.get_combined_box_width(boxes)
            axis_name = "horizontally"
        
        if required > available:
            raise ValueError(f"Boxes don't fit {axis_name}. "
                           f"Available: {available}, required: {required}")
    
    def position_boxes(self, boxes: List['AbstractMenuBox']) -> None:
        self.ensure_there_are_boxes(boxes)
        self.ensure_boxes_can_fit(boxes)
        
        min_val = self.variable_axis_range[0]
        spacing = self.get_spacing(len(boxes))
        
        for i, box in enumerate(boxes):
            variable_pos = min_val + spacing * i
            if self.layout == Layout.VERTICAL:
                pos = (self.fixed_axis_value, variable_pos)
            else:
                pos = (variable_pos, self.fixed_axis_value)
            self._apply_box_positioning(box, pos)


# ===== one_point_layout_manager.py =====

from enum import Enum
from typing import TYPE_CHECKING, List
from resource_modules.enums import Layout, TextSurfacePosAnchor
from ui.page_layout_managers.abstract_layout_manager import AbstractLayoutManager

if TYPE_CHECKING:
    from ui.components_of_menu import AbstractMenuBox


class Alignment(Enum):
    START = "start"      # Left for horizontal, Top for vertical
    CENTER = "center"    # Center for both
    END = "end"         # Right for horizontal, Bottom for vertical


class OnePointLayoutManager(AbstractLayoutManager):
    """Handles vertical/horizontal layouts with flexible alignment (start/center/end) from a single reference point."""
    
    def __init__(self, reference_point: tuple[int, int], layout: Layout, 
                 alignment: Alignment = Alignment.CENTER, spacing: int = 20,
                 box_pos_anchor: TextSurfacePosAnchor = TextSurfacePosAnchor.MIDDLE):
        super().__init__(box_pos_anchor)
        self.reference_point = reference_point
        self.layout = layout
        self.alignment = alignment
        self.spacing = spacing

    def get_total_size(self, boxes: List['AbstractMenuBox']) -> int:
        """Get total size needed along the layout axis."""
        if self.layout == Layout.VERTICAL:
            box_size = sum(box.get_height() for box in boxes)
        else:
            box_size = sum(box.get_width() for box in boxes)
        
        spacing_size = self.spacing * max(0, len(boxes) - 1)
        return box_size + spacing_size
    
    def _calculate_start_position(self, boxes: List['AbstractMenuBox']) -> int:
        """Calculate the starting position based on alignment."""
        total_size = self.get_total_size(boxes)
        
        if self.layout == Layout.VERTICAL:
            reference_coord = self.reference_point[1]
        else:
            reference_coord = self.reference_point[0]
        
        match self.alignment:
            case Alignment.START:
                return reference_coord
            case Alignment.CENTER:
                return reference_coord - total_size // 2
            case Alignment.END:
                return reference_coord - total_size
    
    def ensure_boxes_can_fit(self, boxes: List['AbstractMenuBox']) -> None:
        from resource_modules.screen_info import SCREEN_WIDTH, SCREEN_HEIGHT
        
        start_pos = self._calculate_start_position(boxes)
        total_size = self.get_total_size(boxes)
        end_pos = start_pos + total_size
        
        if self.layout == Layout.VERTICAL:
            screen_limit = SCREEN_HEIGHT
            axis_name = "vertically"
        else:
            screen_limit = SCREEN_WIDTH
            axis_name = "horizontally"
        
        if start_pos < 0 or end_pos > screen_limit:
            raise ValueError(f"Boxes don't fit {axis_name} with {self.alignment.value} alignment "
                           f"at {self.reference_point}")
    
    def position_boxes(self, boxes: List['AbstractMenuBox']) -> None:
        self.ensure_there_are_boxes(boxes)
        self.ensure_boxes_can_fit(boxes)
        
        start_pos = self._calculate_start_position(boxes)
        current_pos = start_pos
        
        if self.layout == Layout.VERTICAL:
            fixed_axis_value = self.reference_point[0]  # x stays the same
            
            for box in boxes:
                pos = (fixed_axis_value, current_pos)
                self._apply_box_positioning(box, pos)
                current_pos += box.get_height() + self.spacing
        else:
            fixed_axis_value = self.reference_point[1]  # y stays the same
            
            for box in boxes:
                pos = (current_pos, fixed_axis_value)
                self._apply_box_positioning(box, pos)
                current_pos += box.get_width() + self.spacing


# ===== sector_layout_manager.py =====

from enum import Enum
from typing import TYPE_CHECKING, List
from resource_modules.enums import Layout, TextSurfacePosAnchor
from ui.page_layout_managers.abstract_layout_manager import AbstractLayoutManager

if TYPE_CHECKING:
    from ui.components_of_menu import AbstractMenuBox


class SectorAlignment(Enum):
    # Horizontal alignments
    LEFT = "left"
    CENTER_H = "center_h" 
    RIGHT = "right"
    
    # Vertical alignments  
    TOP = "top"
    CENTER_V = "center_v"
    BOTTOM = "bottom"


class SectorLayoutManager(AbstractLayoutManager):
    """Positions boxes within a rectangular sector with flexible alignment."""
    
    def __init__(self, top_left: tuple[int, int], bottom_right: tuple[int, int],
                 layout: Layout, h_alignment: SectorAlignment = SectorAlignment.CENTER_H,
                 v_alignment: SectorAlignment = SectorAlignment.CENTER_V, spacing: int = 10,
                 box_pos_anchor: TextSurfacePosAnchor = TextSurfacePosAnchor.MIDDLE):
        super().__init__(box_pos_anchor)
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.layout = layout
        self.h_alignment = h_alignment
        self.v_alignment = v_alignment
        self.spacing = spacing
        
        # Validate sector
        if top_left[0] >= bottom_right[0] or top_left[1] >= bottom_right[1]:
            raise ValueError(f"Invalid sector: {top_left} to {bottom_right}")
    
    def get_sector_width(self) -> int:
        return self.bottom_right[0] - self.top_left[0]
    
    def get_sector_height(self) -> int:
        return self.bottom_right[1] - self.top_left[1]
    
    def get_total_box_size(self, boxes: List['AbstractMenuBox']) -> int:
        """Get total size needed along the layout axis."""
        if self.layout == Layout.VERTICAL:
            box_size = sum(box.get_height() for box in boxes)
        else:
            box_size = sum(box.get_width() for box in boxes)
        
        spacing_size = self.spacing * max(0, len(boxes) - 1)
        return box_size + spacing_size
    
    def _calculate_fixed_axis_position(self) -> int:
        """Calculate position on the axis that doesn't change (x for vertical, y for horizontal)."""
        if self.layout == Layout.VERTICAL:
            # Calculate x position based on horizontal alignment
            match self.h_alignment:
                case SectorAlignment.LEFT:
                    return self.top_left[0]
                case SectorAlignment.CENTER_H:
                    return self.top_left[0] + self.get_sector_width() // 2
                case SectorAlignment.RIGHT:
                    return self.bottom_right[0]
        else:
            # Calculate y position based on vertical alignment
            match self.v_alignment:
                case SectorAlignment.TOP:
                    return self.top_left[1]
                case SectorAlignment.CENTER_V:
                    return self.top_left[1] + self.get_sector_height() // 2
                case SectorAlignment.BOTTOM:
                    return self.bottom_right[1]
    
    def _calculate_variable_axis_start(self, boxes: List['AbstractMenuBox']) -> int:
        """Calculate starting position on the variable axis."""
        total_size = self.get_total_box_size(boxes)
        
        if self.layout == Layout.VERTICAL:
            # Calculate y start position based on vertical alignment
            match self.v_alignment:
                case SectorAlignment.TOP:
                    return self.top_left[1]
                case SectorAlignment.CENTER_V:
                    return self.top_left[1] + (self.get_sector_height() - total_size) // 2
                case SectorAlignment.BOTTOM:
                    return self.bottom_right[1] - total_size
        else:
            # Calculate x start position based on horizontal alignment
            match self.h_alignment:
                case SectorAlignment.LEFT:
                    return self.top_left[0]
                case SectorAlignment.CENTER_H:
                    return self.top_left[0] + (self.get_sector_width() - total_size) // 2
                case SectorAlignment.RIGHT:
                    return self.bottom_right[0] - total_size
    
    def ensure_boxes_can_fit(self, boxes: List['AbstractMenuBox']) -> None:
        total_size = self.get_total_box_size(boxes)
        
        if self.layout == Layout.VERTICAL:
            available = self.get_sector_height()
            axis_name = "vertically"
        else:
            available = self.get_sector_width()
            axis_name = "horizontally"
        
        if total_size > available:
            raise ValueError(f"Boxes don't fit {axis_name} in sector. "
                           f"Available: {available}, required: {total_size}")
    
    def position_boxes(self, boxes: List['AbstractMenuBox']) -> None:
        self.ensure_there_are_boxes(boxes)
        self.ensure_boxes_can_fit(boxes)
        
        fixed_axis_pos = self._calculate_fixed_axis_position()
        variable_axis_start = self._calculate_variable_axis_start(boxes)
        current_pos = variable_axis_start
        
        for box in boxes:
            if self.layout == Layout.VERTICAL:
                pos = (fixed_axis_pos, current_pos)
                current_pos += box.get_height() + self.spacing
            else:
                pos = (current_pos, fixed_axis_pos)
                current_pos += box.get_width() + self.spacing
            
            self._apply_box_positioning(box, pos)


# ===== layout_manager_factory.py =====

from ui.page_layout_managers.one_point_layout_manager import OnePointLayoutManager
from ui.page_layout_managers.aligned_layout_manager import AlignedLayoutManager
from ui.page_layout_managers.two_point_layout_manager import TwoPointLayoutManager
from ui.page_layout_managers.sector_layout_manager import SectorLayoutManager
from resource_modules.enums import LayoutManagerTypes


class LayoutManagerFactory:
    """Simple factory for creating layout managers."""
    
    @staticmethod
    def create(layout_type: LayoutManagerTypes, **kwargs):
        match layout_type:
            case LayoutManagerTypes.ONE_POINT:
                return OnePointLayoutManager(**kwargs)
            case LayoutManagerTypes.ALIGNED:
                return AlignedLayoutManager(**kwargs)
            case LayoutManagerTypes.TWO_POINT:
                return TwoPointLayoutManager(**kwargs)
            case LayoutManagerTypes.SECTOR:
                return SectorLayoutManager(**kwargs)
            case _:
                raise ValueError(f"Unknown layout type: {layout_type}")


# ===== enums.py (additions to your existing enums file) =====

# Add these to your existing resource_modules/enums.py file:

class LayoutManagerTypes(Enum):
    ONE_POINT = "one_point"      # Centers around a point
    ALIGNED = "aligned"          # Aligns relative to a point (start/center/end)
    TWO_POINT = "two_point"      # Distributes between two points
    SECTOR = "sector"            # Positions within a rectangle

# Your existing Layout and TextSurfacePosAnchor enums remain the same


# ===== __init__.py =====

# ui/page_layout_managers/__init__.py

from .abstract_layout_manager import AbstractLayoutManager
from .one_point_layout_manager import OnePointLayoutManager
from .aligned_layout_manager import AlignedLayoutManager, Alignment
from .two_point_layout_manager import TwoPointLayoutManager  
from .sector_layout_manager import SectorLayoutManager, SectorAlignment
from .layout_manager_factory import LayoutManagerFactory

__all__ = [
    'AbstractLayoutManager',
    'OnePointLayoutManager',
    'AlignedLayoutManager', 
    'TwoPointLayoutManager',
    'SectorLayoutManager',
    'LayoutManagerFactory',
    'Alignment',
    'SectorAlignment'
]


# ===== USAGE EXAMPLES =====

"""
# Example usage showing the difference:

# ONE-POINT: Classic centered layout around a point
main_menu = OnePointLayoutManager(
    center_point=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2),
    layout=Layout.VERTICAL
)

# ALIGNED: Flexible alignment relative to a point  
left_sidebar = AlignedLayoutManager(
    reference_point=(50, 200),
    layout=Layout.VERTICAL, 
    alignment=Alignment.START  # Start from the point (not centered)
)

right_sidebar = AlignedLayoutManager(
    reference_point=(SCREEN_WIDTH-50, 200),
    layout=Layout.VERTICAL,
    alignment=Alignment.END    # End at the point
)

# TWO-POINT: Distribute between exact points
button_row = TwoPointLayoutManager(
    start_point=(50, SCREEN_HEIGHT-50),
    end_point=(SCREEN_WIDTH-50, SCREEN_HEIGHT-50)
)

# SECTOR: Within a rectangular area
dialog = SectorLayoutManager(
    top_left=(300, 200), 
    bottom_right=(500, 400),
    layout=Layout.VERTICAL,
    h_alignment=SectorAlignment.CENTER_H,
    v_alignment=SectorAlignment.CENTER_V
)
"""