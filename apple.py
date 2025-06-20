import pygame
pygame.init() 

import os
import random #To relocate the apple

from colors import WHITE
from screen_info import CELL_SIZE, convert_grid_pos_to_display_pos, TOTAL_COLUMNS, TOTAL_ROWS
# from object import Object


### Setting Current Working Directory Equal to apple.py's directory (for relative self.loaded_img path)


class Apple: 
    def __init__(self):
        random_column, random_row = self.__get_random_grid_pos()
        self.grid_pos = self.__get_random_grid_pos()
        self.dipslay_pos = convert_grid_pos_to_display_pos(self.grid_pos)
        ## Sets apple's grid position to a random row and and column in the game grid

        self.width = int(CELL_SIZE[0]) #Sets apple's size equal to size of one block in game grid
        self.height = int(CELL_SIZE[1]) 
        
        unscaled_image = pygame.image.load('apple_test2.png').convert() # Relative file path that loads properly because os code correct cwd
        unscaled_image.set_colorkey(WHITE) #Sets the white to transparent
        self.loaded_img = pygame.transform.scale(unscaled_image, (self.width, self.height)) ## scales the image to the size of a cell in the grid
    
    
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
    
    def relocate(self):
        ## Getting Random Column and Row number
        #Places the apple at a random set of coors within the screen dimensions
        random_grid_pos = self.__get_random_grid_pos()
        self.change_grid_pos(random_grid_pos)

    def display(self, win: pygame.surface.Surface):
        win.blit(self.loaded_img, self.dipslay_pos)

        