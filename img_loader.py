from pygame import image, transform, Surface
from os import listdir, path

from colors import WHITE
from screen_info import CELL_SIZE
from file_paths import get_absolute_file_path


def load_img(absolute_img_path: str) -> Surface:
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

def get_img_scaled_to_size(unscaled_img: Surface, size_to_scale_to: tuple[int, int]) -> Surface:
    """
    Returns a pygame surface of the image scaled to the given size
    
    Parameters: 
        - (Surface) img: Pygame Surface of the image
        - (tuple[int, int]) size_to_scale_to: Size tuple (width, height) to scale the image to
    """
    scaled_img = transform.scale(unscaled_img, size_to_scale_to)
    return scaled_img
    
    
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


def get_skin_name_to_head_body_images_lookup(path_components = ('Assets', 'Sprites', 'Snake')) -> dict[str, dict[str, str]]:
    """
    Scans the base directory for snake skin folders.
    Each folder must contain 'head.png' and 'body.png'.
    Returns a dict of the each folder's snake skin name
    corresponding to a dict of the unscaled head and body pygame Surfaces.

    Raises an error if there is any files or non directories with the Skin folder 
    Returns:
        dict: {
            "skin_name": {
                "head": "unscaled head image Surface",
                "body": "unscaled body image Surface"
            },
        }
    """
    snake_skins = {}
    base_path = get_absolute_file_path(path_components)
    for folder_skin_name in listdir(base_path):
        folder_path = path.join(base_path, folder_skin_name)

        if not path.isdir(folder_path):
            raise ValueError("Should be only Folders in Directory of Snake Images")
        
        head_path = path.join(folder_path, "head.png")
        body_path = path.join(folder_path, "body.png")

        if path.isfile(head_path) and path.isfile(body_path):
            head_img = get_img_scaled_to_size(load_alpha_img(head_path), CELL_SIZE).convert_alpha()
            body_img = get_img_scaled_to_size(load_alpha_img(body_path), CELL_SIZE).convert_alpha()
            snake_skins[folder_skin_name] = {
                "head": head_img,
                "body": body_img
            }
        else:
            raise ValueError(f"Warning: '{folder_skin_name}' folder missing 'head.png' or 'body.png'")

    return snake_skins
