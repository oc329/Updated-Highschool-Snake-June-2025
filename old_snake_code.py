# import pygame
# pygame.init() #Initializes all pygame classes and functions
# import random 

# from apple import Apple
# from enums import Direction 
# from screen_info import CELL_SIZE, GRID_TO_DISPLAY_POS, TOTAL_COLUMNS, TOTAL_ROWS


# pygame.init()

# class Snake(ScreenObject, Updatable):
	
# 	def __init__(self, skin  = RainbowSkin, starting_head_position = CENTER_OF_GRID_POS, starting_direction = (1,0), starting_length = 3):
# 		## Snake is on the first layer 
# 		super().__init__(layer = 1)
# 		## Building Snake
# 		self.starting_head_pos = starting_head_position
# 		self.head_pos = self.starting_head_pos
# 		self.starting_direction = starting_direction
# 		self.starting_length = starting_length
# 		self.starting_segment_grid_positions = []

# 		## __build starting snake has to be called after self.starting_direction and self.starting length are instatiated
# 		self.__build_starting_snake()
		
# 		## Applied direction starts as (0, 0) because the player hasn't applied any direction yet with arrow key input
# 		self.direction = self.starting_direction
# 		self.applied_direction = (0, 0)

# 		self.skin = skin
		
# 	def __build_starting_snake(self):
# 		"""
# 		Sets the positions of the snake body based on the snake's head position and direction the snake is facing.
# 		Saves these positions after the first time
# 		""" 
# 		head_x, head_y = self.starting_head_pos
# 		x_dir, y_dir = self.starting_direction

# 		## Calculating Positions and saving it
# 		self.starting_segment_grid_positions = [
# 			(head_x - piece_i * x_dir, head_y - piece_i * y_dir)
# 			for piece_i in range(self.starting_length)
# 		]
# 		## Sets segment positions equal to a copy of starting segment positions so it doesn't modify starting
# 		self.segment_grid_positions = self.starting_segment_grid_positions.copy()

# 	## Returns True if snake goes out of screen 
# 	def is_colliding_with_wall(self):
# 		"""
# 		Returns True if snake goes out of grid bounds, otherwise False 
# 		"""
# 		return not(0 <= snake_head_row < NUM_ROWS and 0 <= snake_head_column < NUM_COLUMNS)
  
# 	def is_colliding_with(self, object_grid_pos):
# 		"""
# 		Returns true if any of the snake's segments including the head are in the 
# 		same position as the given grid position 
# 		""" 
# 		return object_grid_pos in self.segment_grid_positions 
	
# 	def is_collidng_with_itself(self):
# 		"""
# 		Returns True if the snake's head is colliding with its body
# 		"""
# 		## Checks for collision btw snake head and rest of body 
# 		return self.segment_grid_positions[0] in self.segment_grid_positions[1:]
	
# 	def head_is_colliding_with(self, object_grid_position):
# 		"""
# 		Returns True if the snake head is colliding with the object position
# 		Parameters:
# 			- object_grid_position Tuple[int, int]: The given grid position of the object to compare positions with
# 		"""
# 		return object_grid_position == self.segment_grid_positions[0]
	
# 	def head_is_colliding_with_rect(self, rect):
# 		"""
# 		Returns True if the snake is colliding with the rect.
# 		False otherwise.
# 		"""
# 		return pygame.Rect(self.segment_grid_positions[0][0] * TILE_WIDTH, self.segment_grid_positions[0][1] * TILE_HEIGHT, self.skin.segment_width, self.skin.segment_height).colliderect(rect)

# 	## Used for teleporting the snake 
# 	def move_to_new_pos(self, new_pos):
# 		## Setting local variables for easier readability
# 		## Saving old head position
# 		old_head_x, old_head_y = self.segment_grid_positions[0]
# 		## Moving snake head to new pos
# 		self.segment_grid_positions[0] = new_pos
# 		new_head_x, new_head_y = self.segment_grid_positions[0]
# 		## Moving each snake segment by getting it's old position relative to head and then subtracting that from the new head pos
# 		for seg_pos_index, seg_pos in enumerate(self.segment_grid_positions[1:], start = 1):
# 			old_x_diff_to_head = old_head_x - seg_pos[0]
# 			old_y_diff_to_head = old_head_y - seg_pos[1]
# 			new_seg_pos = (new_head_x - old_x_diff_to_head, new_head_y - old_y_diff_to_head)
# 			self.segment_grid_positions[seg_pos_index] = (new_seg_pos)
	 
