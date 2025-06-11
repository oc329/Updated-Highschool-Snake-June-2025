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
from text_settings import GAME_OVER_MSG_TEXT_RENDERER, GAME_OVER_MSG_TEXT_SETTINGS, GAME_SCORE_TEXT_RENDERER, GAME_SCORE_TEXT_SETINGS
from text_surface import EditableSingleLineTextSurface, SingleLineTextSurface

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

        game_score_msg = "Score 0"
        game_score_pos = SCREEN_WIDTH
        self.game_score_text_surface = EditableSingleLineTextSurface("Score 0", game_score_pos, GAME_SCORE_TEXT_SETINGS, 'end')
        
        GAME_OVER_MSG = "GAME OVER"
        self.game_over_text_surface = SingleLineTextSurface(GAME_OVER_MSG, CENTER_OF_SCREEN, GAME_OVER_MSG_TEXT_RENDERER, 'middle')

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
                    
                self.game_snake.__move_snake_forward_by_one() #Moves adds 1 column or row to the grid pos depending on the pieces' current directions 
                self.game_snake.check_for_fatal_collisions()
                
                if self.game_snake.is_colliding_with_given_apple(self.game_apple):
                    self.game_apple.relocate()
                    self.snake.add_piece()
                    updated_score_msg = (
                    "Score " + str(len(self.game_snake.total_length) - self.game_snake.starting_length)
                    ) 
                    self.game_score_text_surface.change_text(updated_score_msg)
                     
                self.game_snake.display(WINDOW)
                self.game_score_text_surface.display(WINDOW)
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








