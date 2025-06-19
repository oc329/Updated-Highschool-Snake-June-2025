import pygame
pygame.init() #Initializes all pygame classes and functions
#print(pygame.display.get_surface().get_size())
## Window display set in main doesn't set it for every file
import random 

from apple import Apple
from colors import ensure_is_RGB, SNAKE_STARTING_COLOR
from enums import Direction 
from screen_info import CELL_SIZE, convert_grid_pos_to_display_pos, TOTAL_COLUMNS, TOTAL_ROWS




## Snake class is positioned below Snake_piece class so I can use Snake_piece instances in Snake class (can't reference classes out of order )
## (Took all my snake_piece code from main and created a class for it, since a class allows for easier functionality and readability)



# Snake is a collection of snake pieces 
class Snake(): 
    def __init__(self, starting_head_grid_pos: tuple[int, int],  starting_direction = (1,0), starting_length = 3):
        ## starting num of pieces and speed multiple can be changed in instance's arguments 
        self.is_alive = True 
        self.starting_head_grid_pos = starting_head_grid_pos
        self.acceptable_directions = ((1, 0), (-1, 0), (0, -1), (0, 1))
        self.direction = starting_direction
        
        self.starting_length = starting_length
        self.starting_segment_grid_positions: list[tuple[int, int]] = [] 
        self.segment_grid_positions = []

        ## __build starting snake has to be called after self.starting_head_pos and self.starting length are instatiated
        self.__build_starting_snake()

        ## Applied direction starts as (0, 0) because the player hasn't applied any direction yet with arrow key input
        
        self.applied_direction = (0, 0)
        self.color = SNAKE_STARTING_COLOR
    
    def __build_starting_snake(self):
        """
        Sets the positions of the snake body based on the snake's head position and direction the snake is facing.
        Saves these positions after the first time
        """ 
        head_x, head_y = self.starting_head_grid_pos
        x_dir, y_dir = self.direction

        ## Calculating snake body and inserting head at front
        self.starting_segment_grid_positions  = [
                (head_x - piece_i * x_dir, head_y - piece_i * y_dir)
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
    
    def change_direction(self, new_direction: tuple[int, int]):
        """
        Direction should represent the column and row change. 
        It should be(1, 0) or (0, 1)
        """
        if not isinstance(new_direction, tuple): 
            return ValueError("Should be tuple")
        if new_direction not in self.acceptable_directions:
            raise ValueError(f"Direction {new_direction} should be one of these: {self.acceptable_directions}")
        
        self.direction = new_direction
                
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
        Move the snake forward by one tile.
        """
        
        ## Removing last value and shifting all values by one to left
        self.segment_grid_positions[1:] = self.segment_grid_positions[:-1]
        ## Moves snake head's position foward by one in the snake direction
        x_change, y_change = self.direction
        self.segment_grid_positions[0] = (self.segment_grid_positions[0][0] + x_change, self.segment_grid_positions[0][1] + y_change) 

    def add_end_segment(self):
        """
        Adds a snake segment to end of the snake 
        """
        ## Adds a copy of the last segment which will then be changed when snake moves in update_coordinates
        last_segment = self.segment_grid_positions[-1]
        self.segment_grid_positions.append(last_segment)

    ## Used for teleporting the snake 
    def move_to_new_pos(self, new_head_grid_pos: tuple[int, int]):
        """
        Moves the snake to the new grid position

        Parameters: 
            - (tuple[int, int]) new_head_grid_pos: The new row and column grid position in a tuple
        """
        old_head_column, old_head_row = self.segment_grid_positions[0]
        new_head_column, new_head_row = new_head_grid_pos
        self.segment_grid_positions[0] = new_head_grid_pos

        ## Moving each snake segment by getting it's old position relative to head and then subtracting that from the new head pos
        for seg_i in range(1, len(self.segment_grid_positions)):
            seg_column, seg_row = self.segment_grid_positions[seg_i]
            column_diff_to_old_head = old_head_column - seg_column
            row_diff_to_old_head = old_head_row - seg_row
            self.segment_grid_positions[seg_i] = (new_head_column - column_diff_to_old_head, new_head_row - row_diff_to_old_head)       
    
    def change_color(self, new_color: tuple[int, int, int]):
        """
        Changes the color of the snake to the new given color. 
        Raies a value error if the new color is not a RGB tuple

        Parameters: 
            (tuple[int, int, int]) new_color : RGB tuple (red, green, blue) with values btw 0 and 255
        """
        ensure_is_RGB(new_color)
        self.color = new_color
        
    def move_to_new_pos_and_change_direction(self, new_grid_position: tuple[int, int], new_direction: tuple[int, int]):
        """
        Moves the snake to the new grid position and changes the direction its going in.

        Parameters: 
            - (tuple[int, int]) new_head_grid_pos: The new row and column grid position in a tuple
            - (tuple[int, int]) new_direction: The tuple direction as (0, 1) or (1, 0)
        """
        self.move_to_new_pos(new_grid_position)
        self.direction = new_direction
    
    def reset_data(self):
        ## Returns a copy so the grid positions isn't assigned the same memory location of the starting positions which would change the starting 
        self.segment_grid_positions = self.starting_segment_grid_positions.copy()
        self.direction =  (1,0)
        self.applied_direction = (0, 0)

    def display(self, win: pygame.surface.Surface):
        """
        Displays the snake on the screen
        """
        for seg_grid_pos in self.segment_grid_positions:
            pygame.draw.rect(win, self.color, rect = (*convert_grid_pos_to_display_pos(seg_grid_pos), *CELL_SIZE))
                     
        
class MenuSnake(Snake):

    def teleport_to_other_side_of_wall(self):
        """
        Teleports the snake to the other side of the screen 
        moving in the same direction .
        """
        ## Getting the x,y of last segment before teleporting
        last_segment_x, last_segment_y = self.segment_grid_positions[-1]
        
        ## Teleporting the snake to the other side of the screen
        pos_on_other_side = (self.segment_grid_positions[0][0] % TOTAL_COLUMNS, self.segment_grid_positions[0][1] % TOTAL_ROWS)
        self.move_to_new_pos(pos_on_other_side)

        ## Number of segments in snake position (excludes snake head)
        num_segs_in_snake_body = len(self.segment_grid_positions) - 1
        ## Calculating the rect tuple of the snake body left behind (x,y is position of last segment, and width and height is size of snake body (exluding snake head))
        

    def teleport_snake(self, new_snake_head_grid_pos, direction = "horizontal"): 
        """
        Teleports the snake to the given grid position. Keeps the direction going the same
        
        """
        self.menu_snake.snake_head.grid_pos = new_snake_head_grid_pos    #Assigns new coordinates to snake head
        piece_index = 1 ## Snake head has already been assinged coordinates 
        
        if(direction == "horizontal"): 
            while piece_index < len(self.menu_snake.pieces):
                previous_piece = self.menu_snake.pieces[piece_index - 1]
                self.menu_snake.pieces[piece_index] = (previous_piece.grid_pos[0], previous_piece.grid_pos[1] - 1)
                piece_index += 1

        elif (direction == "vertical"):
            while piece_index < len(self.menu_snake.pieces):
                previous_piece = self.menu_snake.pieces[piece_index - 1]
                self.menu_snake.pieces[piece_index] = (previous_piece.grid_pos[0] + 1, previous_piece.grid_pos[1])
                ## Adding 1 to piece's row position instead of subtracting, b/c height 0 is top of screen in computer graphics
                piece_index += 1

    def move_by_1_until_wall(self): 
        """
        Moves the snake by one.
        Once it reaches the side of the screen, it teleports it to the other side. 
        Only works going right for now 
        """

        self.menu_snake.move()
        menu_snake_head_row, menu_snake_head_column    = self.menu_snake.snake_head.grid_pos
         
        ### Teleports snake to left side of screen when it snake_head hits right side    
        if menu_snake_head_column > TOTAL_COLUMNS:
            new_grid_pos = (menu_snake_head_row, 0)
            self.menu_snake.change_location_going_right(new_grid_pos)

        self.menu_snake.update()


# @property
    # def snake_head(self):
    # 	"""
    # 	Returns the first snake segment grid position in the snake
    # 	"""
    # 	return self.segment_grid_positions[0]

# def teleport_snake(self, new_snake_head_grid_pos, direction = "horizontal"): 
#         """
        
#         """
#         self.menu_snake.snake_head.grid_pos = new_snake_head_grid_pos    #Assigns new coordinates to snake head
#         piece_index = 1 ## Snake head has already been assinged coordinates 
        
#         if(direction == "horizontal"): 
#             while piece_index < len(self.menu_snake.pieces):
#                 previous_piece = self.menu_snake.pieces[piece_index - 1]
#                 self.menu_snake.pieces[piece_index] = (previous_piece.grid_pos[0], previous_piece.grid_pos[1] - 1)
#                 piece_index += 1

#         elif (direction == "vertical"):
#             while piece_index < len(self.menu_snake.pieces):
#                 previous_piece = self.menu_snake.pieces[piece_index - 1]

#                 self.menu_snake.pieces[piece_index] = (previous_piece.grid_pos[0] + 1, previous_piece.grid_pos[1])
#                 ## Adding 1 to piece's row position instead of subtracting, b/c height 0 is top of screen in computer graphics

#                 piece_index += 1