# 	## Moves Snake to a new position and changes its direction 
# 	def move_to_new_pos_and_set_direction(self, new_position, new_direction):
# 		self.move_to_new_pos(new_position)
# 		self.direction = new_direction
	
# 	def new_direction_is_valid(self, new_direction):
# 		"""
# 		Returns False if new direction is in opposite direction of current direction or is the current direction, otherwise True
# 		"""
# 		opposite_of_current_x_dir, opposite_of_current_y_dir =  -self.direction[0],  -self.direction[1]
# 		return (new_direction[0] != opposite_of_current_x_dir or new_direction[1] != opposite_of_current_y_dir) and new_direction != self.direction
	
# 	def change_direction(self, new_direction: tuple[int]):
# 		"""
# 		Changes the direction that will be applied to the snake head in update_coors method. 
# 		Can only be changed once per movement refresh
# 		"""
# 		if self.applied_direction == (0,0): 
# 			self.applied_direction = new_direction

# 	def get_rect_to_clear(self):
# 		"""
# 		Returns the tile right behind the snake tail as a rect so that 
# 		so that it can be filled in with background color by the DirtyRectManager class
# 		"""
# 		## Filling in the trailing tile with background color
# 		return self.trailing_rect_to_be_cleared
	
# 	def update_rect_to_clear(self):
# 		self.trailing_rect_to_be_cleared = (
# 			self.segment_grid_positions[-1][0] * TILE_WIDTH,
# 			self.segment_grid_positions[-1][1] * TILE_HEIGHT,
# 			self.skin.segment_width,
# 			self.skin.segment_height
# 		)
	
# 	def update_rects_to_clear(self):
# 		"""
# 		Need to create something like this to clear the head. Work in Progress
# 		"""
# 		self.trailing_rect_to_be_cleared = (
# 			self.segment_grid_positions[-1][0] * TILE_WIDTH,
# 			self.segment_grid_positions[-1][1] * TILE_HEIGHT,
# 			self.skin.segment_width,
# 			self.skin.segment_height
# 		)
# 		head_rect_to_be_cleared = (
# 			self.segment_grid_positions[0][0] * TILE_WIDTH,
# 			self.segment_grid_positions[0][1] * TILE_HEIGHT,
# 			self.skin.segment_width,
# 			self.skin.segment_height
# 		)
# 		return (self.trailing_rect_to_be_cleared, head_rect_to_be_cleared)
	
# 	def __move_snake_forward_by_one(self):
# 		"""
# 		Move the snake forward by one tile.
# 		"""
# 		## Sets the rect that needs to be cleared to the tile just behind the snake (so it can remove the old segment that was there from the screen)
# 		self.update_rect_to_clear()
# 		## Removing last value and shifting all values by one to left
# 		self.segment_grid_positions[1:] = self.segment_grid_positions[:-1]
# 		## Moves snake head's position foward by one in the snake direction
# 		self.segment_grid_positions[0] = (self.segment_grid_positions[0][0] + self.direction[0], self.segment_grid_positions[0][1] + self.direction[1]) 

# 	def __apply_direction_change(self):
# 		"""
# 		Apply the player's direction change to the snake.
# 		"""
# 		if self.applied_direction != (0, 0):
# 			self.direction = self.applied_direction
# 			self.applied_direction = (0, 0)

# 	def update_coors(self):
# 		"""
# 		Changes the snake's direction if the player changed it and moves the snake forward one tile in the direction
# 		"""
# 		self.__apply_direction_change()
# 		self.__move_snake_forward_by_one()

# 	def add_end_segment(self):
# 		"""
# 		Adds a snake segment to end of the snake 
# 		"""
# 		## Adds a copy of the last segment which will then be changed when snake moves in update_coordinates
# 		last_segment = self.segment_grid_positions[-1]
# 		self.segment_grid_positions.append(last_segment)
	
# 	def get_direction(self):
# 		"""
# 		Returns the current direction of the snake as a tuple, 
# 		where the first item represents the change in x and the second 
# 		represents the change in y (for example. (1, 0) means the snake is moving right)
# 		"""
# 		return self.direction

# 	def get_num_of_segments(self):
# 		"""
# 		Returns the current number of snake segments including the head
# 		"""
# 		return len(self.segment_grid_positions)
	
