from os import path


def ensure_path_exists(absolute_img_path: str):
    if not (path.exists(absolute_img_path)):
        raise ValueError("The given path does not exist. Make sure it's absolute and valid")


BASE_DIR = path.dirname(path.abspath(__file__))

# Construct a path relative to the script
apple_img_absolute_file_path = path.join(BASE_DIR, 'Assets', 'Sprites', 'Apple', 'apple.png')
emulogic_absolute_file_path = path.join(BASE_DIR, 'Assets', 'Fonts', 'Emulogic.ttf')

