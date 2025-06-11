import pygame

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 540
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
WINDOW = pygame.display.set_mode(SCREEN_SIZE)

CENTER_OF_SCREEN = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

## Any Magic Numbers are just what I thought seemed like a good size
TOTAL_COLUMNS = 40
TOTAL_ROWS = 20
CELL_SIZE = (SCREEN_WIDTH // TOTAL_COLUMNS, SCREEN_HEIGHT // TOTAL_ROWS)
CELL_WIDTH, CELL_SIZE = CELL_SIZE
GAME_SNAKE_STARTING_GRID_POS  = (TOTAL_ROWS // 2, TOTAL_COLUMNS // 2)
MAIN_MENU_SNAKE_STARTING_GRID_POS =  (TOTAL_ROWS // 4 * 3, TOTAL_COLUMNS // 2)
MAIN_MENU_SNAKE_STARTING_GRID_POS_ON_COLORS_PAGE = (TOTAL_ROWS // 2, TOTAL_COLUMNS  // 4 * 3)

GAME_SCORE_RATIO_OF_OF_SCREEN = 36
GAME_SCORE_FONT_SIZE = (SCREEN_WIDTH + SCREEN_HEIGHT) // GAME_SCORE_RATIO_OF_OF_SCREEN
GAME_OVER_MSG_FONT_SIZE = (SCREEN_WIDTH + SCREEN_HEIGHT) // 30
MENU_TITLE_FONT_SIZE = (SCREEN_WIDTH + SCREEN_HEIGHT) // 8
MENU_BOX_DEFAULT_FONT_SIZE = SCREEN_HEIGHT // 12

MENU_TITLE_CENTER_POS = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)


GRID_POS_TO_DISPLAY_POS = tuple([
    [(col * CELL_SIZE[0], row * CELL_SIZE[1]) for col in range(TOTAL_COLUMNS)]
    for row in range(TOTAL_ROWS)
])

def convert_grid_pos_to_display_pos(grid_pos: tuple[int, int]):
    """
    Converts the grid position of (row_column) to a display pos of (x_coor, y_coor)

    Parameters: 
        - tuple[int, int] grid_pos: tuplle of (column, row)
    
    Returns: 
        - tuple[int, int] display_pos : tuple of (x_coor, y_coor)
    """
    GRID_POS_TO_DISPLAY_POS[grid_pos[0]][grid_pos[1]]

def ensure_pos_is_on_screen(pos: tuple[int, int]):
    """
    Raises ValueError if position is outside screen boundaries
     """
    x, y = pos
    if not (0 <= x <= SCREEN_WIDTH and 0 <= y <= SCREEN_HEIGHT):
        raise ValueError("Display position is outside the screen boundaries.")
