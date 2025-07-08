import pygame 
pygame.init()
import time

from snake_game_stuff.apple import Apple, AppleManager
from resource_modules.colors import GAME_LOOP_BG_COLOR, MAIN_MENU_BG_COLOR
from resource_modules.enums import TextSurfacePosAnchor
from core.event_handler import GameLoopEventHandler, MainMenuEventHamdler
from ui.main_menu import Menu
from resource_modules.screen_info import CENTER_OF_SCREEN, SCREEN_WIDTH, GAME_SNAKE_STARTING_GRID_POS, WINDOW
from core.fps_controller import SnakeFPSController
from snake_game_stuff.snake import GameSnake
from ui.text_settings import GAME_OVER_MSG_TEXT_RENDERER, GAME_SCORE_TEXT_RENDERER
from ui.text_surface import EditableSingleLineTextSurface, SingleLineTextSurface

class GameStateManager: 
    """
    Controls which loop the game is in. 
    """
    def __init__(self): 
        self.main_menu_event_handler = MainMenuEventHamdler()
        self.game_loop_event_handler = GameLoopEventHandler()
        self.FPS = 60
        self.fps_controller = SnakeFPSController(self.FPS)
        
        self.game_snake = GameSnake(GAME_SNAKE_STARTING_GRID_POS)
        self.game_apple = Apple()
        num_of_apples = 3
        self.apple_manager = AppleManager(num_of_apples, self.game_snake)

        game_score_pos = (SCREEN_WIDTH, 0)
        self.game_score_text_surface = EditableSingleLineTextSurface("Score 0", game_score_pos, GAME_SCORE_TEXT_RENDERER, TextSurfacePosAnchor.END)
        
        GAME_OVER_MSG = "GAME OVER"
        self.game_over_text_surface = SingleLineTextSurface(GAME_OVER_MSG, CENTER_OF_SCREEN, GAME_OVER_MSG_TEXT_RENDERER, TextSurfacePosAnchor.MIDDLE)
        self.menu = Menu(self.game_snake) #Takes in pygame window, game_snake and title screen message

    def run(self):
        """
        Runs the game by running all the loops
        """
        self.main_menu_loop()
        self.game_loop()

    def main_menu_loop(self): 
        """
        Displays the main menu. Exits when user starts game or exits the program
        """
        while self.menu.is_running:
            if self.fps_controller.should_update_graphics_and_movement():
                WINDOW.fill(MAIN_MENU_BG_COLOR)
                
                self.main_menu_event_handler.record_input()

                if self.main_menu_event_handler.down_arrow_key_is_pressed: 
                    self.menu.move_down_one_box()
                elif self.main_menu_event_handler.up_arrow_key_is_pressed: 
                    self.menu.move_up_one_box()
                elif self.main_menu_event_handler.return_key_is_pressed:
                    self.menu.click_selected_box()
                elif self.main_menu_event_handler.escape_key_is_pressed:
                    self.menu.open_outer_page()
                
                self.menu.display(WINDOW)
                pygame.display.flip()

            self.fps_controller.limit_fps()
            
    def game_loop(self):
        """
        Runs the game. Ends when the user dies
        """
        while self.game_snake.is_alive:
            if self.fps_controller.should_update_graphics_and_movement():
                WINDOW.fill(GAME_LOOP_BG_COLOR)

                ### Scanning Events for Key Inputs
                self.game_loop_event_handler.record_input()
                snake_direction = self.game_loop_event_handler.direction_key_pressed()
                if snake_direction is not None:
                    self.game_snake.change_direction(snake_direction)
                    
                self.game_snake.move_forward_by_one() #Moves adds 1 column or row to the grid pos depending on the pieces' current directions 
                self.game_snake.check_for_fatal_collisions()
                ## Exiting loop when snake dies from collisions so snake display doesn't cause errors 
                if not self.game_snake.is_alive:
                    return 
                if self.apple_manager.is_colliding_with_snake_head(self.game_snake):
                    self.apple_manager.relocate_colliding_apple(self.game_snake)
                    self.game_snake.add_end_segment()
                    updated_score_msg = (
                    "Score " + str(self.game_snake.calculate_game_score_from_length())
                    )
                    
                    self.game_score_text_surface.change_text(updated_score_msg)
                    self.fps_controller.increase_game_speed()
                    
                self.apple_manager.display(WINDOW)
                self.game_snake.display(WINDOW)
                
                self.game_score_text_surface.display(WINDOW)
                pygame.display.flip()
            self.fps_controller.limit_fps()

    def game_over_loop(self):
        game_over_sound_effect = pygame.mixer.Sound("super_mario_game_over.wav")
        pygame.mixer.Sound.play(game_over_sound_effect)

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








