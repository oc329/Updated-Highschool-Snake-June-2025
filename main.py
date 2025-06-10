import os
import pygame
import time 
pygame.mixer.init()

from apple import Apple
from colors import BLACK, WHITE
from main_menu import MainMenu
from snake import Snake



# ### Graphics, Screen and Game Loop
# clock = pygame.time.Clock()
# ## Setting Current Working Directory for Relative Image Paths 
# cwd_path = os.getcwd() 
# #Returns absolute path to cwd 

# current_file_path = os.path.dirname(os.path.realpath(__file__))
# ## An absolute path to the current working directory which is the name of the snake game folder 

# ## If current directory is not main.py's cwd already, change cwd to it
# if (cwd_path != current_file_path):
#   os.chdir(current_file_path)


# ### Keeping Consistent FPS
# #Going to use clock.tick() func to only let the snake move a certain amount of ticks since the last clock.tick() call

# ### Game Snake Instance
# snake_starting_pos = {"col":TOTAL_COLUMNS // 2, "row": TOTAL_ROWS // 2}  # Using // (Floor Division) returns int instead of float 
# ## starting position is the row and column number that the snake starts at 

# screen = pygame.display.set_mode((SNAKE_GAME_WIDTH, SNAKE_GAME_HEIGHT))

# snake = Snake(screen, snake_starting_pos, "game") # Snake takes in mandatory arguments screen object, grid position, and "game" (which grid to base x and y off of)

# screen = pygame.display.set_mode((MAIN_MENU_WIDTH, MAIN_MENU_HEIGHT))


# #Apple Instance
# apple = Apple(screen)
# apple.relocate()
# #sets it to a random x and y coor




# ### Fonts
# score_font = pygame.font.SysFont(
#     "freemono", (SNAKE_GAME_WIDTH + SNAKE_GAME_HEIGHT) // 36
# )  # size is an int not a float because // is used not / (floor vs classical division)


# menu = MainMenu(screen, snake, "SNAKE") #Takes in pygame window, game_snake and title screen message

# ## Main Menu Loop. (Runs until player pressses play)
# while  menu.menu_done == False:
# 	## User terminated program is after user presses quit box. Bool value later determines whether or not to give the user a score later in leaderboard code below game while loop

# 	screen.fill(BLACK)

# 	menu.update()
	
# 	pygame.display.flip() ## Refreshes and draws everything to the screen. Has to be below update and .fill(black) so it can draw the changes

# 	### Handling Keyboard Input From User
# 	## (Events are any recorded user Input)
# 	for event in pygame.event.get():
# 		if event.type == pygame.KEYDOWN: # (If a key is pressed)

# 			if event.key == pygame.K_DOWN:
# 				menu.move_down_one_box()
# 				#Selects the box beneath it and moves arrow

# 			elif event.key == pygame.K_UP:
# 				menu.move_up_one_box()

# 			elif event.key == pygame.K_RETURN:
# 				menu.selected_box.action()
# 				### uses the box's action to execute the cmd

# 			elif event.key == pygame.K_ESCAPE:
# 				menu.open_new_page(menu.active_page.outer_page) 
# 				## Goes back to last page 

# 		## Pygame's Manual Window Close Button
# 		elif event.type == pygame.QUIT:
# 			pygame.quit()
# 			exit()
# 			## pygame's quit type is for pygame's close window button in top right of window

# 	clock.tick(25) #Max times this loop will repeat in a second (FPS)


# screen = pygame.display.set_mode((SNAKE_GAME_WIDTH, SNAKE_GAME_HEIGHT))
# pygame.time.delay(3)


# user_quit_game = False # Tracks if User presses quit button. Is used to make sure game over text doesn't appear if user quits 

# ## Game Loop 
# while snake.is_dead == False:
# 	# graphics have to be updated every time the loop is run to constantly appear
# 	screen.fill(BLACK) 	# Makes the Entire Screen Black

# 	### Key Inputs Notes
# 	##pygame.event.get() below get's all recent events from the event queue BTS which tracks user input
# 	##Events are every input from the user like mouse movement or key presses

# 	### Scanning Events for Key Inputs
# 	for event in pygame.event.get():
# 		if event.type == pygame.KEYDOWN:
# 			snake.make_snake_head_turn_and_save_move(event)  
# 			## Changes move direction of snake head piece and then transfers the move coordinate, direction of snake before the move, and the move dir all to the 2nd snake piece's available moves, which then transfers the move to the next piece  

# 		## When the exit button in the top right is clicked, the program ends
# 		elif event.type == pygame.QUIT:
# 			pygame.quit()
# 			exit()



