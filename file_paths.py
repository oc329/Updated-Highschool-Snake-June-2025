from os import path

BASE_DIR = path.dirname(path.abspath(__file__))

# Construct a path relative to the script
apple_img_absolute_file_path = path.join(BASE_DIR, 'Assets', 'Sprites', 'Apple', 'apple.png')
emulogic_absolute_file_path = path.join(BASE_DIR, 'Assets', 'Fonts', 'Emulogic.ttf')

print(path.exists(apple_img_absolute_file_path))
print(path.exists(emulogic_absolute_file_path))