from pygame.surface import Surface 
import random # To relocate the apple
from typing import TYPE_CHECKING

from resource_modules.colors import WHITE
from resource_modules.file_paths import apple_img_absolute_file_path
from resource_modules.img_loader import load_img_with_white_bg_and_scale_to_size
from resource_modules.screen_info import CELL_SIZE, convert_grid_pos_to_display_pos, TOTAL_COLUMNS, TOTAL_ROWS

if TYPE_CHECKING:
	from snake_game_stuff.snake import AbstractSnake  # Import only for type hinting

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
    
    def relocate_to_legal_pos(self, snake: 'AbstractSnake', not_legal_grid_positions=()):
        """
        Teleports the apple to a random position not occupied by the snake and other specified positions.
        
        Parameters: 
            - snake (Snake): The snake. To avoid spawning the apple on it. 
            - not_legal_grid_positions (Tuple): A tuple of grid positions of where not to spawn the apple
        """
        
        random_grid_pos = self.__get_random_grid_pos()
        ## Getting another position if it relocates in snake body or stays in same position
        
        while random_grid_pos == self.grid_pos or random_grid_pos in snake.segment_grid_positions or random_grid_pos in not_legal_grid_positions:
            random_grid_pos = self.__get_random_grid_pos()

        self.change_grid_pos(random_grid_pos)
                                              
    def display(self, win: Surface):
        win.blit(self.loaded_img, self.dipslay_pos)


class AppleManager:
    def __init__(self, num_of_apples: int, game_snake:'AbstractSnake'):
        """
        Manages apples, checking for collisions with snake and teleporting the colliding apple if true
        Should call relocate_all_to_legal_positions after init
        Parameters:
        - num_of_apples (int): The number of apples to manage.
        """
        self.num_of_apples = num_of_apples
        self.APPLES_GRAPHICS_LAYER = 1
        self.apples: tuple[Apple] = tuple([Apple() for _ in range(self.num_of_apples)])
        self.colliding_apple_i: int | None = None
        self.relocate_all_to_legal_positions(game_snake)

    def relocate_all_to_legal_positions(self, snake: 'AbstractSnake'):
        """
        Teleports all apples to random legal positions.
        Makes sure the apples aren't teleported to the same spot

        Parameters:
        - snake (Snake): The snake object.
        """

        for apple_i, apple in enumerate(self.apples):
            all_previous_apple_grid_positions = tuple(a.grid_pos for a in self.apples[:apple_i])
            apple.relocate_to_legal_pos(snake, all_previous_apple_grid_positions)

    def is_colliding_with_snake_head(self, snake: 'AbstractSnake'):
        """
        Returns True if any apples are in the same position as the snake head. 
        Otherwise False. 

        Parameters:
            - snake (Snake): The snake object.

        Returns:
            - bool: True if any apples are colliding, otherwise False.
        """
        colliding_apple_i = next((apple_i for apple_i, apple in enumerate(self.apples) if snake.is_colliding_with_given_apple(apple)), None)
        if colliding_apple_i is None:
            return False
        
        self.colliding_apple_i = colliding_apple_i
        return True
    
    def relocate_colliding_apple(self, snake: 'AbstractSnake'):
        """
        Teleports the apple that is colliding with the snake.
        Makes sure it doesn't teleport to a position already ocupied by other apples.

        Parameters:
        - snake (Snake): The snake object.
        """
        colliding_apple: Apple = self.apples[self.colliding_apple_i]
        all_other_apple_positions = tuple(a.grid_pos for a in self.apples[:self.colliding_apple_i]) + tuple(a.grid_pos for a in self.apples[self.colliding_apple_i + 1:])
        colliding_apple.relocate_to_legal_pos(snake, all_other_apple_positions)
        self.colliding_apple_i = None
    
    def display(self, win: Surface):
        """
        Displays all its apples. 
        """
        for apple in self.apples: 
            apple.display(win)