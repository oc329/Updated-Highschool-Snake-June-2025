##### Organized main_menu classes into two files main_menu and components_of_menu 
#### The main menu class is the mediator and organzier of the components 
#### Menu is instantiated in main.py while the components are not

### Library Modules
import pygame
pygame.init()



### My Modules
from colors import RAINBOW_SNAKE_COLORS, RED, WHITE
from components_of_menu import Arrow, MainMenuPage, Page, ScreenSettingsPage, SnakeSkinsSettingsPage
from enums import PageName
from screen_info import GRID_POS_TO_DISPLAY_POS, MAIN_MENU_SNAKE_STARTING_GRID_POS, MAIN_MENU_SNAKE_STARTING_GRID_POS_ON_COLORS_PAGE, MENU_TITLE_CENTER_POS, TOTAL_COLUMNS, TOTAL_ROWS, SCREEN_WIDTH, SCREEN_HEIGHT
from text_settings import MENU_TITLE_TEXT_SETTINGS
from snake import Snake 


class Menu: 
    def __init__ (self, game_snake):
        self.is_running = False
        self.game_snake = game_snake
        self.menu_snake = Snake(self.window, MAIN_MENU_SNAKE_STARTING_GRID_POS , "menu", starting_num_of_pieces = 5)
        
        
        ##Menu snake is a snake that moves along the bottom of the home page. Spawns in the middle bottom of screen and continues indefinitely
        ##speed_multiple is different b/c I want a slightly slower snake for the menu than the game
        self.TITLE_MESSAGE = "SNAKE"

        ### Preset Sizes
        self.y_space_btw_main_menu_title_and_first_box = SCREEN_HEIGHT // 16
        ## Determines the home page's y distance from title
        
        self.main_menu_page = MainMenuPage(self, display_pos, display_pos, outer_page = None, child_pages= {})
        self.screen_settings_page = ScreenSettingsPage(self, display_pos, display_pos, outer_page = None, child_pages= {})
        self.snake_colors_settings_page = SnakeSkinsSettingsPage(display_pos, display_pos, outer_page = None, child_pages= {})
        self.active_page = self.main_menu_page
        
        self.page_hierarchy = {
            PageName.MAIN_MENU: 
            {
                "Page" : self.main_menu_page,
                "Children": {
                    PageName.SNAKE_SKIN_SETTINGS: {
                        "Page": PageName.SNAKE_SKIN_SETTINGS, 
                        "Children" : {}
                        },
                    PageName.SNAKE_SKIN_SETTINGS :{
                        "Page": self.snake_colors_settings_page, 
                        "Children": {}
                    }
                }
            }
        }
        self.set_page_relationshhups()
        ### User Page and Box Sselection
        self.selected_box = self.active_page.menu_boxes[0] #defined here b/c arrow needs self.selected_box

        ### Creating the Arrow Highlighter 
        space_between_arrow_and_box = self.play_box.width // 8
        self.arrow = Arrow(space_between_arrow_and_box) 
        ## self is this menu class #uses menu to access selected box attribute 
        ## Arrow instance to be after self.selected_box since the Arrow's ininitalization references self.selected_box and construction method __init__ doesn't search for the attribute like calling a method does
        self.highlight_selected_box()

    ## For transition boxes
    def change_page(self, new_page: 'Page'): 
        """
        Sets the active page to the new passed page.

        Parameters: 
            - new_page: The new page to set as active
        """
        if new_page is not None:
            # if statement is there bause home_page.outer_page has a value of none since the home page has not outer page doesn't have an outer page to escape to when user presses esc
            self.active_page = new_page
            self.selected_box.unhighlight()
            ## ^ so the font color of the selected_box of the previous page doesn't remain white
            self.selected_box = new_page.item_list[0]
            self.highlight_selected_box() 
            ## Changes the first box of the new_page to the selected_box and highlights it (changes it to the highlighting color and puts the arrow's position relative to it)

            # ## Brute Forcing Snake Relocation to correct spot when user opens open page or colors pages
            # if(new_page == self.colors_page):
            # 	self.relocate_menu_snake(MAIN_MENU_SNAKE_STARTING_GRID_POS_ON_COLORS_PAGE)
            # 	## Teleports snake to right side of screen so player can see the different colors on snake 
            # elif(new_page == self.home_page):
            # 	self.relocate_menu_snake(GRID_POS_TO_DISPLAY_POS)
            # 	## Teleports snake to bottom of screen to do snake animation

    def change_to_outer_page(self):
        """
        If the current page has an outer page. Changes the current page 
        to the outer page. Otherwise, does nothing.
        """
        if self.active_page.outer_page is None:
            return 
        
        self.change_page(self.active_page.outer_page)
    
    def set_page_relationshhups(self):
        """
        Sets the outer and child pages of each page. Uses the recurisve set page relationship method 
        to set each page's outer and child pages based on the page_hierarchy dict
        """
        top_of_hierarchy_page_dict = self.page_hierarchy[PageName.MAIN_MENU]
        self._recursive_set_page[top_of_hierarchy_page_dict]

    def _recursive_set_page_relationships(self, current_node: dict, parent_page: Page = None):
        current_page = current_node["page"]
        children_dict = current_node["children"]

        if parent_page is not None:
            current_page.set_outer_page(parent_page)

        # Prepare and set child pages
        child_pages = {
            page_name: child_data["page"]
            for page_name, child_data in children_dict.items()
        }

        current_page.child_pages = child_pages

        ## If th ere are no children pages it does nothing 
        for child_data in children_dict.values():
            self._recursive_set_page(child_data, current_page)
            
    

    ### For Color Boxes
    def change_both_snakes_colors(self, new_color_list):
        self.menu_snake.change_all_colors(new_color_list)
        self.game_snake.change_all_colors(new_color_list)
        
    ### For the Play Box
    def start_game(self):
        """
        Ends the Menu loop and starts the game
        """
        self.is_running = False

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
        self.selected_box = self.active_page.item_list[new_box_index] 
        self.highlight_selected_box()

    def move_down_one_box(self):
        """
        Moves the selected box down one if possible. 
        Otherwise does nothing. 
        """
        current_box_index = self.active_page.item_list.index(self.selected_box)
        number_of_boxes = len(self.active_page.item_list)
        
        if current_box_index == (number_of_boxes - 1):
            return
        self.selected_box.font_color =    self.selected_box.default_font_color 
            # A color box's default font_color is set upon defining by the passed argument and never changes 
                    
        self.select_box(current_box_index + 1)
        
    def move_up_one_box(self):
        """
        Moves the selected box up one if possible. Otherwise does nothing.
        """
        current_box_index = self.active_page.item_list.index(self.selected_box)
        
        if current_box_index == 0:
            return
        self.selected_box.font_color =    self.selected_box.default_font_color 
            # A color box's default font_color is set upon defining by the passed argument and never changes 
                    
        self.select_box(current_box_index + 1)
            

    def relocate_menu_snake(self, new_snake_head_grid_pos, direction = "horizontal"): 
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


    def snake(self): 
        ##Moves a snake across the bottom of the screen
        self.menu_snake.move()
        menu_snake_head_row, menu_snake_head_column = self.menu_snake.snake_head.grid_pos
         
        ### Teleports snake to left side of screen when it snake_head hits right side    
        if menu_snake_head_column > TOTAL_COLUMNS:
            new_grid_pos = (menu_snake_head_row, 0)
            self.menu_snake.change_location_going_right(new_grid_pos)

        self.menu_snake.update()

    def display(self): 
        ## Snake Animation for Only Home Page
        if self.active_page == self.home_page: 
            self.snake() #Animates a snake moving across the screen 

        elif self.active_page == self.colors_page: 
            self.menu_snake.update()

        ## Updating page components 
        self.arrow.update()
        self.display.display() #Updates all menu boxes that are part of the page and additonal boxes like title screen if needed
        

    




    

