from abc import ABC, abstractmethod
from enum import Enum
import pygame
from typing import TYPE_CHECKING
pygame.init()

from colors import ARROW_COLOR, MENU_BOX_COLOR, RAINBOW_SNAKE_COLORS
from enums import PageName
from event_handler import quit_program
from screen_info import CENTER_OF_SCREEN, MENU_BOX_DEFAULT_FONT_SIZE, MENU_TITLE_CENTER_POS
from snake import Snake
from text_settings import BaseTextRenderer, MENU_BOX_DEFAULT_COLOR_TEXT_RENDERER, MENU_BOX_HIGHLIGHTED_COLOR_TEXT_RENDERER, MENU_BOX_TEXT_SETTINGS, MENU_TITLE_TEXT_RENDERER, RAINBOW_MENU_BOX_TEXT_RENDERER, SingleLineTextSurface, TextRendererWithSingleColor, TextRendererWithMultiColors
from text_surface import HighlightableSingleLineTextSurface

if TYPE_CHECKING:
    from main_menu import Menu  # Import only for type hinting


    

class Page(ABC):
	def __init__(self, menu: Menu, outer_page = None, child_pages = None):
		## Later defined using set_outer_page method which is called in main
		## The outer page of a page is reliant on other pages so I don't want to have to define the pages in the order that they rely on pages so I'm using a method to assign a page to the page's outer_page atribtue after initialization
		self.menu = menu
		
		self.outer_page = outer_page
		self.child_pages: dict[str : Page] = child_pages if child_pages is not None else {}
		self.menu_boxes: list[BaseMenuBox] = []
		self.highlighted_menu_box_text_renderer = MENU_BOX_HIGHLIGHTED_COLOR_TEXT_RENDERER

	def create_boxes(self):
		"""
		Method that creates all the Menuboxes attributes.
		Should be called in __init__
		"""
		raise NotImplementedError()

	def add_child_page(self, child_page_name: str, child_page: Page):
		"""
		Adds a child page to this page's child pages
		"""
		self.child_pages[child_page_name] = child_page

	def set_outer_page(self, outer_page):
		"""
		Sets this page's outerpage
		"""
		self.outer_page = outer_page

	def display(self):
		#Updates all of the item_boxes as well as additional boxes
		for box in self.item_list:
			box.update()
		for box in self.additional_boxes:
			box.update() #If it's empty, iterating through an empty list won't run anything since index is already equal to length

