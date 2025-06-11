import pygame
pygame.init() 

import os
import random #To relocate the apple

from screen_info import BLOCK_SIZE, grid_pos_to_display_pos_lookup, TOTAL_COLUMNS, TOTAL_ROWS
# from object import Object


### Setting Current Working Directory Equal to apple.py's directory (for relative self.loaded_img path)


class Apple(): 
	def __init__(self):
		random_column, random_row = self.__get_random_grid_pos()
		self.grid_pos = (random_column, random_row)
		## Sets apple's grid position to a random row and and column in the game grid

		self.width = int(BLOCK_SIZE[0]) #Sets apple's size equal to size of one block in game grid
		self.height = int(BLOCK_SIZE[1]) 


		### Dimensions
		# super().__init__(parent_screen, x_coor, y_coor, width, height)
		#Since I use the attributes x, y, width and height in both the apple and snake piece classes, I made an object class that they both inherit
		
		
		#self.loaded_img = pygame.image.load('apple_img.jpg')
		self.loaded_img = pygame.image.load('apple_test2.png') # Relative file path that loads properly because os code correct cwd

		self.loaded_img = pygame.transform.scale(self.loaded_img, (self.width, self.height)) #scales the image to a 16 by 16 square
	
	def __get_random_grid_pos(self):
		"""
		Returns a tuple of a random grid position

		Returns: tuple[int, int]; (random column, random row)
		"""
		return (random.randint(0, TOTAL_COLUMNS - 1), random.randint(0, TOTAL_ROWS - 1)) # Minus 1 since randint upper is inclusive
	def relocate(self):
		## Getting Random Column and Row number
		#Places the apple at a random set of coors within the screen dimensions

		self.grid_pos = self.__get_random_grid_pos()
		x_coor, y_coor = grid_pos_to_display_pos_lookup(self.grid_pos)
		
	def display(self, win: pygame.surface.Surface):
		win.blit(self.loaded_img, self.rect)


		