# 	def reset_data(self):
# 		## Returns a copy so the grid positions isn't assigned the same memory location of the starting positions which would change the starting 
# 		self.segment_grid_positions = self.starting_segment_grid_positions.copy()
# 		self.direction =  (1,0)
# 		self.applied_direction = (0, 0)
	
# 	def display(self, win):
# 		"""
# 		Displays the snake at its location. The visuals are determined by the snake's skin
# 		"""
# 		self.skin.display(self.segment_grid_positions)

# class UncontrollableSnake(Snake):
# 	def teleport_to_other_side_of_wall(self):
# 		"""
# 		Clears the space where the snake was and 
# 		Teleports snake to oher side of screen if it's out of bounds.
# 		"""
# 		## Getting the x,y of last segment before teleporting
# 		last_segment_x, last_segment_y = self.segment_grid_positions[-1]
		
# 		## Teleporting the snake to the other side of the screen
# 		pos_on_other_side = (self.segment_grid_positions[0][0] % NUM_COLUMNS, self.segment_grid_positions[0][1] % NUM_ROWS)
# 		self.move_to_new_pos(pos_on_other_side)

# 		## Number of segments in snake position (excludes snake head)
# 		num_segs_in_snake_body = len(self.segment_grid_positions) - 1
# 		## Calculating the rect tuple of the snake body left behind (x,y is position of last segment, and width and height is size of snake body (exluding snake head))
# 		rect_of_snake_body = (last_segment_x * TILE_WIDTH, 
# 							  last_segment_y * TILE_HEIGHT, 
# 							  num_segs_in_snake_body * TILE_WIDTH, 
# 							  self.skin.segment_height) 
# 		## Posting event for dirty rect manager to clear the snake body from its previous position
# 		post_event_to_clear_rect(rect_of_snake_body)
		
		
		



# # import pygame
# # pygame.init() #Initializes all pygame classes and functions
# # #print(pygame.display.get_surface().get_size())
# # ## Window display set in main doesn't set it for every file
# # import random 

# # from apple import Apple
# # from enums import Direction 
# # from screen_info import CELL_SIZE, GRID_TO_DISPLAY_POS, TOTAL_COLUMNS, TOTAL_ROWS




# # class Snake_piece(): 
# # #Constructor Method 
# # 	def __init__(self, grid_pos, color, speed_multiple = .5):

# # 		### Dimension and Graphics Attributes
# # 		self.color = color
# # 		self.grid_pos = grid_pos

# # 		### Movement Attributes
# # 		self.move_dir = (1, 0)  #Starts moving to the right 

# # 		# self.speed_ratio = 4/537 #speed that I liked with a screen width of 537. 4 was good with the x dimesion 537 so I saved the ratio to apply it to any dimension 
# # 		self.speed_multiple = speed_multiple # above a 2 the snake can't iterate through the moves fast enough and breaks apart

		
# # 		self.available_moves = []
# # 		## available move is the list of moves that the piece in front of the current piece made
# # 		## When the user makes a move by pressing an arrow key, the snake head moves and then every subsequent piece 
# # 		## after it when they reach the same position 

# # 	### Key Input 
# # 	#Muatator method

# # 	def change_dir(self, str_direction: str): 
# # 		'''
# # 		Changes the snake's movement direction to the passed direction.
# # 		Parameters: 
# # 			- (str) str_direction: The direction a string (eg: right, left, up, down)
# # 		'''    

# # 		### Y Axis Move Direction Change
# # 		if self.move_dir[0] != 0: 
# # 			if str_direction == Direction.UP:
# # 				self.move_dir[1]  = -1 #up is negative in graphics. It's in the 4th quadrant
# # 			elif str_direction == Direction.DOWN:
# # 				self.move_dir[1] = 1

# # 		elif self.move_dir[1] != 0: 
# # 			if str_direction == Direction.LEFT:
# # 				self.move_dir[0]  = -1  #up is negative in graphics. It's in the 4th quadrant
# # 			elif str_direction == Direction.RIGHT:
# # 				self.move_dir[0] = 1
				

# # 	### Mutator Method that Adds an Inputted Move
# # 	def add_available_move(self, move): 
# # 		self.available_moves.append(move)


# # 	## Method to check if the current piece has reached the same position in the grid where the piece in front of it turned 
# # 	## Once it reaches that place it makes the move (changes move direction) and adds the move to the following snake piece's available move list
# # 	def check_and_transfer(self, next_snake_piece): 
# # 		for move in self.available_moves: 
# # 			move_pos = move[0]
# # 			#print(move[0])
# # 			dir_at_move = move[1]
# # 			#dir at move = move dir of snake head when it turned 

