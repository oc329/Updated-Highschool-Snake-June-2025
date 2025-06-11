import pygame 
pygame.init()
import time

from apple import Apple
from colors import GAME_LOOP_BG_COLOR, MAIN_MENU_BG_COLOR
from event_handler import GameLoopEventHandler, MainMenuEventHamdler
from main_menu import MainMenu
from screen_info import CENTER_OF_SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT, GAME_SNAKE_STARTING_GRID_POS, MAIN_MENU_SNAKE_STARTING_GRID_POS, WINDOW
from fps_controller import FPSController
from snake import Snake
from text_settings import GAME_OVER_MSG_TEXT_SETTINGS, GAME_SCORE_TEXT_SETTINGS

class GameStateManager: 
    """
    Controls which loop the game is in. 
    """
    def __init__(self): 
        self.main_menu_event_handler = MainMenuEventHamdler()
        self.game_loop_event_handler = GameLoopEventHandler()
        self.clock = pygame.time.Clock()
        FPS = 25
        self.FPS_controller = FPSController(self.FPS)
        self.game_snake = Snake(WINDOW, GAME_SNAKE_STARTING_GRID_POS, "game")
        self.game_apple = Apple()

        self.GAME_OVER_MSG = "GAME OVER"
        self.GAME_OVER_MSG_FONT_OBJ = GAME_OVER_MSG_TEXT_SETTINGS.get_rendered_text(self.GAME_OVER_MSG)
        self.GAME_OVER_MSG_POS = (CENTER_OF_SCREEN[0] - self.GAME_OVER_MSG_FONT_OBJ.get_width(), 
                                  CENTER_OF_SCREEN[1] - self.GAME_OVER_MSG_FONT_OBJ.get_height)


    def main_menu_loop(self): 
        menu = MainMenu(WINDOW, self.game_snake) #Takes in pygame window, game_snake and title screen message
        while menu.is_running:
            if self.fps_controller.should_update_graphics_and_movement():
                WINDOW.fill(MAIN_MENU_BG_COLOR)
                
                self.main_menu_event_handler.record_input()

                if self.main_menu_event_handler.down_arrow_key_is_pressed: 
                    menu.move_down_one_box()
                elif self.main_menu_event_handler.up_arrow_key_is_pressed: 
                    menu.move_up_one_box()
                elif self.main_menu_event_handler.return_key_is_pressed:
                    menu.selected_box.action()
                elif self.main_menu_event_handler.escape_key_is_pressed:
                    menu.open_new_page(menu.active_page.outer_page)
                menu.update()
                
                pygame.display.flip()

            self.fps_controller.limit_fps()
            
    def game_loop(self):
        while self.game_snake.is_alive:
            if self.FPS_controller.should_update_graphics_and_movement():
                WINDOW.fill(GAME_LOOP_BG_COLOR)
                ### Scanning Events for Key Inputs
                self.game_loop_event_handler.record_input()
                snake_direction_tuple = self.game_loop_event_handler.direction_key_pressed().value
                if snake_direction_tuple is not None:
                    self.game_snake.change_dir(snake_direction_tuple)

                #https://www.pygame.org/docs/ref/rect.html#pygame.Rect.colliderect
                ## Checks if snake collides with apple 
                if self.game_snake.is_colliding_with_given_apple(self.game_apple):
                    self.game_apple.relocate()
                    self.snake.add_piece()

                self.game_snake.move() #Moves adds 1 column or row to the grid pos depending on the pieces' current directions 

                self.game_snake.check_for_fatal_collisions()


                ### Displaying Score to Screen (In format Score + num)
                score_msg = (
                    "Score " + str(len(self.game_snake.snake.pieces) - self.game_snake.initial_num_of_pieces)
                )  # Concatenated with + and not , b/c a "," produces the error TypeError: text must be a unicode or bytes
                score_text = GAME_SCORE_TEXT_SETTINGS.get_rendered_text(score_msg)
                score_text_pos = (SCREEN_WIDTH - score_text.get_width(), 0)

                WINDOW.blit(score_text, score_text_pos)  # Makes the text appear on screen in top right corner
                self.game_snake.display(WINDOW)
                self.game.display(WINDOW)

                pygame.display.flip()

            self.FPS_controller.limit_fps()
    
    def game_over_loop(self):

        game_over_sound_effect = pygame.mixer.Sound("super_mario_game_over.wav")
        pygame.mixer.Sound.play(game_over_sound_effect)


        ### 

        ## Measuring Time, Using the time elapsed as the while condition
        start_time = int(
            time.time()
        )  # Returns the amount of seconds since the beginning of the Unix (operating system) Jan 1970
        time_length = 8
        current_time = 0
      

        ## Game Over Text Loop 
        while (current_time - start_time) < time_length:
            WINDOW.fill(GAME_LOOP_BG_COLOR)
            WINDOW.blit(self.GAME_OVER_MSG_FONT_OBJ, self.GAME_OVER_MSG_POS)

            current_time = int(time.time())
            pygame.display.flip()

        pygame.quit()
        exit()








