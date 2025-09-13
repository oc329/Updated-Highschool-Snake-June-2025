import os
import glob

# Define the old and new module names (without .py extension)
old_module_name = "utils.colors"
new_module_name = "resource_modules.colors"

# Define the directory to search for Python files
# Adjust this path to your project's root or relevant directory
search_directory = os.getcwd()

# Find all Python files in the specified directory and its subdirectories
python_files = glob.glob(os.path.join(search_directory, "**", "*.py"), recursive=True)

def old_update_imports():
    have_printed_content = True
    for file_path in python_files:
        with open(file_path, 'r') as f:
            content = f.read()
        if file_path == os.path.join(search_directory, "change_module_name.py"):
            continue
        print(content)
        # if content.find(f"import pygame") != -1:
        #     print(content.find(f"from {old_module_name}"))
        updated_content = content.replace(f"import {old_module_name}.", f"import {new_module_name}.")
        updated_content = updated_content.replace(f"from {old_module_name}", f"from {new_module_name}")
        updated_content = updated_content.replace(f"import {old_module_name} as", f"import {new_module_name} as")
        updated_content = updated_content.replace(f"from {old_module_name} import", f"from {new_module_name} import")

        # Write the updated content back to the file if changes were made
        if updated_content != content:
            with open(file_path, 'w') as f:
                f.write(updated_content)
            print(f"Updated imports in: {file_path}")


old_update_imports()
# import re

# # Root directory of your project
# PROJECT_ROOT = Path(os.getcwd()).resolve()
# print("root", PROJECT_ROOT)

# # Map of old import paths to new ones (without ".py")
# IMPORT_MAP = {
#     "utils.colors": "resource_modules.colors",
#     "utils.file_paths": "resource_modules.file_paths",
#     "utils.img_loader": "resource_modules.img_loader",
#     "utils.enums": "resource_modules.enums",

#     "main_menu": "ui.main_menu",
#     "components_of_main_menu": "ui.components_of_main_menu",
#     "text_surface": "ui.text_surface",
#     "text_settings": "ui.text_settings",
    

#     "apple": "snake_game_stuff.apple",
#     "snake": "snake_game_stuff.snake",
#     "skin": "snake_game_stuff.skin",

#     "game_manager": "core.game_manager",
#     "fps_manager": "core.fps_manager",
#     "event_handler": "core.event_handler",

#     "abstract_layout_manager": "ui.layout.abstract_layout_manager",
#     "single_point_layout_manager": "ui.layout.single_point_layout_manager",
#     "two_point_layout_manager": "ui.layout.two_point_layout_manager",
#     "sector_layout": "ui.layout.sector_layout",
# }

# def replace_imports():
#     print("all files:")
#     print(*list(PROJECT_ROOT.rglob("*.py")), sep = "\n")
#     for file in PROJECT_ROOT.rglob("*.py"):
#         if file.name == "change_module_name.py":
#             continue  # skip self

#         content = file.read_text()
#         original_content = content


# import os
# import re
# from pathlib import Path
# import difflib

# PROJECT_ROOT = Path(os.getcwd()).resolve()

# IMPORT_MAP = {
#     "utils.colors": "resource_modules.colors",
#     "utils.file_paths": "resource_modules.file_paths",
#     "utils.img_loader": "resource_modules.img_loader",
#     "utils.enums": "resource_modules.enums",

#     "main_menu": "ui.main_menu",
#     "components_of_main_menu": "ui.components_of_main_menu",
#     "text_surface": "ui.text_surface",
#     "text_settings": "ui.text_settings",

#     "apple": "snake_game_stuff.apple",
#     "snake": "snake_game_stuff.snake",
#     "skin": "snake_game_stuff.skin",

#     "game_manager": "core.game_manager",
#     "fps_manager": "core.fps_manager",
#     "event_handler": "core.event_handler",

#     "abstract_layout_manager": "ui.layout.abstract_layout_manager",
#     "single_point_layout_manager": "ui.layout.single_point_layout_manager",
#     "two_point_layout_manager": "ui.layout.two_point_layout_manager",
#     "sector_layout": "ui.layout.sector_layout",
# }


# def replace_imports():
#     py_files = list(PROJECT_ROOT.rglob("*.py"))
#     for file in py_files:
#         #print(file)
#         if file.name == "change_module_name.py":
#             continue

#         content = file.read_text()
#         original = content

#         for old, new in IMPORT_MAP.items():
#             # Match both import old and import old as alias
#             content = re.sub(
#                 rf'(^|\n|\s)import\s+{re.escape(old)}(?=\s|$)',
#                 rf'\1import {new}',
#                 content
#             )

#             # Match from old import ...
#             content = re.sub(
#                 rf'(^|\n|\s)from\s+{re.escape(old)}(?=\s|\.| import)',
#                 rf'\1from {new}',
#                 content)


#         if content != original:
#             print(f"✅ Updated {file}")
#             file.write_text(content)
#         else: 
#             print("no import match")


# #replace_imports()


# import os
# from pathlib import Path

# PROJECT_ROOT = Path(os.getcwd())

# # Exact string replacements: old import path → new import path
# IMPORT_MAP_SHORT = {
#     "from resource_modules.colors": "from resource_modules.colors",
#     "from resource_modules.file_paths": "from resource_modules.file_paths",
#     "from resource_modules.img_loader": "from resource_modules.img_loader",
#     "from resource_modules.enums": "from resource_modules.enums",

#     # "from resource_modules.colors": "from resource_modules.colors",
#     # "from resource_modules.file_paths": "from resource_modules.file_paths",
#     # "from resource_modules.img_loader": "from resource_modules.img_loader",
#     # "from resource_modules.enums": "from resource_modules.enums",

#     # "import main_menu": "import ui.main_menu",
#     # "from main_menu": "from ui.main_menu",

#     # "import text_surface": "import ui.text_surface",
#     # "from text_surface": "from ui.text_surface",

#     # "import snake": "import snake_game_stuff.snake",
#     # "from snake": "from snake_game_stuff.snake",

#     # "import game_manager": "import core.game_manager",
#     # "from game_manager": "from core.game_manager",

#     # "import event_handler": "import core.event_handler",
#     # "from event_handler": "from core.event_handler",

#     # "import abstract_layout_manager": "import ui.layout.abstract_layout_manager",
#     # "from abstract_layout_manager": "from ui.layout.abstract_layout_manager",
# }
# def replace_imports_file_open():
#     for file_path in PROJECT_ROOT.rglob("*.py"):
#         if file_path.name == "change_module_name.py":
#             continue  # skip the script itself

#         with open(file_path, "r", encoding="utf-8") as f:
#             content = f.read()

#         original_content = content

#         for old, new in IMPORT_MAP_SHORT.items():
#             content = content.replace(old, new)

#         if content != original_content:
#             with open(file_path, "w", encoding="utf-8") as f:
#                 f.write(content)
#             print(f"✅ Updated imports in: {file_path}")
#         else: 
#             print("no changes")

# #replace_imports_file_open()