# # 			dir_of_move = move[2]
# # 			#dir of move is diretion of the turn that the user entered 

# # 			## Bug Snake Turning Testing with Print Statemnts
# # 			## Checks if the piece has is at the same place in grid and has the same move direction
# # 			if (self.grid_pos == move_pos and (dir_at_move[0] == self.move_dir[0] and dir_at_move[1] == self.move_dir[1])):
# # 				# Checks if the coordinates and the move direction of the piece are the same as when the move was made
				
# # 				## Making the move(turn) on current piece 
# # 				self.move_dir[0] = dir_of_move[0]
# # 				self.move_dir[1] = dir_of_move[1]
				
# # 				## Confirms that there is another snake piece after this current one (last snake piece doesn't have another piece to transfer a move to)
# # 				if next_snake_piece != None: 
# # 					# None is passed instead of a piece if snake piece is last in list 
# # 					next_snake_piece.add_available_move(move)

# # 				self.available_moves.remove(move) 




# # 	### Constantly Moves the Snake by Updating Grid Position 
# # 	def move(self): 
# # 		self.grid_pos[0] += self.move_dir[0]
# # 		self.grid_pos[1] += self.move_dir[1] 
		

# # 	def display(self, win: pygame.surface.Surface):
# # 		x_coor, y_coor = self.calculate_grid_x_y(self.grid_pos)
# # 		self.rect = pygame.Rect(x_coor, y_coor, self.width, self.height) #Updates the value of rect space's coordinates with each call 
# # 		pygame.draw.rect(win, self.color,self.rect)
		


# # ## Snake class is positioned below Snake_piece class so I can use Snake_piece instances in Snake class (can't reference classes out of order )
# # ## (Took all my snake_piece code from main and created a class for it, since a class allows for easier functionality and readability)



# # # Snake is a collection of snake pieces 
# # class Snake(): 
# # 	def __init__(self, starting_head_grid_pos: tuple[int, int], speed_multiple = 2, starting_num_of_pieces = 4):
# # 		## starting num of pieces and speed multiple can be changed in instance's arguments 
# # 		self.is_alive = True 
# # 		self.starting_head_grid_pos = starting_head_grid_pos
# # 		self.speed_multiple = speed_multiple
# # 		self.self.starting_direction = (1, 0)

# # 		self.starting_snake_segments_grid_positions = [] 
# # 		self.speed_multiple = speed_multiple #To adjust the speed of the snake pieces when I create them  

# # 		red = (255,0,0) # Color of snake head and also whole body if color pattern isn't changed   
# # 		self.snake_head = Snake_piece(starting_head_grid_pos, red, speed_multiple = self.speed_multiple) # // Floor division automatically rounds to nearest whole number and converts to int 
# # 		## I never created a self.gridpos snake_head class since they would just be the same as the snake head and would be confusing/annoying having to constantly update both variables to make sure they have the same value

# # 		# green = (0,255,0)
# # 		self.snake_colors = [red]
# # 		# Green is the default color for the whole snake. The tuple is in a list since the code has to be compatible with the rainbow color pattern which has multiple colors in a list
# # 		self.pieces = [self.snake_head]
# # 		## pieces is a list with snake_head in it because I don't want a create an empty list and append when I can do this in one line. (Code later appends snake pieces to self.pieces in while loop below)

# # 		self.initial_num_of_pieces = starting_num_of_pieces
# # 		# ^ num doesn't include the first snake piece which has the grid_pos that the rest of the snake pieces are based off of 

# # 		# (I don't have to assign var names to snake class instances b/c I can just append the instances to a list without assigning them variables)

# # 		### Creating Snake Piece Instances of Snake (Instances in list of pieces)
# # 		piece_num = 1 # it's 1 since snake_head is already created
# # 		self.current_color_index = 0  # keeps count of current index in colors list so pieces are added with the correct color
		
		
				

# # 	def __build_starting_snake(self):
# # 				"""
# # 				Sets the positions of the snake body based on the snake's head position and direction the snake is facing.
# # 				Saves these positions after the first time
# # 				""" 
# # 				self.snake_head.grid_pos = self.starting_head_grid_pos
# # 				head_x, head_y = self.starting_head_pos
# # 				x_dir, y_dir = self.starting_direction

