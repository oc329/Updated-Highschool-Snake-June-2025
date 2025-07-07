##### Organized main_menu classes into two files main_menu and components_of_menu 
#### The main menu class is the mediator and organzier of the components 
#### Menu is instantiated in main.py while the components are not

### Library Modules
import pygame
pygame.init()



### My Modules
from colors import RAINBOW_SNAKE_COLORS_NAME_TO_RGB_LOOKUP
from components_of_menu import Arrow, BaseMenuBox, MainMenuPage, Page, SettingsTransitionPage, ScreenSettingsPage, ColorSnakeSkinsSettingsPage
from enums import PageName, MenuSnakeTeleportationType
from screen_info import BOTTOM_RIGHT_FIFTH_OF_SCREEN, BOTTOM_MIDDLE_THIRD_OF_SCREEN, MAIN_MENU_PAGE_BOTTOM_RIGHT_POS, MAIN_MENU_PAGE_TOP_LEFT_POS, MAIN_MENU_PAGE_SNAKE_STARTING_GRID_POS, SCREEN_SIZE, TOP_LEFT_FIFTH_OF_SCREEN, TOP_MIDDLE_THIRD_OF_SCREEN
from skin import color_snake_skin_manager
from text_surface import HighlightableEditableSingleLineTextSurface
from snake import MenuSnake, GameSnake


