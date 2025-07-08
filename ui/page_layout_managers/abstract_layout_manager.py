from abc import ABC, abstractmethod
class AbstractLayoutManager(ABC):
    def __init__(self):
        pass
        
    @abstractmethod
    def position_boxes(self, boxes: list):
        """
        Abstract method for positioning boxes in the sector.
        """
        pass