# 	#https://www.pygame.org/docs/ref/rect.html#pygame.Rect.colliderect
# 	## Checks if snake collides with apple 
# 	if (snake.snake_head.rect_space.colliderect(apple.rect_space)) == 1:
# 		## Pygame Method Rect.colliderect() returns 0 or 1.  Returns 1 for collding and 0 for not. 1 means the snake head's rect is colliding with the apple's rect
# 		apple.relocate()
# 		snake.add_piece()

# 	snake.check_all_piece_moves() ## Iterates through snake pieces list and checks if any pieces have reached the location of a previous turn


# 	snake.move() #Moves adds 1 column or row to the grid pos depending on the pieces' current directions 


# 	## Game Loop End Condition
# 	# Ends if snake runs into wall or self
# 	if snake.is_colliding_with_fatal():
# 		snake.is_dead = True
	

# 	### Displaying Score to Screen (In format Score + num)
# 	score_msg = (
# 	    "Score " + str(len(snake.pieces) - snake.initial_num_of_pieces)
# 	)  # Concatenated with + and not , b/c a "," produces the error TypeError: text must be a unicode or bytes
# 	score_text = pygame.font.Font.render(score_font, score_msg, True, WHITE)

# 	screen.blit(score_text,
# 	            (SNAKE_GAME_WIDTH - score_text.get_width(),
# 	             0))  # Makes the text appear on screen in top right corner
	
# 	### Drawing everything to the screen
# 	snake.update()
# 	apple.update()

# 	pygame.display.flip()
# 	## ^ .flip() Updates the screen with all of the new coordinates and drawings. (It's .display.flip() not my screen.flip() b/c there can only be one screen anyways)

# 	print(snake.pieces[-1].grid_pos)
# 	print("available moves", snake.pieces[-1].available_moves)
	
# 	clock.tick(30)  #Max amount of times this while loop will run per second



# ### Playing Game Over Sound 
# ## Notes
# ## Pygame Music Documentation Link: https://www.pygame.org/docs/ref/music.html#pygame.mixer.music.load
# ## Pygame music isn't working on both VS code and Repl so I'll use the sound effects library instead. (I'm playing sound effects not music so I should .Sound anyways)
# ## Pygame .Sound Documentation Link:
# ## https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.Sound

# #replit.audio.play_file('super_mario_game_over.wav') #replit audio packages produce sound but it cuts it off, plus I want to use pygames audio modules. Also repl restarts the program to confirm that I want audio, which is annoying

# game_over_sound_effect = pygame.mixer.Sound("super_mario_game_over.wav")
# pygame.mixer.Sound.play(game_over_sound_effect)


# ### Fonts
# ## Notes:
# ## Pygame font documentation  https://www.pygame.org/docs/ref/font.html#pygame.font.SysFont
# #print(pygame.font.get_fonts())
# #trebuchet_font = pygame.font.SysFont("trebuchetmsbold", 144) #font id, size  #String font name isn't working, since keeps on crashing. I need to use .ttf files for fonts

# ## Creating Fonts and Messages
# game_over_char_size = 32
# game_over_font = pygame.font.Font(
#     "Emulogic.ttf", game_over_char_size
# )  #32 is the size of each character. It creates a rect that fits the dimensions of the created text
# game_over_text = pygame.font.Font.render(game_over_font, "Game Over", True,
#                                          WHITE)

# #print(game_over_text.get_width(), game_over_text.get_height()) #returns 288 by 40

# ## Measuring Time, Using the time elapsed as the while condition
# start_time = int(
#     time.time()
# )  # Returns the amount of seconds since the beginning of the Unix (operating system) Jan 1970
# time_length = 8
# current_time = 0

# ## Game Over Text Loop 
# while (current_time - start_time) < time_length:
# 	screen.fill(BLACK)
# 	screen.blit(game_over_text,
# 				((SNAKE_GAME_WIDTH - game_over_text.get_width()) // 2,
# 				(SNAKE_GAME_HEIGHT - game_over_text.get_height()) // 2))

# 	current_time = int(time.time())
# 	pygame.display.flip()

# 	### Notes
# 	## // returns an rounded int while / returns a float. Floor vs classic division
# 	## After a bunch of testing, I know that the program keeps crashing from the blit (doesn't produce any errors tho) # UPDATE: I needed to fill the screen with black and then update it every pass with .flip. The crash wasn't even related to .font
# 	## The expression (Width - text_width)/2 centers the text because it's half of the difference on each side.

# pygame.quit()
# exit()











# ''' Notes and Scrap Code
# ## Need to learn .blit for poesnake skins and apple image
# ## Non image idea for a skin could just be a different random color for every snake_piece 


