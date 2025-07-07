import pygame

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 540

SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
WINDOW = pygame.display.set_mode(SCREEN_SIZE)

CENTER_OF_SCREEN_X, CENTER_OF_SCREEN_Y = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
CENTER_OF_SCREEN = (CENTER_OF_SCREEN_X, CENTER_OF_SCREEN_Y)
MIDDLE_TOP_OF_SCREEN = (CENTER_OF_SCREEN[0], 0)

TOP_LEFT_FIFTH_OF_SCREEN = (0, SCREEN_HEIGHT // 5)
TOP_MIDDLE_FIFTH_OF_SCREEN = (CENTER_OF_SCREEN[0], TOP_LEFT_FIFTH_OF_SCREEN[1])

TOP_THIRD_OF_SCREEN_Y = (SCREEN_HEIGHT // 3)
BOTTOM_THIRD_OF_SCREEN_Y = (SCREEN_HEIGHT * 2 // 3)
TOP_MIDDLE_THIRD_OF_SCREEN = (CENTER_OF_SCREEN[0], TOP_THIRD_OF_SCREEN_Y)
BOTTOM_MIDDLE_THIRD_OF_SCREEN = (CENTER_OF_SCREEN[0], BOTTOM_THIRD_OF_SCREEN_Y)

BOTTOM_RIGHT_FIFTH_OF_SCREEN = (SCREEN_WIDTH, TOP_LEFT_FIFTH_OF_SCREEN[1] * 4)
BOTTOM_MIDDLE_FIFTH_OF_SCREEN = (CENTER_OF_SCREEN[0], TOP_MIDDLE_FIFTH_OF_SCREEN[1] * 4)

## Any Magic Numbers are just what I thought seemed like a good size or pos
TOTAL_COLUMNS = 40
TOTAL_ROWS = 20
print(f"number of cells is {TOTAL_COLUMNS} * {TOTAL_ROWS} = {TOTAL_COLUMNS * TOTAL_ROWS}")
CELL_SIZE = (SCREEN_WIDTH // TOTAL_COLUMNS, SCREEN_HEIGHT // TOTAL_ROWS)
CELL_WIDTH, CELL_HEIGHT = CELL_SIZE

GAME_SNAKE_STARTING_GRID_POS  = (TOTAL_COLUMNS // 2, TOTAL_ROWS // 2)
BOTTOM_MIDDLE_OF_GRID_THAT_LOOKS_GOOD_FOR_SNAKE = (TOTAL_COLUMNS // 2, TOTAL_ROWS * 17 // 20)
MAIN_MENU_PAGE_SNAKE_STARTING_GRID_POS =  BOTTOM_MIDDLE_OF_GRID_THAT_LOOKS_GOOD_FOR_SNAKE 
MAIN_MENU_SNAKE_STARTING_GRID_POS_ON_SKINS_PAGE = (TOTAL_COLUMNS * 3 // 4 , TOTAL_ROWS // 3)

GAME_SCORE_RATIO_OF_OF_SCREEN = 36
GAME_SCORE_FONT_SIZE = (SCREEN_WIDTH + SCREEN_HEIGHT) // GAME_SCORE_RATIO_OF_OF_SCREEN
GAME_OVER_MSG_FONT_SIZE = (SCREEN_WIDTH + SCREEN_HEIGHT) // 30
MENU_TITLE_FONT_SIZE = (SCREEN_WIDTH + SCREEN_HEIGHT) // 10
ratio_of_menu_box_to_screen =  12
MENU_BOX_DEFAULT_FONT_SIZE = SCREEN_HEIGHT // ratio_of_menu_box_to_screen
ARROW_SIZE = (MENU_BOX_DEFAULT_FONT_SIZE, MENU_BOX_DEFAULT_FONT_SIZE // 3)

MENU_TITLE_CENTER_POS = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
MAIN_MENU_PAGE_TOP_LEFT_POS = (0, MENU_TITLE_FONT_SIZE + (MENU_BOX_DEFAULT_FONT_SIZE * 3 // 2))
MAIN_MENU_PAGE_BOTTOM_RIGHT_POS = (SCREEN_WIDTH, SCREEN_HEIGHT - (SCREEN_HEIGHT // 7))

BOTTOM_MIDDLE_TENTH_OF_GRID_POS = (TOTAL_COLUMNS // 2, TOTAL_ROWS // 10)

GRID_POS_TO_DISPLAY_POS = tuple([
    [(column * CELL_WIDTH, row * CELL_HEIGHT) for row in range(TOTAL_ROWS)]
    for column in range(TOTAL_COLUMNS)])

def convert_grid_pos_to_display_pos(grid_pos: tuple[int, int]):
    """
    Converts the grid position of (row_column) to a display pos of (x_coor, y_coor)

    Parameters: 
        - tuple[int, int] grid_pos: tuplle of (column, row)
    
    Returns: 
        - tuple[int, int] display_pos : tuple of (x_coor, y_coor)
    """
    return GRID_POS_TO_DISPLAY_POS[grid_pos[0]][grid_pos[1]]

def grid_pos_is_on_screen(grid_pos: tuple[int, int]):
    """
    Returns True if the grid position is on the screen. Otherwise False. 
    """
    column, row = grid_pos
    return (0 <= column < TOTAL_COLUMNS and 0 <= row < TOTAL_ROWS)

def ensure_pos_is_on_screen(pos: tuple[int, int]):
    """
    Raises ValueError if position is outside screen boundaries
     """
    x, y = pos
    if not (0 <= x <= SCREEN_WIDTH and 0 <= y <= SCREEN_HEIGHT):
        raise ValueError(f"Display position is outside the screen boundaries.\n"
                         f"Display pos: {pos}")

def ensure_grid_pos_is_on_grid(grid_pos: tuple[int, int]):
    """
    Raises an error if the given (column, row) grid position 
    isn't within the total column and row boundaries.
    """
    column, row = grid_pos
    if not (0 <= column < TOTAL_COLUMNS and 0 <= row < TOTAL_ROWS):
        raise ValueError(f"Display position is outside the grid boundaries.\n"
                         f"Grid pos: {grid_pos}\n"
                         f"Total Columns: {TOTAL_COLUMNS}, Total Rows: {TOTAL_ROWS}") 
