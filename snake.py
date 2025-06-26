import pygame
pygame.init() #Initializes all pygame classes and functions
## Window display set in main doesn't set it for every file
import random 

from apple import Apple
from colors import ensure_is_RGB, SNAKE_STARTING_COLOR
from enums import Direction 
from screen_info import CELL_SIZE, convert_grid_pos_to_display_pos, ensure_grid_pos_is_on_grid, TOTAL_COLUMNS, TOTAL_ROWS




## Snake class is positioned below Snake_piece class so I can use Snake_piece instances in Snake class (can't reference classes out of order )
## (Took all my snake_piece code from main and created a class for it, since a class allows for easier functionality and readability)



# Snake is a collection of snake pieces 
class Snake(): 
    def __init__(self, starting_head_grid_pos: tuple[int, int],  starting_direction = Direction.RIGHT.value, starting_length = 5):
        ## starting num of pieces and speed multiple can be changed in instance's arguments 
        self.is_alive = True 
        self.starting_head_grid_pos = starting_head_grid_pos
        self.direction = starting_direction
        
        self.starting_length = starting_length
        self.starting_segment_grid_positions: list[tuple[int, int]] = [] 
        self.segment_grid_positions = []

        ## __build starting snake has to be called after self.starting_head_pos and self.starting length are instatiated
        self.__build_starting_snake()
        
        self.color = SNAKE_STARTING_COLOR
    
    def __build_starting_snake(self):
        """
        Sets the positions of the snake body based on the snake's head position and direction the snake is facing.
        Saves these positions after the first time
        """ 
        head_column, head_row = self.starting_head_grid_pos
        column_offset, row_offset = self.direction

        ## Calculating snake body and inserting head at front
        self.starting_segment_grid_positions  = [
                (head_column - piece_i * column_offset, head_row - piece_i * row_offset)
                for piece_i in range(0, self.starting_length)
        ]
        ## Sets segment positions equal to a copy of starting segment positions so it doesn't modify starting
        self.segment_grid_positions = self.starting_segment_grid_positions.copy()
    
    @property
    def total_length(self):
        """
        Returns the total number of snake segments
        """
        return len(self.segment_grid_positions)
    
    @staticmethod
    def ensure_new_direciton_is_valid(new_direction: Direction):
        """
        Raises a value error if
        the new direction isn't a Direction Enum.
        """
        if not isinstance(new_direction, Direction):
            return ValueError("Should be valid Direction Enum")
        
    def change_direction(self, new_direction_enum: Direction):
        """
        Direction should represent the column and row change. 
        It should be one of the Direction Enums: (1, 0), (-1, 0), (0, -1), (0, 1).
        Only changes direction if the new 
        direction isn't in the same as or the opposite of the old direction.
        """
        self.ensure_new_direciton_is_valid(new_direction_enum)
        
        old_column_direction, old_row_direction = self.direction
        new_column_direction, new_row_direction = new_direction_enum.value
        
        ## Not changing direction if it's the same or in the opposite dir (not possible in snake)
        if old_column_direction == abs(new_column_direction) or old_row_direction == abs(new_row_direction):
            return
        self.direction = (new_direction_enum.value)
                
    def is_colliding_with_wall(self):
        """
        Returns True if snake goes out of grid bounds, otherwise False 
        """
        snake_head_column, snake_head_row = self.segment_grid_positions[0]

        return not(0 <= snake_head_column < TOTAL_COLUMNS and 0 <= snake_head_row < TOTAL_ROWS)
    
    def is_colliding_with_self(self):
        """
        Returns True if the snake's head is colliding with its body
        """
        ## Checks for collision btw snake head and rest of body 
        return self.segment_grid_positions[0] in self.segment_grid_positions[1:]
    
    def is_colliding_with_given_apple(self, apple_obj: Apple):
        """
        Returns True if snake's head is in the same location as the given apple. 
        Otherwise False
        Parameters: 
            - (Apple) apple_obj: The given apple_obj to check against
        """
        return self.segment_grid_positions[0] == apple_obj.grid_pos
    
    ### Wall Collisions and Self Collisions Combined
    def check_for_fatal_collisions(self):
        """
        Checks if the snake is colliding with the wall or its self. 
        If colliding, then the snake's is alive variable is set to False

        Returns: 
            - Returns False if colliding with self or wall, otherwise True
        """
        ## Returns Bool if snake has collided with wall or is colliding self  
        self.is_alive = not(self.is_colliding_with_wall() or self.is_colliding_with_self())

    def move_forward_by_one(self):
        """
        Move the snake forward by one tile in the current direction.
        """
        ## Removing last value and shifting all values by one to left
        self.segment_grid_positions[1:] = self.segment_grid_positions[:-1]
        ## Moves snake head's position foward by one in the snake direction
        column_change, row_change = self.direction
        self.segment_grid_positions[0] = (self.segment_grid_positions[0][0] + column_change, self.segment_grid_positions[0][1] + row_change) 

    def add_end_segment(self):
        """
        Adds a snake segment to end of the snake 
        """
        ## Adds a copy of the last segment which will then be changed when snake moves in update_coordinates
        last_segment = self.segment_grid_positions[-1]
        self.segment_grid_positions.append(last_segment)   
    
    def change_color(self, new_color: tuple[int, int, int]):
        """
        Changes the color of the snake to the new given color. 
        Raies a value error if the new color is not a RGB tuple

        Parameters: 
            (tuple[int, int, int]) new_color : RGB tuple (red, green, blue) with values btw 0 and 255
        """
        ensure_is_RGB(new_color)
        self.color = new_color
    
    def reset_data(self):
        ## Returns a copy so the grid positions isn't assigned the same memory location of the starting positions which would change the starting 
        self.segment_grid_positions = self.starting_segment_grid_positions.copy()
        self.direction =  Direction.RIGHT

    def display(self, win: pygame.surface.Surface):
        """
        Displays the snake on the screen
        """
        for seg_grid_pos in self.segment_grid_positions:
            if not (0 <= seg_grid_pos[0] < TOTAL_COLUMNS and 0 <= seg_grid_pos[1] < TOTAL_ROWS):
                continue  # Skip drawing off-screen segments
            pygame.draw.rect(win, self.color, rect = (*convert_grid_pos_to_display_pos(seg_grid_pos), *CELL_SIZE))
                     
        
