from abc import ABC, abstractmethod
from collections.abc import Iterable

from resource_modules.colors import RAINBOW_SNAKE_COLORS_NAME_TO_RGB_LOOKUP
from resource_modules.enums import Direction
from resource_modules.img_loader import get_skin_name_to_head_body_images_lookup
from pygame import draw, image, transform, Surface
from resource_modules.screen_info import CELL_WIDTH, CELL_HEIGHT, convert_grid_pos_to_display_pos, grid_pos_is_on_screen, TOTAL_COLUMNS, TOTAL_ROWS

# === BASE CLASSES === #

class AbstractSkin(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def display(self, win: Surface, *args, **kwargs):
        pass


class SnakeSkinMixin:
    """
    A Mixin for Image and Color SnakeSkins to set the segment size and calculate segment rect
    """
    def set_segment_size(self, width: int, height: int):
        self.seg_width = width
        self.seg_height = height

    def get_segment_rect(self, grid_pos: tuple[int, int]):
        """
        Calculates the rect tuple of the current segment. 

        Parameters: 
            - (tuple[int, int]) grid_pos: The column and row of the current segment. 
        """
        return (*convert_grid_pos_to_display_pos(grid_pos), self.seg_width, self.seg_height)

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
        self.border = (CELL_WIDTH + CELL_HEIGHT) // 12 if is_retro else 0


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
    def __init__(self, name: str, colors: Iterable[str], is_retro = False):
        """
         - (str) name: The name of this skin
         - (tuple) colors: The Iterable of RGB color tuple value of this skin. Each segment gets a color from colors accordignly 
                            and when the snake is longer than colors, colors is looped through again
         - (bool) is_retro: Whether or not to display the rectangle as hollow
        """
        super().__init__(name, colors, is_retro)
        self.set_segment_size(CELL_WIDTH, CELL_HEIGHT)

    def display(self, win: Surface, positions: Iterable[tuple[int, int]], direction = None):
        for seg_i, grid_pos in enumerate(positions):
            if not grid_pos_is_on_screen(grid_pos):
                continue  # Skip drawing off-screen segments
            seg_rect = self.get_segment_rect(grid_pos)
            seg_color = self.colors[seg_i % len(self.colors)]
            draw.rect(win, seg_color, seg_rect, self.border)


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
    def __init__(self, name: str, head_img: Surface, body_img: Surface):
        super().__init__(name)
        self.set_segment_size(CELL_WIDTH, CELL_HEIGHT)
        self.head_img = head_img 
        self.body_img = body_img
        self.head_images_by_direction = {
            Direction.RIGHT.value : head_img,
            Direction.UP.value : transform.rotate(head_img, 90),
            Direction.LEFT.value : transform.flip(head_img, True, False),
            Direction.DOWN.value : transform.rotate(head_img, 270)
        }
        self.current_head_direction_img = Direction.RIGHT

    
    def change_current_direction_head_img(self, direction: Direction):
        self.current_head_direction_img = self.head_images_by_direction[direction] 

    def display(self, win: Surface, positions: Iterable[tuple[int, int]], direction: Direction = None):
        self.change_current_direction_head_img(direction)
        if grid_pos_is_on_screen(positions[0]):
            win.blit(self.current_head_direction_img, self.get_segment_rect(positions[0]))
        for grid_pos in positions[1:]:
            if not grid_pos_is_on_screen(grid_pos):
                continue  # Skip drawing off-screen segments
            win.blit(self.body_img, self.get_segment_rect(grid_pos))


# === SKIN MANAGERS === #

class AbstractSkinManager(ABC):
    """
    Holds all the available Skins of images or color for an object like Snake or Apple
    """
    def __init__(self):
        self.skins = []
        self.create_all_skins()
    
    @abstractmethod
    def create_all_skins(self):
        """
        Creates all the skins and sets it the skins attribute
        """
        raise NotImplementedError()

    def get_skin(self, target_name: str) -> AbstractSkin:
        """
        Returns the Skin object that has the given name
        """
        return next((skin for skin in self.skins if skin.name == target_name), None)
    
    def get_all_skins(self) -> list[AbstractSkin]:
        """
        Returns all the skins in this Skin Manager
        """
        return self.skins

class RectangularSkinManager(AbstractSkinManager):
    def add_all_img_skins(self, dir_name: str):
        pass  # Future implementation

class ColorSnakeSkinManager(AbstractSkinManager):
    def create_all_skins(self):
        is_retro = True
        for color_name, color_rgb in RAINBOW_SNAKE_COLORS_NAME_TO_RGB_LOOKUP.items():
            self.skins.append(SnakeColorSkin(color_name, (color_rgb, ), is_retro))

        rainbow_colors = (tuple(RAINBOW_SNAKE_COLORS_NAME_TO_RGB_LOOKUP.values()))
        rainbow_snake_skin = SnakeColorSkin("RAINBOW", rainbow_colors, is_retro)
        self.skins.append(rainbow_snake_skin)

class ImageSnakeSkinManager(AbstractSkinManager):
    def create_all_skins(self):
        all_img_skin_names_to_head_body_imgs = get_skin_name_to_head_body_images_lookup()
        for skin_name, head_body_dict in all_img_skin_names_to_head_body_imgs.items():
            snake_head_img = head_body_dict["head"]
            snake_body_img = head_body_dict["body"]
            self.skins.append(SnakeImageSkin(skin_name, snake_head_img, snake_body_img))

color_snake_skin_manager = ColorSnakeSkinManager()
img_snake_manager = ImageSnakeSkinManager()