# # 				## Calculating snake body and inserting head at front
# # 				self.starting_snake_segments_grid_positions  = [
# # 						(head_x - piece_i * x_dir, head_y - piece_i * y_dir)
# # 						for piece_i in range(1, self.starting_length)
# # 				].insert(0, self.snake_head)
# # 				## Sets segment positions equal to a copy of starting segment positions so it doesn't modify starting
# # 				self.segment_grid_positions = self.starting_snake_segments_grid_positions.copy()
# # 	@property
# # 	def snake_head(self):
# # 		"""
# # 		Returns the first snake segment grid position in the snake
# # 		"""
# # 		return self.segment_grid_positions[0]
# # 	# Method to change speed of snake
# # 	def change_speed_multiple(self, new_speed_multiple): 
# # 		for snake in self.pieces: #To change speed of menu snake specifically, or if I want to the user to be able to change the game's snake speed later on
# # 			snake.speed_multiple = new_speed_multiple
		

# # 	## Snake Methods called only in are Main_menu are: change_all colors, and change_location_going_right
# # 	## Method to change the color pattern of the snake since there are color picker settings for the user in main menu. 
# # 	## Both the snake that moves in main menu and the game snake have the same color pattern  
# # 	def change_all_colors(self, new_color_list): #For player color picker in the main menu under settings
# # 		self.snake_colors = new_color_list
# # 		piece_index = 0 #aren't attributes since I don't need to use their values outside of this function. I also dont' want to save the values in attributes since that could be confusing
# # 		colors_index = 0
# # 		while piece_index < len(self.pieces):
# # 			self.pieces[piece_index].color = self.snake_colors[colors_index] ## Changes color to the current color in colors
			
# # 			piece_index += 1 
# # 			if len(self.snake_colors) != 1:
# # 				colors_index += 1
# # 				if colors_index == (len(self.snake_colors)):
# # 					#I didn't use a while loop for the colors since I want the outer while loop to break when the desired amount of pieces are added, not when all the colors are added
# # 					colors_index = 0
# # 					#resets to beginning of snake_colors list


# # 	## Method to move snake to new location on the grid assuming it's already moving in a horizontal direction
# # 	def change_location_going_right(self, new_grid_pos: tuple[int, int]): 
# # 		#Only going to be used for the menu_snake so I don't have to check the direction of the snake before adding the pieces behind it. I'll automatically assume that the snake is going to the right, since that's the way I set up the menu snake
# # 		piece_index = 1 
# # 		self.snake_head.grid_pos = new_grid_pos 
# # 		while piece_index < self.initial_num_of_pieces:
# # 			previous_piece = self.pieces[piece_index - 1]
# # 			self.pieces[piece_index].grid_pos = (previous_piece.grid_pos[0] - 1, previous_piece.grid_pos[1])
# # 			#Adds the pieces to the left of the snake_head since the menu_snake is going to the right
# # 			piece_index += 1
		

# # 	## Returns the correct color of the new piece being added according to colors in self.snake_colors 
# # 	## Called in add_piece() method and in initalization when creating all pieces in a while loop 
# # 	def get_current_piece_color(self):
# # 		if (self.current_color_index + 1) == len(self.snake_colors):
# # 			self.current_color_index = 0
# # 		else:
# # 			self.current_color_index += 1

# # 		return self.snake_colors[self.current_color_index]


# # 	## Method adds a piece to the end of the snake's tail depending on the direction the snake is moving 
# # 	## Called when snake eats an apple 
# # 	def add_piece(self):
# # 		"""
# # 		Adds new piece behind last snake piece. Adds it accordingly based on the current 
# # 		movement direction of the last piece.
# # 		"""
# # 		last_piece = self.pieces[-1]
# # 		last_piece_dir_x, last_piece_dir_y = last_piece.move_dir

# # 		new_pos = (
# # 			last_piece.grid_pos[0] + (last_piece_dir_y if last_piece_dir_y != 0 else 0),
# # 			last_piece.grid_pos[1] + (last_piece_dir_x if last_piece_dir_x != 0 else 0)
# # 		)

# # 		new_piece = Snake_piece(self.window, new_pos, "game", self.get_current_piece_color())
# # 		new_piece.move_dir = last_piece.move_dir

# # 		self.pieces.append(new_piece)


