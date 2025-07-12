from ui.page_layout_managers.one_point_layout_manager import OnePointLayoutManager
from ui.page_layout_managers.two_point_layout_manager import TwoPointLayoutManager
from ui.page_layout_managers.sector_layout_manager import VerticalSectorLayoutManager, HorizontalSectorLayoutManager

from resource_modules.enums import LayoutMangerTypes


class LayoutManagerFactory:
    @staticmethod
    def create(layout_type: LayoutMangerTypes, **kwargs):
        match layout_type:
            case LayoutMangerTypes.ONE_POINT:
                return OnePointLayoutManager(**kwargs)
            case LayoutMangerTypes.TWO_POINT:
                return TwoPointLayoutManager(**kwargs)
            case LayoutMangerTypes.VERTICAL_SECTOR:
                return VerticalSectorLayoutManager(**kwargs)
            case LayoutMangerTypes.HORIZONTAL_SECTOR:
                return HorizontalSectorLayoutManager(**kwargs)
            case _:
                raise ValueError(f"Unknown manager type: {layout_type}")