class MenuSnake(Snake):

    def change_pos(self, new_snake_head_grid_pos: tuple[int, int]): 
        """
        Teleports the snake to the given grid position. Keeps the direction going the same
        
        """
        self.segment_grid_positions[0] = new_snake_head_grid_pos    #Assigns new coordinates to snake head
        
        ## Helps positiion the snake body behind the snake
        column_offset, row_offset = (self.direction[0], self.direction[1])

        
        ## Snake head has already been assinged coordinates 
        for i in range(1, len(self.segment_grid_positions)):
            prev_x, prev_y = self.segment_grid_positions[i - 1]
            new_seg_pos = (prev_x - column_offset, prev_y - row_offset)
            self.segment_grid_positions[i] = new_seg_pos

    def move_forward_by_one_until_instant_teleport_at_walll(self):
        """
        Move the snake forward by one tile in the current direction.
        Once the final piece reaches the wall that it's heading torwards. 
        It teleports the snake head with 
        the rest of the body off screen to the opposite wall.
        """
        self.move_forward_by_one()
        last_piece_column, last_piece_row  = self.segment_grid_positions[-1]        
        
        ## Checks for the corresponding wall at the end of each direction and teleports snake to the opposite side
        new_grid_pos = None
        match self.direction:
            case Direction.RIGHT.value:
                if last_piece_column >= TOTAL_COLUMNS:
                    new_grid_pos = (0, last_piece_row)
            case Direction.LEFT.value:
                if last_piece_column < 0:
                    new_grid_pos = (TOTAL_COLUMNS - 1, last_piece_row)
            case Direction.UP.value:
                ## Y is in 4th quadrant for graphics
                if last_piece_row < 0:
                    new_grid_pos = (last_piece_column, TOTAL_ROWS - 1)
            case Direction.DOWN.value:
                if last_piece_row >= TOTAL_ROWS:
                    new_grid_pos = (last_piece_column, 0)
            case _: 
                raise ValueError("Not correct valid Direction in snake."
                                 f"Snake direction: {self.direction}")
        
        if new_grid_pos is not None:
            self.change_pos(new_grid_pos)

    def move_forward_by_one_until_wrapping_at_wall(self):
        """
        Move the snake forward by one tile in the current direction,
        wrapping around the screen edges.
        """
        column_offset, row_offset = self.direction
        new_head_column = (self.segment_grid_positions[0][0] + column_offset) % TOTAL_COLUMNS
        new_head_row = (self.segment_grid_positions[0][1] + row_offset) % TOTAL_ROWS

        # Shift the body
        self.segment_grid_positions[1:] = self.segment_grid_positions[:-1]
        self.segment_grid_positions[0] = (new_head_column, new_head_row)


    def move_forward_by_one_until_wall(self): 
        """
        Moves theforward snake by one.
        Once snake reaches wall, teleports the snake to the opposite side (so right to left wall, top to bottom, etc.)
        Checks for the wall based on the snake's direction
        """
        self.move_forward_by_one_until_instant_teleport_at_walll()
        #self.move_forward_by_one_until_wrapping_at_wall()

    def move_to_new_pos_and_change_to_any_direction(self, new_grid_position: tuple[int, int], new_direction: Direction):
        """
        Moves the snake to the new grid position and changes the direction. 
        Raises error if the grid position isn't on the grid or if the direction isn't a Direction Enum
        Direction can be any Direction including the same or opposite of the current direction

        Parameters: 
            - (tuple[int, int]) new_head_grid_pos: The new row and column grid position in a tuple
            - (Direction Enum which is tuple[int, int]) new_direction: The new Direction. One of these: ((0, 1), (0, -1), (-1, 0), (1, 0))
        """
        self.ensure_new_direciton_is_valid(new_direction)
        ensure_grid_pos_is_on_grid(new_grid_position)
        ## Direction has to be changed first so the snake body can be positioned behind the head correctly when moved
        self.direction = new_direction.value
        self.change_pos(new_grid_position)
        
    def transfer_colors_to_other_snake(self, other_snake: Snake):
        """
        Transfers the color(s) of this snake to the other snake object
        """
        pass