class Menu: 
    ## Snake Dummy Grid Poitions b/c it gets moved to correct position within each page it appears in
    #MENU_SNAKE_DUMMY_GRID_POS = (0, 0)
    def __init__ (self, game_snake: GameSnake):
        self.is_running = True
        self.game_snake = game_snake
        self.menu_snake = MenuSnake(MAIN_MENU_PAGE_SNAKE_STARTING_GRID_POS, MenuSnakeTeleportationType.INSTANT)
        
        ##Menu snake is a snake that moves along the bottom of the home page. Spawns in the middle bottom of screen and continues indefinitely
        ##speed_multiple is different b/c I want a slightly slower snake for the menu than the game
        self.TITLE_MESSAGE = "SNAKE"

        ### Preset Sizes
        
        ## Determines the home page's y distance from title
        
        self.main_menu_page = MainMenuPage(self.TITLE_MESSAGE, self.menu_snake, self, MAIN_MENU_PAGE_TOP_LEFT_POS, MAIN_MENU_PAGE_BOTTOM_RIGHT_POS)
        self.settings_transition_page = SettingsTransitionPage(self, TOP_MIDDLE_THIRD_OF_SCREEN, BOTTOM_MIDDLE_THIRD_OF_SCREEN)
        self.screen_settings_page = ScreenSettingsPage(self, (0,0), SCREEN_SIZE)
        self.snake_colors_settings_page = ColorSnakeSkinsSettingsPage(color_snake_skin_manager, self.menu_snake, self, TOP_LEFT_FIFTH_OF_SCREEN, SCREEN_SIZE)
        
        self.active_page = self.main_menu_page

        self.page_hierarchy = {
            PageName.MAIN_MENU: 
            {
                "Page" : self.main_menu_page,
                "Children": 
                {
                    PageName.TRANSITION_TO_SETTINGS :
                    {
                        "Page": self.settings_transition_page, 
                        "Children": {
                            PageName.SNAKE_SKIN_SETTINGS :{
                            "Page": self.snake_colors_settings_page, 
                            "Children": {}
                            },
                            PageName.SCREEN_SETTINGS: {
                                "Page": self.screen_settings_page, 
                                "Children" : {}
                            }
                        }  
                    }
                }
            }
        }
        self.set_page_realtionships()
        print(self.settings_transition_page.child_pages)
        ### User Page and Box Sselection
        self.selected_box : BaseMenuBox = self.active_page.menu_boxes[0] #defined here b/c arrow needs self.selected_box

        ### Creating the Arrow Highlighter 
        space_between_arrow_and_box = self.selected_box.get_height() // 8
        self.arrow = Arrow(self, space_between_arrow_and_box) 
        ## self is this menu class #uses menu to access selected box attribute 
        ## Arrow instance to be after self.selected_box since the Arrow's ininitalization references self.selected_box and construction method __init__ doesn't search for the attribute like calling a method does
        self.highlight_selected_box()
    
    def click_selected_box(self):
        """
        Calls the on_click function of the selected box
        """
        self.selected_box.on_click()

    def open_outer_page(self):
        """
        Changes the page to the outer page of this page if there is one. 
        Otherwise does nothing.
        """
        self.change_page(self.active_page.outer_page)

    ## For transition boxes
    def change_page(self, new_page: Page): 
        """
        Sets the active page to the new passed page.

        Parameters: 
            - new_page: The new page to set as active
        """
        ## if statement is there bause main_menu_page.outer_page has a value of none 
        if new_page is None:
            return 
        
        self.selected_box.unhighlight()
        self.active_page = new_page
        self.selected_box = new_page.menu_boxes[0]
        self.highlight_selected_box() 
        self.active_page.on_enter()

    def set_page_realtionships(self):
        """
        Sets the outer and child pages of each page. Uses the recurisve set page relationship method 
        to set each page's outer and child pages based on the page_hierarchy dict
        """
        top_of_hierarchy_page_dict = self.page_hierarchy[PageName.MAIN_MENU]
        self._recursive_set_page(top_of_hierarchy_page_dict)

    def _recursive_set_page(self, current_node: dict, parent_page: Page = None):
        """
        Recursively dives through page hierarchy dict to set the child outer page relationships. 

        Parameters: 
            - (dict) current_node: The current page dict in the dictionary
            - (Page) parent_page: The parent page of this current Page
        """
        current_page: Page = current_node["Page"]
        children_dict = current_node["Children"]

        if parent_page is not None:
            current_page.set_outer_page(parent_page)

        # Prepare and set child pages
        child_pages = {
            page_name: child_data["Page"]
            for page_name, child_data in children_dict.items()
        }

        current_page.set_child_pages(child_pages)

        ## If th ere are no children pages it does nothing 
        for child_data in children_dict.values():
            self._recursive_set_page(child_data, current_page)

    ### For Color Boxes
    def change_snake_color(self, new_color):
        self.menu_snake.change_color(new_color)
        
    ### For the Play Box
    def start_game(self):
        """
        Ends the Menu loop and starts the game. Changes the game snake colors to the menu snake 
        """
        self.is_running = False
        self.game_snake.change_skin(self.menu_snake.skin)

    def unhighlight_selected_box(self):
        """
        Unhighlights the selected box. Should be called before switching boxes
        """
        self.selected_box.unhighlight()

    ### Highlighting the Selected Box 
    def highlight_selected_box(self): 
        """
        Highlights the selected box and moves the selection arrow next to it
        """
        self.selected_box.highlight()
        self.arrow.change_box(self.selected_box)

    def select_box(self, new_box_index: int): 
        """
        Selects the box at the new box index

        Parameters: 
            - (int) new_box_index: The index of the new box to select
        """
        self.unhighlight_selected_box()
        self.selected_box = self.active_page.menu_boxes[new_box_index] 
        self.highlight_selected_box()
        self.arrow.update_selected_box()

    def move_down_one_box(self):
        """
        Moves the selected box down.. 
        If it's the last box, then it does nothing. 
        """
        current_box_index = self.active_page.menu_boxes.index(self.selected_box)
        number_of_boxes = len(self.active_page.menu_boxes)
        
        if current_box_index == (number_of_boxes - 1):
            return
                    
        self.select_box(current_box_index + 1)
        
    def move_up_one_box(self):
        """
        Moves the selected box up one if it's not the first box. Otherwise does nothing.
        """
        current_box_index = self.active_page.menu_boxes.index(self.selected_box)
        
        if current_box_index == 0:
            return
                            
        self.select_box(current_box_index - 1)

    def display(self, win: pygame.surface.Surface): 
        """
        Displays the selection arrow and
        all the current page's menu boxes and additional items
        """
        self.active_page.display(win)
        self.arrow.display(win)



