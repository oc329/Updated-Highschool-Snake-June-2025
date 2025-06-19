from abc import ABC, abstractmethod
import pygame
from typing import TYPE_CHECKING
pygame.init()

from colors import ARROW_COLOR, RAINBOW_SNAKE_COLORS
from enums import PageName
from event_handler import quit_program
from screen_info import ARROW_SIZE, CENTER_OF_SCREEN, MIDDLE_TOP_OF_SCREEN, SCREEN_HEIGHT, SCREEN_WIDTH
from snake import Snake
from text_settings import BaseTextRenderer, MENU_BOX_DEFAULT_COLOR_TEXT_RENDERER, MENU_BOX_HIGHLIGHTED_COLOR_TEXT_RENDERER, MENU_BOX_TEXT_SETTINGS, MENU_TITLE_TEXT_RENDERER, RAINBOW_MENU_BOX_TEXT_RENDERER, TextRendererWithSingleColor
from text_surface import SingleLineTextSurface, HighlightableEditableSingleLineTextSurface

if TYPE_CHECKING:
	from main_menu import Menu  # Import only for type hinting


	

class Page(ABC):
	def __init__(self, menu: 'Menu'):
		## Later defined using set_outer_page method which is called in main
		## The outer page of a page is reliant on other pages so I don't want to have to define the pages in the order that they rely on pages so I'm using a method to assign a page to the page's outer_page atribtue after initialization
		self.menu = menu
		
		self.outer_page : Page | None = None
		self.child_pages: dict[str : Page] =  {}
		self.menu_boxes: list[HighlightableEditableSingleLineTextSurface] = []
		self.highlighted_menu_box_text_renderer = MENU_BOX_HIGHLIGHTED_COLOR_TEXT_RENDERER

		self.create_boxes()

	def create_boxes(self):
		"""
		Method that creates all the Menuboxes attributes.
		Should be called in __init__
		"""
		raise NotImplementedError()

	def add_child_page(self, child_page_name: str, child_page: 'Page'):
		"""
		Adds a child page to this page's child pages
		"""
		self.child_pages[child_page_name] = child_page

	def set_outer_page(self, outer_page: 'Page'):
		"""
		Sets this page's outerpage
		"""
		self.outer_page = outer_page

	def display(self, win: pygame.surface.Surface):
		"""
		Displays all the Game Title and all Menu boxes 
		"""
		for menu_box in self.menu_boxes: 
			menu_box.display(win)
class PageWithBoxesCompactedIntoSector(Page):
	"""
	Subclass of Page. Has methods and functionality to display 
	the menu boxes into a vertical list between the passed start and end pos. 

	"""
	def __init__(self, menu: 'Menu', top_of_sector_pos: tuple[int, int], bottom_of_sector_pos: tuple[int, int], pos_anchor = "middle"): 
		## These attributes need to be before parent init since they're used in create_boxes method
		self.menu_box_dummy_pos = CENTER_OF_SCREEN
		self.pos_anchor = pos_anchor
		super().__init__(menu)
		self.longest_message_length: int | None = None
		self.top_of_sector_pos = top_of_sector_pos
		self.bottom_of_sector_pos = bottom_of_sector_pos

		self.box_display_interval = self._calculate_box_display_interval()

		self.move_boxes_into_sector()
		
	def _calculate_box_display_interval(self) -> int:
		"""
		Calculates the interval at which to display each box inside the sector.
		Is based on the number of boxes and the top and bottom pos
		
		Returns: 
			- (int) display_interval: An int representing the inteerval at which to display each box
		"""
		## Bottom subtracts from top since it's 4th quad graphics
		sector_height = self.bottom_of_sector_pos[1] - self.top_of_sector_pos[1]
		num_boxes = len(self.menu_boxes)
		return sector_height // num_boxes
	
	def move_boxes_into_sector(self):
		"""
		Moves the boxes into the page sector with equal spacing btw each one.
		(sector = space btw top and bottom sector pos) 
		
		"""
		for menu_box_i, menu_box in enumerate(self.menu_boxes):
			menu_box.change_pos_anchor(self.pos_anchor)
			y_coor = self.top_of_sector_pos[1] + self.box_display_interval * menu_box_i
			menu_box_display_pos = (self.top_of_sector_pos[0], y_coor)
			menu_box.change_pos(menu_box_display_pos)