# # 	def make_snake_head_turn_and_save_move(self, event):
# # 		snake_head_dir_at_move = (self.snake_head.move_dir[0], self.snake_head.move_dir[1])
# # 		# Saves the direction of the move so pieces after the head can make the same move while moving in same direction
		
# # 		self.snake_head.change_dir(event.key)
# # 		snake_head_dir_of_move = (self.snake_head.move_dir[0], self.snake_head.move_dir[1])
# # 		# dir_of_move is the direction of the move that was made by user.

# # 		snake_head_pos = self.snake_head.grid_pos #snake head's grid position is assigned to new variable so that the grid position
# # 		## argument passed doesn't keep on pointing to snake head's updating position (caused me a headache figuring this out)

# # 		## Checks if snake is already going in the direction of the turn (e.g if snake is going right and user hits right arrow key)
# # 		if (snake_head_dir_at_move != snake_head_dir_of_move):
# # 			self.pieces[1].add_available_move((snake_head_pos, snake_head_dir_at_move, snake_head_dir_of_move))

# # 			## grid_pos is the snake_head's position when it turned, dir_at_move is the direction snake head was going, and dir of move is the direction the snake goes in after move was made 
# # 			# Available moves is a list that that contains tuples   
# # 			## (I used tuples instead of dictionaries since I don't change the values, I just move and 
# # 			## delete them from list to list. (Tuples are immutable and more efficient))

		


# # 	def check_all_piece_moves(self):
# # 		"""
# # 		Iterates through snake pieces list and checks if any pieces have reached the location of a previous turn
# # 		"""

# # 		piece_index = 1
# # 		# ^ not 0 b/c the snake head already directly receives user input
# # 		while piece_index < len(self.pieces): 
# # 			if self.pieces[piece_index].available_moves != []:
# # 				last_index =  (len(self.pieces) - 1)
# # 				if piece_index != last_index:  
# # 					## ^ checks if current piece isn't the last snake_piece so there's no index error 
# # 					self.pieces[piece_index].check_and_transfer(self.pieces[piece_index + 1]) #transfers the available move to the next snake piece
# # 				else: 
# # 					self.pieces[piece_index].check_and_transfer(None) 
# # 					## None is entered when the piece is the tail of the snake. 
# # 					## In the method the the avaiable move is deleted and not transfered since there's no following piece to transfer it to

# # 			piece_index += 1

# # 	def is_colliding_with_given_apple(self, apple_obj: Apple):
# # 		"""
# # 		Returns True if snake's head is in the same location as the given apple. 
# # 		Otherwise False
# # 		Parameters: 
# # 			- (Apple) apple_obj: The given apple_obj to check against
# # 		"""
# # 		return self.snake_head.rect.colliderect(apple_obj.rect)

# # 	### Returns Bool for Colliding with Self  
# # 	def is_colliding_with_self(self):
# # 		## Checks if snake_head is colliding with the rest of the snake_pieces
# # 		for piece in self.pieces: 
# # 			if (piece != self.snake_head and piece != self.pieces[1])and self.snake_head.rect.colliderect(piece.rect):
# # 					return True 
# # 		return False ##if if statment is true return stops the method so any time if statement isn't fulfilled (snake_isn't colliding with self) than it returns False


# # 	### Returns True or False for if snake is colliding with wall 
# # 	def is_colliding_with_wall(self):
# # 		## This method returns True or False so the method name is framed like a boolean. Used in is_colliding_with_fatal

# # 		snake_head_row, snake_head_column = self.snake_head.grid_pos

# # 		return not(0 <= snake_head_row < TOTAL_ROWS and 0 <= snake_head_column < TOTAL_COLUMNS)

# # 	### Wall Collisions and Self Collisions Combined
# # 	def check_for_fatal_collisions(self):
# # 		"""
# # 		Checks if the snake is colliding with the wall or its self. 
# # 		If colliding, then the snake's is alive variable is set to False
# # 		"""
# # 		## Returns Bool if snake has collided with wall or is colliding self  
# # 		self.is_alive = not(self.is_colliding_with_wall() or self.is_colliding_with_self())
		

# # 	## Move() function adds 1 to each piece's row or column depending on which direction they are going 
# # 	def move(self): 
# # 		"""
# # 		Moves each piece one forward in the direction that they were moving
# # 		"""
# # 		self.game_snake.check_all_piece_moves() 
# # 		for piece in self.pieces:
# # 			piece.move() #move() func in snake piece

