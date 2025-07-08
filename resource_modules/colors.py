WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

RED = (255, 0, 0)
ORANGE  = (255, 140, 0 )
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (75, 0, 130)
PINK = (238, 130, 238)

MAIN_MENU_BG_COLOR = BLACK
GAME_LOOP_BG_COLOR = BLACK
RAINBOW_SNAKE_COLORS = (RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK)
SNAKE_SKIN_COLORS = RAINBOW_SNAKE_COLORS
SNAKE_STARTING_COLOR = RED

ARROW_COLOR = WHITE

GAME_SCORE_FONT_COLOR = WHITE
GAME_OVER_MSG_FONT_COLOR = WHITE
MENU_TITLE_FONT_COLOR = WHITE
MENU_BOX_DEFAULT_FONT_COLOR = WHITE
MENU_BOX_HIGHLIGHTED_FONT_COLOR = YELLOW

## Trying out eval of variable name
RAINBOW_SNAKE_COLORS_NAME_TO_RGB_LOOKUP = {"RED": RED, 
                                    "ORANGE" : ORANGE, 
                                    "YELLOW" : YELLOW, 
                                    "GREEN" : GREEN,
                                    "BLUE" : BLUE, 
                                    "PURPLE" : PURPLE, 
                                    "PINK" : PINK}



def ensure_is_RGB(color_RGB: tuple[int, int, int]):
    """
    Raises a ValueError if the input is not a tuple of three integers between 0 and 255.
    """
    if not isinstance(color_RGB, tuple):
        raise ValueError("Color must be a tuple.")
    if len(color_RGB) != 3:
        raise ValueError("Color must be a tuple of three elements.")
    if not all(isinstance(value, int) for value in color_RGB):
        raise ValueError("All color values must be integers.")
    if not all(0 <= value <= 255 for value in color_RGB):
        raise ValueError("All color values must be between 0 and 255.")

# def ensure_is_RGB(color_RGB: tuple[int, int, int]):
#     match color_RGB:
#         case (int(r), int(g), int(b)) if all(0 <= v <= 255 for v in (r, g, b)):
#             return
#         case _:
#             raise ValueError("Must be a tuple of three ints between 0 and 255.")
