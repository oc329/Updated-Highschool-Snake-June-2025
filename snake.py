import pygame
pygame.init() #Initializes all pygame classes and functions
#print(pygame.display.get_surface().get_size())
## Window display set in main doesn't set it for every file
import random 

from apple import Apple
from enums import Direction 
from screen_info import BLOCK_SIZE, GRID_TO_DISPLAY_POS, TOTAL_COLUMNS, TOTAL_ROWS





# def display(self, win: pygame.surface.Surface):
# 	x_coor, y_coor = self.calculate_grid_x_y(self.grid_pos)
# 	self.rect = pygame.Rect(x_coor, y_coor, self.width, self.height) #Updates the value of rect space's coordinates with each call 
# 	pygame.draw.rect(win, self.color,self.rect)
	


## Snake class is positioned below Snake_piece class so I can use Snake_piece instances in Snake class (can't reference classes out of order )
## (Took all my snake_piece code from main and created a class for it, since a class allows for easier functionality and readability)



# Snake is a collection of snake pieces 
class Snake(): 
	def __init__(self, starting_head_grid_pos: tuple[int, int],  starting_direction = (1,0), starting_length = 3):
		## starting num of pieces and speed multiple can be changed in instance's arguments 
		self.is_alive = True 
		self.starting_head_grid_pos = starting_head_grid_pos

		self.starting_snake_segments_grid_positions: list[tuple[int, int]] = [] 

		self.starting_length = starting_length
		self.starting_segment_grid_positions = []

		## __build starting snake has to be called after self.starting_head_pos and self.starting length are instatiated
		self.__build_starting_snake()
		
		## Applied direction starts as (0, 0) because the player hasn't applied any direction yet with arrow key input
		self.direction = self.starting_head_pos
		self.applied_direction = (0, 0)
		self.acceptable_directions = ((1, 0) or (0, 1))


	def __build_starting_snake(self):
				"""
				Sets the positions of the snake body based on the snake's head position and direction the snake is facing.
				Saves these positions after the first time
				""" 
				self.snake_head.grid_pos = self.starting_head_grid_pos
				head_x, head_y = self.starting_head_pos
				x_dir, y_dir = self.starting_head_pos

				## Calculating snake body and inserting head at front
				self.starting_snake_segments_grid_positions  = [
						(head_x - piece_i * x_dir, head_y - piece_i * y_dir)
						for piece_i in range(1, self.starting_length)
				].insert(0, self.snake_head)
				## Sets segment positions equal to a copy of starting segment positions so it doesn't modify starting
				self.segment_grid_positions = self.starting_snake_segments_grid_positions.copy()
	@property
	def direction(self):
		return self.direction
	
	@direction.setter
	def direction(self, new_direction: tuple[int, int]):
		if not isinstance(new_direction, tuple): 
			return ValueError("Should be tuple")
		if new_direction not in self.acceptable_directions:
			raise ValueError(f"Direction should be one of these: {self.acceptable_directions}")
		
	# def ensure_passed_direction_is_within_bounds(self, new_direction: tuple[int, int]):
	# 	"""
	# 	Direction should represent the column and row change. 
	# 	It should be(1, 0) or (0, 1)
 	# 	"""
	# 	if new_direction not in self.acceptable_directions:
	# 		raise ValueError(f"Direction should be one of these: {self.acceptable_directions}")
		
	def is_colliding_with_wall(self):
		"""
		Returns True if snake goes out of grid bounds, otherwise False 
		"""

		snake_head_row, snake_head_column = self.segment_grid_positions[0]

		return not(0 <= snake_head_row < TOTAL_ROWS and 0 <= snake_head_column < TOTAL_COLUMNS)
	
	def is_collidng_with_itself(self):
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
		return self.snake_head.rect.colliderect(apple_obj.rect)
	
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

	def __apply_direction_change(self):
		"""
		Apply the player's direction change to the snake.
		"""
		## The snake displayed in menu may be motionless (0, 0 in x,y directions)
		if self.applied_direction != (0, 0):
			self.direction = self.applied_direction
			self.applied_direction = (0, 0)

	def __move_snake_forward_by_one(self):
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
		for piece in self.pieces: 
			piece.display(win) #Draws the rectangle each frame for snake piece onto screen  




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
		## Used to Relocate Menu Snake in Colors Page
		## Direciton represents the axis it's along. Didn't want to have the arguments be x and y to signify axis so I chose the parameter name direction 

		self.menu_snake.snake_head.grid_pos = new_snake_head_grid_pos    #Assigns new coordinates to snake head
		piece_index = 1 ## Snake head has already been assinged coordinates 
		
		if(direction == "horizontal"): 
			while piece_index < len(self.menu_snake.pieces):
				previous_piece = self.menu_snake.pieces[piece_index - 1]
				self.menu_snake.pieces[piece_index] = (previous_piece.grid_pos[0], previous_piece.grid_pos[1] - 1 )
				piece_index += 1

		elif (direction == "vertical"):
			while piece_index < len(self.menu_snake.pieces):
				previous_piece = self.menu_snake.pieces[piece_index - 1]

				self.menu_snake.pieces[piece_index] = (previous_piece.grid_pos[0] + 1, previous_piece.grid_pos[1])
				## Adding 1 to piece's row position instead of subtracting, b/c height 0 is top of screen in computer graphics

				piece_index += 1
	
	def teleport_to_grid_pos(self, new_snake_head_grid_pos): 
		## Used to Relocate Menu Snake in Colors Page
		## Direciton represents the axis it's along. Didn't want to have the arguments be x and y to signify axis so I chose the parameter name direction 

		x_direction, y_direction = self.snake_head.move_dir
		piece_index = 1 
		self.snake_head.grid_pos = new_snake_head_grid_pos
		
		while piece_index < len(self.menu_snake.pieces):
		
		if(direction == "horizontal"): 
			while piece_index < len(self.menu_snake.pieces):
				previous_piece = self.menu_snake.pieces[piece_index - 1]
				self.menu_snake.pieces[piece_index] = (previous_piece.grid_pos[0], previous_piece.grid_pos[1] - 1 )
				piece_index += 1

		elif (direction == "vertical"):
			while piece_index < len(self.menu_snake.pieces):
				previous_piece = self.menu_snake.pieces[piece_index - 1]

				self.menu_snake.pieces[piece_index] = (previous_piece.grid_pos[0] + 1, previous_piece.grid_pos[1])
				## Adding 1 to piece's row position instead of subtracting, b/c height 0 is top of screen in computer graphics

				piece_index += 1

	def snake(self): 
		##Moves a snake across the bottom of the screen
		self.menu_snake.move()
		menu_snake_head_row, menu_snake_head_column    = self.menu_snake.snake_head.grid_pos
		 
		### Teleports snake to left side of screen when it snake_head hits right side    
		if menu_snake_head_column > TOTAL_COLUMNS:
			new_grid_pos = (menu_snake_head_row, 0)
			self.menu_snake.change_location_going_right(new_grid_pos)

		self.menu_snake.update()


	# ### Scrap Code
	# ## Checking if the move will collide with a snake piece
	# # potential_coors = ((self.snake_head.grid_pos["col"] + (self.snake_head.move_dir[0] * self.snake_head.speed, 1)), (self.snake_head.y + round(self.snake_head.move_dir[1] * self.snake_head.speed, 1)))
	# # potential_head_rect = pygame.Rect(potential_coors[0], potential_coors[1], self.snake_head.width, self.snake_head.height)
	# # Potential_head_rect is the where the snake_head's rectangle would be if the move executes. The if statement below makes sure that the new rect doesn't collide with the piece behind the snake head.

	# ## If move doesn't collide with a piece then it executes
	# # if potential_head_rect.colliderect(self.pieces[1].rect)== 0: # colliderectreturns 0 or 1. (0 means no collision)



# @property
	# def snake_head(self):
	# 	"""
	# 	Returns the first snake segment grid position in the snake
	# 	"""
	# 	return self.segment_grid_positions[0]