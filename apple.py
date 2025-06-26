from pygame.surface import Surface 

import random #To relocate the apple

from colors import WHITE
from file_paths import apple_img_absolute_file_path
from img_loader import load_img_with_white_bg_and_scale_to_size
from screen_info import CELL_SIZE, convert_grid_pos_to_display_pos, TOTAL_COLUMNS, TOTAL_ROWS
# from object import Object



class Apple: 
    def __init__(self):
        random_column, random_row = self.__get_random_grid_pos()
        self.grid_pos = self.__get_random_grid_pos()
        self.dipslay_pos = convert_grid_pos_to_display_pos(self.grid_pos)
        ## Sets apple's grid position to a random row and and column in the game grid
        self.width, self.height =  CELL_SIZE
        self.loaded_img =  load_img_with_white_bg_and_scale_to_size(apple_img_absolute_file_path, (self.width, self.height))
    
    
    def change_grid_pos(self, new_grid_pos: tuple[int, int]): 
        """
        Changes the grid pos and updates the internal display pos

        Parameters: 
            - (tuple[int, int]) new_grid_pos : The new grid pos in format of (column, row)
        """
        self.grid_pos = new_grid_pos
        self.dipslay_pos = convert_grid_pos_to_display_pos(self.grid_pos)

    def __get_random_grid_pos(self):
        """
        Returns a tuple of a random grid position

        Returns: tuple[int, int]; (random column, random row)
        """
        return (random.randint(0, TOTAL_COLUMNS - 1), random.randint(0, TOTAL_ROWS - 1)) # Minus 1 since randint upper is inclusive
    
    def relocate(self, snake):
        ## Getting Random Column and Row number
        #Places the apple at a random set of coors within the screen dimensions
        random_grid_pos = self.__get_random_grid_pos()
        ## Getting another position if it relocates in snake body or stays in same position
        while random_grid_pos == self.grid_pos or random_grid_pos in snake.segment_grid_positions:
            random_grid_pos = self.__get_random_grid_pos()
        self.change_grid_pos(random_grid_pos)

    def display(self, win: Surface):
        win.blit(self.loaded_img, self.dipslay_pos)

        