# # 	def display(self, win: pygame.surface.Surface):
# # 		"""
# # 		Displays the snake on the screen
# # 		"""
# # 		for piece in self.pieces: 
# # 			piece.display(win) #Draws the rectangle each frame for snake piece onto screen  




# # class GameSnake(Snake):

# # 	def teleport_snake(self, new_snake_head_grid_pos, direction = "horizontal"): 
# # 		## Used to Relocate Menu Snake in Colors Page
# # 		## Direciton represents the axis it's along. Didn't want to have the arguments be x and y to signify axis so I chose the parameter name direction 

# # 		self.menu_snake.snake_head.grid_pos = new_snake_head_grid_pos    #Assigns new coordinates to snake head
# # 		piece_index = 1 ## Snake head has already been assinged coordinates 
		
# # 		if(direction == "horizontal"): 
# # 			while piece_index < len(self.menu_snake.pieces):
# # 				previous_piece = self.menu_snake.pieces[piece_index - 1]
# # 				self.menu_snake.pieces[piece_index] = (previous_piece.grid_pos[0], previous_piece.grid_pos[1] - 1 )
# # 				piece_index += 1

# # 		elif (direction == "vertical"):
# # 			while piece_index < len(self.menu_snake.pieces):
# # 				previous_piece = self.menu_snake.pieces[piece_index - 1]

# # 				self.menu_snake.pieces[piece_index] = (previous_piece.grid_pos[0] + 1, previous_piece.grid_pos[1])
# # 				## Adding 1 to piece's row position instead of subtracting, b/c height 0 is top of screen in computer graphics

# # 				piece_index += 1
	
# # 	def teleport_to_grid_pos(self, new_snake_head_grid_pos): 
# # 		## Used to Relocate Menu Snake in Colors Page
# # 		## Direciton represents the axis it's along. Didn't want to have the arguments be x and y to signify axis so I chose the parameter name direction 

# # 		x_direction, y_direction = self.snake_head.move_dir
# # 		piece_index = 1 
# # 		self.snake_head.grid_pos = new_snake_head_grid_pos
		
# # 		while piece_index < len(self.menu_snake.pieces):
		
# # 		if(direction == "horizontal"): 
# # 			while piece_index < len(self.menu_snake.pieces):
# # 				previous_piece = self.menu_snake.pieces[piece_index - 1]
# # 				self.menu_snake.pieces[piece_index] = (previous_piece.grid_pos[0], previous_piece.grid_pos[1] - 1 )
# # 				piece_index += 1

# # 		elif (direction == "vertical"):
# # 			while piece_index < len(self.menu_snake.pieces):
# # 				previous_piece = self.menu_snake.pieces[piece_index - 1]

# # 				self.menu_snake.pieces[piece_index] = (previous_piece.grid_pos[0] + 1, previous_piece.grid_pos[1])
# # 				## Adding 1 to piece's row position instead of subtracting, b/c height 0 is top of screen in computer graphics

# # 				piece_index += 1

# # 	def snake(self): 
# # 		##Moves a snake across the bottom of the screen
# # 		self.menu_snake.move()
# # 		menu_snake_head_row, menu_snake_head_column    = self.menu_snake.snake_head.grid_pos
		 
# # 		### Teleports snake to left side of screen when it snake_head hits right side    
# # 		if menu_snake_head_column > TOTAL_COLUMNS:
# # 			new_grid_pos = (menu_snake_head_row, 0)
# # 			self.menu_snake.change_location_going_right(new_grid_pos)

# # 		self.menu_snake.update()


# # 	# ### Scrap Code
# # 	# ## Checking if the move will collide with a snake piece
# # 	# # potential_coors = ((self.snake_head.grid_pos["col"] + (self.snake_head.move_dir[0] * self.snake_head.speed, 1)), (self.snake_head.y + round(self.snake_head.move_dir[1] * self.snake_head.speed, 1)))
# # 	# # potential_head_rect = pygame.Rect(potential_coors[0], potential_coors[1], self.snake_head.width, self.snake_head.height)
# # 	# # Potential_head_rect is the where the snake_head's rectangle would be if the move executes. The if statement below makes sure that the new rect doesn't collide with the piece behind the snake head.

# # 	# ## If move doesn't collide with a piece then it executes
# # 	# # if potential_head_rect.colliderect(self.pieces[1].rect)== 0: # colliderectreturns 0 or 1. (0 means no collision)