class PageWithBoxesCompactedIntoSector(Page):
	"""
	Subclass of Page. Has methods and functionality to display 
	the menu boxes into a vertical list between the passed start and end pos. 

	"""
	def __init__(self, top_left_item_start_pos, bottom_left_item_start_pos, menu: Menu, outer_page = None, child_pages: list[Page] = None): 
		super().__init__(menu: Menu, outer_page = None, child_pages: list[Page] = None)
		self.longest_message_length: int | None = None
		self.space_btw_boxes = MENU_BOX_TEXT_SETTINGS.font.get_height()
		
	def set_item_list_compact_and_set_boxes_page(self):
		for item_box in self.item_list:
				item_box.set_page(self) ## takes in page, which is self, and sets the box's page attribute = to self (for transition menu boxes, which transition between pages with an outer page and transition page that the transition_box changes to )

		self.compact_items_into_sector()

	def compact_items_into_sector(self):
		## Unlike the unchanegable sequential order of attributes in the contructor method __init__, methods can be called out of order (It's still good to set attributes in main to None so there isn't any attribute not found in other types of menu boxes that don't have that attribute from a method)

		self.item_list[0].x, self.item_list[0].y, = self.x, self.y
		
		self.compacted_char_size = (self.height / len(self.item_list))
		## Sets a character size equal to the page's y dimsension divided by the length of list and then later in the while loop sets the character sizes of the page's item boxes equal to that size

		self.item_list[0].char_size = self.compacted_char_size

		self.longest_message_length = len(self.item_list[0].message)

		## The longest message is initally assinged to the first item box in the list's message length and in the while loop if another box's message is longer it assigns that message's length to self.longest_message (Longest_message is used for the page's width)

		item_index = 1
		while item_index < len(self.item_list):
				##similar to snake piece creation from snake_pieces. I set the coors and attributes of the first item in list and then base every item off of the previous item
				## (changes the item_boxes character size to the compacted char size created in __init__)
				self.item_list[item_index].char_size = self.compacted_char_size

				self.item_list[item_index].x = self.item_list[item_index - 1].x
				self.item_list[item_index].y = self.item_list[item_index -1].y + self.item_list[item_index - 1].height

				 ## each item box's y coor's are based on the previous box

				if len(self.item_list[item_index].message) > self.longest_message_length:
					self.longest_message_length = len(self.item_list[item_index].message)

				item_index += 1

		self.width = (self.longest_message_length * self.compacted_char_size)
		## Planning to potentially use width to set items into a horizontal sector for dimension_boxes

	def position_items_in_center(self):


		self.width = self.window.get_width()
		## Messages can go to the end of the page

		## self.height equals the page's passed arguments starting_y - end_y
		## The Page's dimension width is = to the width of the longest item box in self.item_box_list

		self.x, self.y  = (CENTER_OF_SCREEN[0] - self.width // 2, CENTER_OF_SCREEN[1] - self.height // 2)
		## Pos is down so subraction moves y attribute up
		## y is now half the height of item list above the screen's y center


		self.compact_items_into_sector()
		### Organizes the items in item list into the new
class MainMenuPage(Page):
	def __init__(self, game_title: str, menu: Menu, top_left_item_start_pos, bottom_left_item_start_pos, outer_page = None, child_pages: dict[str: Page] = None):
		super().__init__(menu, top_left_item_start_pos, bottom_left_item_start_pos, outer_page, child_pages)
		self.GAME_TITLE = game_title
		self.title_text_surface: SingleLineTextSurface = SingleLineTextSurface(self, game_title, CENTER_OF_SCREEN, MENU_TITLE_TEXT_RENDERER, pos_is_centered_on_middle = True)

	### Settings Page Boxes
	def create_boxes(self):
		play_box_x, play_box_y = (CENTER_OF_SCREEN, self.title.y + self.title.height + self.y_space_btw_title_and_first_box)
		self.play_box = PlayMenuBox(self, CENTER_OF_SCREEN, "Play", MENU_BOX_DEFAULT_COLOR_TEXT_RENDERER, MENU_BOX_HIGHLIGHTED_COLOR_TEXT_RENDERER)
		self.color_page_transition_box = TransitionMenuBox(PageName.SNAKE_SKIN_SETTINGS, self, CENTER_OF_SCREEN, "SNAKE COLORS", MENU_BOX_DEFAULT_COLOR_TEXT_RENDERER, MENU_BOX_HIGHLIGHTED_COLOR_TEXT_RENDERER)
		self.screen_page_transition_box = TransitionMenuBox(PageName.SCREEN_SETTINGS, self, CENTER_OF_SCREEN, "SCREEN DIMENSIONS", MENU_BOX_DEFAULT_COLOR_TEXT_RENDERER, MENU_BOX_HIGHLIGHTED_COLOR_TEXT_RENDERER)
		self.quit_box = QuitProgramMenuBox(self, CENTER_OF_SCREEN, "QUIT", MENU_BOX_DEFAULT_COLOR_TEXT_RENDERER, MENU_BOX_HIGHLIGHTED_COLOR_TEXT_RENDERER)
		self.menu_boxes = [self.play_box, self.color_page_transition_box, self.screen_page_transition_box, self.quit_box]

	def display(self, win: pygame.surface.Surface):
		"""
		Displays all the Game Title and all Menu boxes 
		"""
		for menu_box in self.menu_boxes: 
			menu_box.display(win)

class SnakeSkinsSettingsPage(Page):
	def __init__(self, colors: dict[str : tuple[int, int, int]], snake_to_edit: Snake, menu: Menu, top_left_item_start_pos, bottom_left_item_start_pos, outer_page = None, child_pages: dict[str: Page] = None):
		super().__init__()
		self.colors = colors
		self.snake_to_edit = snake_to_edit
		
	def create_boxes(self):
		rainbow_Menu_box = SettingsMenuBox

		for color_name, color_rgb in self.colors:
			text = color_name
			default_text_renderer = TextRendererWithSingleColor(MENU_BOX_TEXT_SETTINGS, color_rgb)
			highlighted_text_renderer = TextRendererWithSingleColor(MENU_BOX_TEXT_SETTINGS, color_rgb)
			self.menu_boxes.append(SettingsMenuBox(self.snake_to_edit, color_rgb, self, CENTER_OF_SCREEN, text, default_text_renderer, highlighted_text_renderer))
		## Adding Rainbow Menu Box
		rainbow_text = "RAINBOW"
		rainbow_color_menu_box = SettingsMenuBox(self.snake_to_edit, RAINBOW_SNAKE_COLORS, self, CENTER_OF_SCREEN, "RAINBOW", RAINBOW_MENU_BOX_TEXT_RENDERER, highlighted_text_renderer)
		self.menu_boxes.append(rainbow_color_menu_box)


class ScreenSettingsPage(Page):
	
	def create_boxes(self):
		pass


class BaseMenuBox(HighlightableSingleLineTextSurface):
	def __init__(self, page: Page, display_pos: tuple[int][int], text: str, default_text_renderer: BaseTextRenderer, highlighted_text_renderer: BaseTextRenderer):
		super().__init__(text, display_pos, default_text_renderer, highlighted_text_renderer, pos_is_centered_on_middle = True)
		self.page = page

	@abstractmethod
	def on_click(self):
		"""
		Method that is called when the user insteracts with the Menu Box
		"""
		raise NotImplementedError()

	

class TransitionMenuBox(BaseMenuBox):
	"""
	Subclass of MenuBox.
	Transitions to another page when iteracted with.
	"""
	def __init__(self, target_page_name: Page, page: Page, display_pos: tuple[int][int], text: str, default_text_renderer: BaseTextRenderer, highlighted_text_renderer: BaseTextRenderer):
		super().__init__(page, display_pos, text, default_text_renderer: BaseTextRenderer, highlighted_text_renderer: BaseTextRenderer)
		self.target_page_name = target_page_name

	def on_click(self):
		"""
		Transfers to the child page that this Menubox references
		"""
		target_page = self.page.child_pages[self.target_page_name]
		self.page.menu.change_page(target_page)

class PlayMenuBox(BaseMenuBox):
	"""
	Subclass of MenuBox.
	MenuBox that starts the game when clicked
	"""

	def on_click(self):
		"""
		Ends the menu loop and starts the game
		"""
		self.page.menu.start_game()

class QuitProgramMenuBox(BaseMenuBox):
	def on_click(self):
		"""
		Closes the program application 
		"""
		quit_program()

class SettingsMenuBox(BaseMenuBox):
	"""
	Subclass of MenuBox.
	For MenuBoxes that alter a game setting variable.
	When clicked, it will the change the variable_to_change_on_click 
	to the new_data_for_variable both passed in constructor
	"""
	def __init__(self, mutable_variable_to_change_on_click, new_data_for_variable, page: Page, display_pos: tuple[int][int], text: str, default_text_renderer: BaseTextRenderer, highlighted_text_renderer: BaseTextRenderer):
		super().__init__(page, display_pos, text, default_text_renderer: BaseTextRenderer, highlighted_text_renderer: BaseTextRenderer)
		self.variable_to_change = mutable_variable_to_change_on_click
		self.new_data_for_variable = new_data_for_variable
	
	def on_click(self):
		"""
		Change the held settings variable to the new data
		"""
		self.variable_to_change = self.new_data_for_variable


class SettingsMenuBoxLambdaTry(BaseMenuBox):
	"""
	Subclass of MenuBox.
	For MenuBoxes that alter a game setting variable.
	When clicked, it will the change the variable_to_change_on_click 
	to the new_data_for_variable both passed in constructor
	"""
	def __init__(self, lambda_on_click_func, page: Page, display_pos: tuple[int][int], text: str, default_text_renderer: BaseTextRenderer, highlighted_text_renderer: BaseTextRenderer):
		super().__init__(page, display_pos, text, default_text_renderer: BaseTextRenderer, highlighted_text_renderer: BaseTextRenderer)
		self.on_click_fun = lambda_on_click_func
	
	def on_click(self):
		"""
		Change the held settings variable to the new data
		"""
		self.on_click_func()


## I created an arrow class so I could customize the arrow more easily and in case I wanted to create multiple instances of the arrow instead of moving it from page to page
class Arrow:
	"""
	Arrow is an object shaped like an arrow that can be displayed to the left or right side of a rect
	"""
	def __init__(self, space_btw_box_and_arrow, side_of_box = "left"):
		self.space_btw_arrow_and_box = space_btw_box_and_arrow
		self.current_selected_box: BaseMenuBox | None = None
		self.side_of_box = side_of_box
		self.rect = (0,0,10,10) #Blank holder for now


	def set_arrow_pos_to_left_side_of_selected_box(self):
		self.x = self.current_selected_box.display[0] - self.menu.space_between_arrow - self.width

	def set_arrow_pos_to_right_side_of_selected_box(self):
		self.x = self.current_selected_box.display[0] + self.current_selected_box.width + self.space_btw_arrow_and_box + self.width

	def change_side_of_box(self, new_side_of_box):
		"""
		Changes the arrow to another side of the box ("right", or "left").
		If the arrow is already on that side then it does nothing.
		"""
		if new_side_of_box not in ["right, left"]:
			raise ValueError["Not a side. Please pass 'right' or 'left' to change the side "]
		if new_side_of_box == self.side_of_box:
				return

		self.side_of_box = new_side_of_box
		if new_side_of_box == "right":
				self.set_arrow_pos_to_right_side_of_selected_box()
				## Adds together the selected box's x and width, the menu's spacing between box and arrow, and the arrow's width to position the arrow on the right hand side of that box

		elif new_side_of_box == "left":
				self.set_arrow_pos_to_left_side_of_selected_box()


	def _update_pos_based_on_current_box(self):
		"""
		Sets the y position of the arrow to the middle y of its current selected box
		"""
		self.y = self.menu.selected_box.display_pos[1] + (self.menu.selected_box.height // 2)

	def change_box(self, new_box: BaseMenuBox): #the positions don't change atuomatically so I have to set the x and y coordiantes relative to the side they're on
		"""
		Changes the arrows selected box to the new passed box
		Parameters:
				- (MenuBox) new_box: The new box to display the arrow next to
		"""
		self.current_selected_box = new_box
		self.y = self.menu.selected_box.display_pos[1] + (self.menu.selected_box.height // 2)
		## selected_box.height //2 puts the arrow's y_coor halfway down the box


	def display(self, win: pygame.surface.Surface):
		#Draws arrow to screen. (Arrow is just a long rect)
		pygame.draw.rect(win, ARROW_COLOR, self.rect)