class MainMenuPage(PageWithBoxesCompactedIntoSector):
	def __init__(self, game_title: str, menu: 'Menu', top_of_sector_pos: tuple[int, int], bottom_of_sector_pos: tuple[int, int], pos_anchor = "middle"):
		super().__init__(menu, top_of_sector_pos, bottom_of_sector_pos, pos_anchor)
		self.y_space_btw_main_menu_title_and_first_box = SCREEN_HEIGHT // 16
		self.GAME_TITLE = game_title
		title_pos = (top_of_sector_pos[0], bottom_of_sector_pos[1] - self.y_space_btw_main_menu_title_and_first_box)
		self.title_text_surface: SingleLineTextSurface = SingleLineTextSurface(game_title, MIDDLE_TOP_OF_SCREEN, MENU_TITLE_TEXT_RENDERER, pos_anchor = "middle")

	### Settings Page Boxes
	def create_boxes(self):
		"""
		Creates all the menu boxes for the pages. 
		Feeds them dummy positions to be corrected later.
		"""
		dummy_pos = self.menu_box_dummy_pos
		self.play_box = PlayMenuBox(self, CENTER_OF_SCREEN, "Play", MENU_BOX_DEFAULT_COLOR_TEXT_RENDERER, MENU_BOX_HIGHLIGHTED_COLOR_TEXT_RENDERER, self.pos_anchor)
		self.color_page_transition_box = TransitionMenuBox(PageName.SNAKE_SKIN_SETTINGS, self, CENTER_OF_SCREEN, "SNAKE COLORS", MENU_BOX_DEFAULT_COLOR_TEXT_RENDERER, MENU_BOX_HIGHLIGHTED_COLOR_TEXT_RENDERER, self.pos_anchor)
		self.screen_page_transition_box = TransitionMenuBox(PageName.SCREEN_SETTINGS, self, CENTER_OF_SCREEN, "SCREEN DIMENSIONS", MENU_BOX_DEFAULT_COLOR_TEXT_RENDERER, MENU_BOX_HIGHLIGHTED_COLOR_TEXT_RENDERER, self.pos_anchor)
		self.quit_box = QuitProgramMenuBox(self, CENTER_OF_SCREEN, "QUIT", MENU_BOX_DEFAULT_COLOR_TEXT_RENDERER, MENU_BOX_HIGHLIGHTED_COLOR_TEXT_RENDERER, self.pos_anchor)
		self.menu_boxes = [self.play_box, self.color_page_transition_box, self.screen_page_transition_box, self.quit_box]

	def display(self, win: pygame.surface.Surface):
		"""
		Displays all the Game Title and all Menu boxes 
		"""
		for menu_box in self.menu_boxes: 
			menu_box.display(win)
		self.title_text_surface.display(win)

class SnakeSkinsSettingsPage(PageWithBoxesCompactedIntoSector):
	def __init__(self, colors: dict[str : tuple[int, int, int]], snake_to_edit: Snake, menu: 'Menu', top_of_sector_pos: tuple[int, int], bottom_of_sector_pos: tuple[int, int], pos_anchor: str = "middle"):
		self.colors = colors
		self.snake_to_edit = snake_to_edit
		super().__init__(menu, top_of_sector_pos, bottom_of_sector_pos, pos_anchor)
		
		
	def create_boxes(self):
		for color_name, color_rgb in self.colors.items():
			text = color_name
			default_text_renderer = TextRendererWithSingleColor(MENU_BOX_TEXT_SETTINGS, color_rgb)
			highlighted_text_renderer = TextRendererWithSingleColor(MENU_BOX_TEXT_SETTINGS, color_rgb)
			self.menu_boxes.append(SettingsMenuBox(self.snake_to_edit, color_rgb, self, CENTER_OF_SCREEN, text, default_text_renderer, default_text_renderer))
		
		## Adding Rainbow Menu Box
		rainbow_text = "RAINBOW"
		rainbow_color_menu_box = SettingsMenuBox(self.snake_to_edit, RAINBOW_SNAKE_COLORS, self, CENTER_OF_SCREEN, "RAINBOW", RAINBOW_MENU_BOX_TEXT_RENDERER, RAINBOW_MENU_BOX_TEXT_RENDERER)
		self.menu_boxes.append(rainbow_color_menu_box)


