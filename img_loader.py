from pygame import image, transform, Surface

from colors import WHITE
from file_paths import ensure_path_exists


def load_img(absolute_img_path: str) -> Surface:
    ensure_path_exists(absolute_img_path)
    return image.load(absolute_img_path)

def load_alpha_img(absolute_img_path: str):
    """
    Loads an image and converts the alpha
    """
    return load_img(absolute_img_path).convert_alpha()

def load_regular_img(absolute_img_path: str):
    """
    Loads an image and converts it
    """
    return load_img(absolute_img_path).convert()

def load_img_with_white_bg_and_scale_to_size(absolute_img_path: str, size_to_scale_to: tuple[int, int]):
    """
    Loads an image that has a white background. 
    Makes the white background transparaent ands scales the img to the given size

    Parameters: 
        - (str) absolute_img_path: Absolute file path to the image 
        - (tuple[int, int]) size_to_scale_to: Size tuple (width, height) to scale the image to
    """
    unscaled_img = load_regular_img(absolute_img_path)
    unscaled_img.set_colorkey(WHITE)
    scaled_img = transform.scale(unscaled_img, size_to_scale_to) ## scales the image to the size of a cell in the grid
    return scaled_img

def load_alpha_img_and_scale_to_size(absolute_img_path: str, size_to_scale_to: tuple[int, int]):
    """
    Loads an alpha image and makes the alpha background transparent.
    Scales the image to the given size 

    Parameters: 
        - (str) absolute_img_path: Absolute file path to the image 
        - (tuple[int, int]) size_to_scale_to: Size tuple (width, height) to scale the image to
    """
    unscaled_img = load_alpha_img(absolute_img_path)
    scaled_img = transform.scale(unscaled_img, size_to_scale_to)
    return scaled_img