#### Notes and Scrapped Code 
    ## self can be taken in as an argument. #Ex is the title instance that takes in self (the menu class) as an argument
    
    ## arrow_width= self.play_box.width #so the arrow's length doesn't change with each box and instead is based on the play boxes width
    ##arrow_height = self.selected_box.height //4
    ##self.arrow    = Object(self.window, ##self.space_between_arrow, self.selected_box.y - ##self.selected_box.height//2, arrow_width, arrow_height)

    ### Code for Splitting the Message into different colored parts 
    # #while message_part_index < len(self.font_color):
    #         #beg_of_part = len(self.message) // len(self.font_color) * font_color_index 
    #         ### Splits the message into equal parts and then multiplies it by the index of the current_color.
    #         ### Algorithm above is wrong. This code just splits the message into a number of parts instead of the colors being on alternating characters so I might have to scrap it. I'm going to create an algorithm to have each char's color be based on a iteration of the color box's font_color list 
    #         #end_of_part =    len(self.message) // len(self.font_color) * (font_color_index + 1) 
#    ### Executable Commands
#         #self.action = None

#         #if self.type == "transition":
#             #pass #Couldn't have the action created in the menu box since it wouldn't have access to the menu's current active page and the next page that each transiton menu box would want to go to. Putting the action methods in the Main_menu class makes more sense since I can pass the action as the argument and can pass the desired page for transiiton boxes in that action

#         #elif self.type == "color":
#             self.menu.change_both_snakes_colors(self.font_color)

#         #elif self.type == "play":
#             #self.action = self.end_menu_loop #Even though .end_menu_loop isn't a function. I didn't call it with () b/c I want to later call .action() in main

## self.char_size= dict() ##have to declare dictionary first using dict() or {} before I can insert keys and values
     

# def position_all_boxes(self): 
#     # Home page was previously just a list, but I needed to change it to a class to organize variables with attributes
#     self.home_page.item_list[0].y = self.title.y + self.title.height + self.y_space_btw_title_and_first_box
#     self.home_page[0].x = self.home_page.item_list[0].off_center["x"]

#     index = 1
#     while index < len(self.home_page):
#         self.home_page.item_list[index].y = self.home_page.item_list[0].y + self.home_page.compacted_char_size
#         self.home_page.item_list.x =    self.home_page.x
#         index += 1 
#     self.arrow.change_box()

# self.home_page_item_boxes = []
# self.home_page_additional_boxes = []
# self.settings_page_item_boxes = []
# self.