from os import path
from pathlib import Path

def ensure_path_exists(absolute_img_path: str):
    p = Path(absolute_img_path)
    if not p.exists():
        raise ValueError(f"The given path does not exist: {absolute_img_path}")


## Setting Base Directory to one above this 
BASE_DIR = Path(path.dirname(path.abspath(__file__))).resolve().parent

def get_absolute_file_path(path_components: tuple):
    """
    Returns an absolute path to the file. 
    path_components is a list of the file names in the order of the file path. 
    Ex. Assets/Sprites/Apple/apple.png is ()'Assets', 'Sprites', 'Apple', 'apple.png')

    Raises a Value Error if the path does not exist.

    Parameters: 
        - tuple[str, ..] path_components: A tuple of all the directory names and the file name
    """
    absolute_file_path = path.join(BASE_DIR, *path_components)
    ensure_path_exists(absolute_file_path)
    return absolute_file_path
    
# Construct a path relative to the script
apple_img_absolute_file_path = get_absolute_file_path(('Assets', 'Sprites', 'Apple', 'apple.png'))
emulogic_absolute_file_path = get_absolute_file_path(('Assets', 'Fonts', 'Emulogic.ttf'))

