from abc import ABC, abstractmethod
from collections.abc import Iterable
from pygame import draw, image, transform, Surface
from screen_info import CELL_WIDTH, CELL_HEIGHT

# === BASE CLASSES === #

class AbstractSkin(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def display(self, win: Surface, *args, **kwargs):
        pass


class SnakeSkinMixin:
    def set_segment_size(self, width: int, height: int):
        self.seg_width = width
        self.seg_height = height

    def get_segment_rect(self, column: int, row: int):
        return (column * CELL_WIDTH, row * CELL_HEIGHT, self.segment_w, self.segment_h)


# === COLOR SKINS === #

class AbstractColorSkin(AbstractSkin):
    def __init__(self, name: str, colors: Iterable[tuple], is_retro: bool = False):
        """
        Parameters: 
            - (str) name: The name of this skin
            - (Iterable[tuple]) colors: The color(s) of this skin. 
            - (bool) is_retro: Whether or not to display the rectangle as hollow
        """
        super().__init__(name)
        self.colors = colors
        self.is_retro = is_retro
        self.border = 2 if is_retro else 0


class RectangularColorSkin(AbstractColorSkin):
    """
    Saves 
    """
    def __init__(self, name: str, color: tuple, is_retro: bool = False):
        """
        Parameters: 
            - (str) name: The name of this skin
            - (tuple) color: The RGB color tuple value of this skin
            - (bool) is_retro: Whether or not to display the rectangle as hollow
        """
        super().__init__(name, [color], is_retro)
    
    @property
    def color(self):
        return self.colors[0]
    
    def display(self, win: Surface, rect: tuple):
        draw.rect(win, self.colors[0], rect, self.border)


class SnakeColorSkin(AbstractColorSkin, SnakeSkinMixin):
    def __init__(self, name: str, colors: Iterable[str], retro=False):
        super().__init__(name, colors, retro)
        self.set_segment_size(CELL_WIDTH, CELL_HEIGHT)

    def display(self, win: Surface, positions: Iterable[tuple[int, int]]):
        for seg_i, (col, row) in enumerate(positions):
            seg_rect = self.get_segment_rect(col, row)
            draw.rect(win, self.colors[seg_i % len(self.colors)], seg_rect, self.border)


# === IMAGE SKINS === #

class AbstractRectangularImageSkin(AbstractSkin):
    def __init__(self, name: str, img_path: str):
        super().__init__(name)
        self.image = image.load(img_path).convert_alpha()

    def blit_image(self, win: Surface, rect: tuple):
        win.blit(self.image, rect)


class RectangularImageSkin(AbstractRectangularImageSkin):
    def display(self, win: Surface,  rect: tuple):
        self.blit_image(win, rect)


class SnakeImageSkin(AbstractSkin, SnakeSkinMixin):
    def __init__(self, name, head_path, body_path):
        super().__init__(name)
        SnakeSkinMixin.set_segment_size(CELL_WIDTH, CELL_HEIGHT)
        unscaled_head = image.load(head_path).convert_alpha()
        unscaled_body = image.load(body_path).convert_alpha()
        self.head_img = transform.scale(unscaled_head, (self.seg_width, self.seg_height))
        self.body_img = transform.scale(unscaled_body, (self.seg_width, self.seg_height))
        
        # self.set_segment_size(
        #     max(self.head_img.get_width(), self.body_img.get_width()),
        #     max(self.head_img.get_height(), self.body_img.get_height())
        # )

    def display(self, win: Surface, positions: Iterable[tuple[int, int]]):
        win.blit(self.head_img, self.get_segment_rect(*positions[0]))
        for col, row in positions[1:]:
            win.blit(self.body_img, self.get_segment_rect(col, row))


# === SKIN MANAGERS === #

class AbstractSkinManager(ABC):
    def __init__(self):
        self.skins: dict[str, AbstractSkin] = {}

    def add_skin(self, skin: AbstractSkin):
        self.skins[skin.name] = skin

    def get_skin(self, name: str) -> AbstractSkin:
        return self.skins.get(name)

    @abstractmethod
    def add_all_img_skins(self, *args, **kwargs):
        pass


class RectangularSkinManager(AbstractSkinManager):
    def add_all_img_skins(self, dir_name: str):
        pass  # Future implementation


class SnakeSkinManager(AbstractSkinManager):
    def add_all_img_skins(self):
        path = "Assets/Sprites/Snake_Skin_Images"
        # for skin_name in get_all_dir_names_in_dir(path):
        #     self.add_skin(SnakeSkin(image_folder_name=skin_name))