class ScreenSettingsPage(PageWithBoxesCompactedIntoSector):
	
	def create_boxes(self):
		dummy_box = SettingsMenuBox([], CENTER_OF_SCREEN, self, self.menu_box_dummy_pos, "CENTER OF SCREEN", MENU_BOX_DEFAULT_COLOR_TEXT_RENDERER, MENU_BOX_HIGHLIGHTED_COLOR_TEXT_RENDERER)
		self.menu_boxes.append(dummy_box)

class BaseMenuBox(HighlightableEditableSingleLineTextSurface):
	def __init__(self, page: Page, display_pos: tuple[int, int], text: str, default_text_renderer: BaseTextRenderer, highlighted_text_renderer: BaseTextRenderer, pos_anchor: str = "middle"):
		super().__init__(text, display_pos, default_text_renderer, highlighted_text_renderer, pos_anchor)
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
	def __init__(self, target_page_name: Page, page: Page, display_pos: tuple[int, int], text: str, default_text_renderer: BaseTextRenderer, highlighted_text_renderer: BaseTextRenderer, pos_anchor: str = "middle"):
		super().__init__(page, display_pos, text, default_text_renderer, highlighted_text_renderer, pos_anchor)
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
	def __init__(self, mutable_variable_to_change_on_click, new_data_for_variable, page: Page, display_pos: tuple[int, int], text: str, default_text_renderer: BaseTextRenderer, highlighted_text_renderer: BaseTextRenderer, pos_anchor: str = "middle"):
		super().__init__(page, display_pos, text, default_text_renderer, highlighted_text_renderer, pos_anchor)
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
	def __init__(self, lambda_on_click_func, page: Page, display_pos: tuple[int, int], text: str, default_text_renderer: BaseTextRenderer, highlighted_text_renderer: BaseTextRenderer, pos_anchor: str = "middle"):
		super().__init__(page, display_pos, text, default_text_renderer, highlighted_text_renderer, pos_anchor)
		self.on_click_fun = lambda_on_click_func
	
	def on_click(self):
		"""
		Change the held settings variable to the new data
		"""
		self.on_click_func()

class Arrow:
	"""
	An arrow indicator rendered to the left or right of a selected menu box.
	"""

	def __init__(self, menu: 'Menu', space_btw_box_and_arrow: int, side_of_box: str = "left"):
		self.menu = menu
		self.space_btw_box_and_arrow = space_btw_box_and_arrow
		self.side_of_box = side_of_box

		self.selected_box: BaseMenuBox = self.menu.selected_box
		ratio_of_arrow_to_screen = 20
		self.width, self.height = ARROW_SIZE
		# self.width = (SCREEN_WIDTH // ratio_of_arrow_to_screen)
		# self.height = (self.selected_box.get_height() // (ratio_of_arrow_to_screen * 3 // 2))

	@property
	def x(self) -> int:
		"""
		Computes the arrow's x-position based on the current side and selected box.
		"""
		box_x = self.selected_box.display_pos[0]
		box_width = self.selected_box.get_width()

		if self.side_of_box == "left":
			return box_x - self.space_btw_box_and_arrow - self.width
		elif self.side_of_box == "right":
			return box_x + box_width + self.space_btw_box_and_arrow
		else:
			raise ValueError("side_of_box must be 'left' or 'right'.")

	@property
	def y(self) -> int:
		"""
		Computes the arrow's y-position centered vertically with the box.
		"""
		box_y = self.selected_box.display_pos[1]
		box_height = self.selected_box.get_height()
		return box_y + box_height // 2 - self.height // 2

	@property
	def display_pos(self) -> tuple[int, int]:
		return (self.x, self.y)

	def update_selected_box(self):
		"""
		Updates the selected box reference from the menu.
		"""
		self.selected_box = self.menu.selected_box

	def change_box(self, new_box: BaseMenuBox):
		"""
		Changes which box the arrow points to.
		"""
		self.selected_box = new_box

	def change_side_of_box(self, new_side_of_box: str):
		"""
		Changes the side of the box where the arrow is displayed.
		"""
		if new_side_of_box not in ("left", "right"):
			raise ValueError("side_of_box must be 'left' or 'right'.")
		self.side_of_box = new_side_of_box

	def display(self, win: pygame.surface.Surface):
		"""
		Draws the arrow on the screen.
		"""
		pygame.draw.rect(win, ARROW_COLOR, (*self.display_pos, self.width, self.height))