# ## I want to get the size of the console screen based on the user adjustment, so the user can make the field bigger or smaller but I don't know how to get the dimensions of the replit console 

# #apple_img = pygame.image.load('apple_img.jpg')
# #for piece in snake_pieces: 
#         #piece.change_dir(event.key) #Didn't change pieces individually, it changed the whole snake at once. I want the pieces to act as individual bodies and then change them one at a time each frame using indexes 

# #desired_moves  = {} 
# # dict where the tuple (x coor, y coor) is the key and the move directions that happened at those coordinates are the value
# # Desired moves is a dictionary where the coordinates of when the move occured are the keys and the move directions are the values

# #Attempted to use the undocumented pygame functions .left, .right, .top and .bottom, which measure the distance from an object to the respective side of the screen 

#   #.Left and .Right notes
#   .left should measure the distance from the left side of the rect to the left side of the screen and .right does the same for right side of the rect and right side of the screen. Not well documented tho
#   Link that mentions ^^^: 
#   https://replit.com/talk/learn/A-Starter-Guide-to-Pygame/11741
  

#   if (snake.left <= 0) or (snake.right <= 0): 
#     running = False
#   elif (snake.top <= 0) or (snake.bottom <= 0): #Both if statements do the same thing but I made it two if statements instead of one so it's easier to read
#     running = False


#    #pygame.screen.blit(blue, (player.x, player.y)
#   #.screen.blit can load in images (file_source,(x_coor, y_coor))

#   ## Attempt at changing the movement of all snake_pieces when they reach the coordinates where the move occured 


#   for snake in snake_pieces:
#     desired_moves_list = list(desired_moves.items())
#     for move in desired_moves_list:
#     #for move in desired_moves.items():
#       #print(desired_moves.items())
#       #.items returns the keys and values of a dictionary in tuples 
#       #Coordinates and Move Direction of the recorded move 
#       x_coor_of_move = move[0][0] #[0][0] b/c tuple in a tuple
#       y_coor_of_move = move[0][1]
      
#       move_dir_x = move[1][0]
#       move_dir_y = move[1][1]

#       #print(snake.x)
#       #print(snake.y)
#       #print(x_coor_of_move)
#       #print(y_coor_of_move)
      
#       if snake.x == x_coor_of_move and snake.y == y_coor_of_move: 
#         print("recorded move coor and past piece coor works")
#         snake.move_dir["x"] = move_dir_x
#         snake.move_dir["y"] = move_dir_y

#         sucessful_past_move = move
#         num_of_pieces_changed += 1 

#       if num_of_pieces_changed > len(snake_pieces) - 2: 
#         #len(snake_pieces) - 2 because -1 for height difference from index and -1 for the snake.snake_head which automatically changes directions on line 66 

#         desired_moves.pop(move[0], None) #Pops (deletes and returns) the move in the list, but if the move isn't there then it returns None. I don't think it'll ever return none but I used it just in case
#         num_of_pieces_changed = 0

#       #print(desired_move_dirs)

#   if piece_func_index == (len(snake_pieces) - 1): 
#     piece_func_index = 0
#   else: 
#     piece_func_index += 1

#   ### Put all of this fatal collision code under one method in snake that returns True or False
#   ### End Condition for Running Into Walls 
#   if snake.snake_head.x < 0 or (snake.snake_head.x + snake.snake_head.width) > screen.get_width():
#     #.x is the top left corner of the rect so I need to add the width to check for right side collisions
#     running = False

    
#   elif snake.snake_head.y < 0 or (snake.snake_head.y + snake.snake_head.height) > screen.get_height():
#     running = False 



#   ### End Condition for Running Into Self 
#   if snake.is_colliding_with_self(): #returns true or false
#     running = False

# ### All of Pygame's Accessible Dictionary Colors
#   # #from pprint import pprint
#   # #import pygame as pg
#   # #pprint(pg.color.THECOLORS)


# # ### String Split Tests 
# # test_string = "Fischer"
# # test_string_in_two = test_string.split(sep = "", maxsplit = 2)
# # print(test_string_in_two) #Doesn't split the string, I need to use splicing to split a word or string into equal parts 

# '''
# '''
# ### Attempt with music library. .Sound is better
# #pygame.mixer.music.load("super_mario_game_over.wav")
# #pygame.mixer.music.load("test_game_over.wav")  
# #pygame.mixer.music.load("trash_mp3_test.mp3")

# # ^ Kind of like opening a text file 
# # pygame.mixer.music.play() #only one music file can be played at
# # print(pygame.mixer.music.get_volume()) #returns .99 so the music is runnign but theres' no sound
# # #while ch.get_busy():
# # pygame.mixer.music.unload() #closes file 
# '''

