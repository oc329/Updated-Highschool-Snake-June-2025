from abc import ABC, abstractmethod
import pygame
from typing import TYPE_CHECKING
pygame.init()

from resource_modules.colors import ARROW_COLOR, RAINBOW_SNAKE_COLORS
from resource_modules.enums import AbstractSectorPosAnchor, Direction, HorizontalSectorPosAnchor, PageName, SectorType, TextSurfacePosAnchor, VerticalSectorPosAnchor
from core.event_handler import quit_program
from ui.page_layout_managers.sector_layout_manager import AbstractSectorLayoutManager, HorizontalSectorLayoutManager, VerticalSectorLayoutManager
from snake_game_stuff.skin import AbstractSkinManager, SnakeColorSkin
from resource_modules.screen_info import ARROW_SIZE, CENTER_OF_SCREEN, MAIN_MENU_PAGE_SNAKE_STARTING_GRID_POS, MIDDLE_TOP_OF_SCREEN, SCREEN_HEIGHT, MAIN_MENU_SNAKE_STARTING_GRID_POS_ON_SKINS_PAGE
from snake_game_stuff.snake import MenuSnake
from ui.text_settings import BaseTextRenderer, MENU_BOX_DEFAULT_COLOR_TEXT_RENDERER, MENU_BOX_HIGHLIGHTED_COLOR_TEXT_RENDERER, MENU_BOX_TEXT_SETTINGS, MENU_TITLE_TEXT_RENDERER, RAINBOW_MENU_BOX_TEXT_RENDERER, TextRendererWithMultiColor, TextRendererWithSingleColor
from ui.text_surface import SingleLineTextSurface, HighlightableEditableSingleLineTextSurface

if TYPE_CHECKING:
	from ui.main_menu import Menu  # Import only for type hinting


class Page(ABC):
	def __init__(self, menu: 'Menu', index_to_insert_transition_boxes = None):
		## Later defined using set_outer_page method which is called in main
		## The outer page of a page is reliant on other pages so I don't want to have to define the pages in the order that they rely on pages so I'm using a method to assign a page to the page's outer_page atribtue after initialization
		self.menu = menu
		
		self.outer_page : Page | None = None
		self.child_pages: dict[PageName, Page] =  {}
		self.menu_boxes: list[HighlightableEditableSingleLineTextSurface] = []
		self.highlighted_menu_box_text_renderer = MENU_BOX_HIGHLIGHTED_COLOR_TEXT_RENDERER
		self.index_to_insert_transition_boxes = index_to_insert_transition_boxes
		self.selected_box_index: int = 0

		self.create_boxes()

	def create_boxes(self):
		"""
		Method that creates all the Menuboxes attributes.
		Should be called in __init__
		"""
		raise NotImplementedError()

	def set_child_pages(self, child_pages_dict: dict[PageName: 'Page']):
		"""
		Sets the child pages to the given child pages dict. 
		Automatically creates the transition page menu boxes
		Parameters: 
			-(dict[PageName: 'Page']) child_pages_dict: A dict with Page Names as the keys and Pages as the values
		"""
		for page_name, page in child_pages_dict.items():
			self.add_child_page(page_name, page)

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
	
	@property
	def selected_box(self):
		"""
		Returns the current selected box
		"""
		## Raises an error if there are no menu boxes 
		if not self.menu_boxes:
			raise IndexError("Page has no menu boxes; cannot select a box.")
		
		return self.menu_boxes[self.selected_box_index]
	
	def on_enter(self):
		"""
		Method that is called when this page becomes active 
		"""
		pass

	def on_every_frame(self):
		"""
		Method that is called every display frame 
		when this page is active 
		"""
		pass
	

	def display(self, win: pygame.surface.Surface):
		"""
		Displays all the Game Title and all Menu boxes 
		"""
		for menu_box in self.menu_boxes: 
			menu_box.display(win)
		self.on_every_frame()

class PageWithBoxesCompactedIntoSector(Page):
	"""
	Subclass of Page. Has methods and functionality to display 
	the menu boxes into a vertical list between the passed start and end pos. 
	"""
	def __init__(self, menu: 'Menu', top_left_pos: tuple[int, int], bottom_right_pos: tuple[int, int], box_pos_anchor = TextSurfacePosAnchor.MIDDLE,
			  sector_pos_anchor: AbstractSectorPosAnchor = VerticalSectorPosAnchor.MIDDLE, sector_type = SectorType.VERTICAL): 
		
		self.layout_manager = self._get_layout_manager_based_on_type(top_left_pos, bottom_right_pos, sector_type, sector_pos_anchor, box_pos_anchor)
		self.box_pos_anchor = box_pos_anchor
		super().__init__(menu)
		## Needs to after Page super so page can create boxes
		self.layout_manager.position_boxes(self.menu_boxes)

	def _get_layout_manager_based_on_type(self, top_left_pos: tuple[int, int], bottom_right_pos: tuple[int, int], 
									   sector_type: AbstractSectorLayoutManager, sector_pos_anchor: AbstractSectorPosAnchor, box_pos_anchor: TextSurfacePosAnchor) -> AbstractSectorLayoutManager:
		"""
		Based on the given Sector Type enum. 
		Returns the corresponding SectorLayoutManager object
		"""
		if sector_type is SectorType.VERTICAL: 
			layout_manager = VerticalSectorLayoutManager(top_left_pos, bottom_right_pos, sector_pos_anchor, box_pos_anchor)
		elif sector_type is SectorType.HORIZONTAL: 
			layout_manager = HorizontalSectorLayoutManager(top_left_pos, bottom_right_pos, sector_pos_anchor, box_pos_anchor)
		else:
			raise ValueError("Sector type should be a valid SectorType Enum")
		
		return layout_manager
	
class MainMenuPage(PageWithBoxesCompactedIntoSector):
	def __init__(self, game_title: str, menu_snake: MenuSnake, menu: 'Menu', top_left_pos: tuple[int, int], bottom_right_pos: tuple[int, int], box_pos_anchor = TextSurfacePosAnchor.MIDDLE):
		super().__init__(menu, top_left_pos, bottom_right_pos, box_pos_anchor)
		self.GAME_TITLE = game_title
		self.menu_snake = menu_snake
		y_space_btw_main_menu_title_and_first_box = SCREEN_HEIGHT // 16
		title_pos = (CENTER_OF_SCREEN[0], top_left_pos[1] - y_space_btw_main_menu_title_and_first_box)
		self.title_text_surface = SingleLineTextSurface(game_title, MIDDLE_TOP_OF_SCREEN, MENU_TITLE_TEXT_RENDERER, pos_anchor = TextSurfacePosAnchor.MIDDLE)
		self.ensure_sector_does_not_overlap_with_title()

	def ensure_sector_does_not_overlap_with_title(self):
		"""
		Raises a value Error if the title is within the page's sector
		"""
		title_x = self.title_text_surface.display_pos[0] 
		bottom_of_title_y = self.title_text_surface.display_pos[1] + self.title_text_surface.get_height()
		sector_top_left_pos = self.layout_manager.top_left_pos
		sector_bottom_right_pos = self.layout_manager.bottom_right_pos
		if sector_top_left_pos[1] < bottom_of_title_y < sector_bottom_right_pos[1]:
			raise ValueError(f"Title shouldn't overlap with page sector.\n"
					f"Title Pos: {(title_x, bottom_of_title_y)}\n"
					f"Top Left Pos: {sector_top_left_pos}\n"
					f"Bottom Right Pos: {sector_bottom_right_pos}"
					)
		
	### Settings Page Boxes
	def create_boxes(self):
		"""
		Creates all the menu boxes for the pages. 
		Feeds them dummy positions to be corrected later.
		"""
		self.play_box = PlayMenuBox(self, "Play", MENU_BOX_DEFAULT_COLOR_TEXT_RENDERER, MENU_BOX_HIGHLIGHTED_COLOR_TEXT_RENDERER, pos_anchor = self.box_pos_anchor)
		self.settings_page_transition_box = TransitionMenuBox(PageName.TRANSITION_TO_SETTINGS, self, PageName.TRANSITION_TO_SETTINGS.value, MENU_BOX_DEFAULT_COLOR_TEXT_RENDERER, MENU_BOX_HIGHLIGHTED_COLOR_TEXT_RENDERER, pos_anchor = self.box_pos_anchor)
		# self.color_page_transition_box = TransitionMenuBox(PageName.SNAKE_SKIN_SETTINGS, self, "SNAKE COLORS", MENU_BOX_DEFAULT_COLOR_TEXT_RENDERER, MENU_BOX_HIGHLIGHTED_COLOR_TEXT_RENDERER, pos_anchor = self.box_pos_anchor)
		# self.screen_page_transition_box = TransitionMenuBox(PageName.SCREEN_SETTINGS, self, "SCREEN DIMENSIONS", MENU_BOX_DEFAULT_COLOR_TEXT_RENDERER, MENU_BOX_HIGHLIGHTED_COLOR_TEXT_RENDERER, pos_anchor = self.box_pos_anchor)
		self.quit_box = QuitProgramMenuBox(self, "QUIT", MENU_BOX_DEFAULT_COLOR_TEXT_RENDERER, MENU_BOX_HIGHLIGHTED_COLOR_TEXT_RENDERER, pos_anchor = self.box_pos_anchor)
		self.menu_boxes = [self.play_box, self.settings_page_transition_box, self.quit_box]

	def on_enter(self):
		### Move snake to postiion with the head in the right direction 
		self.menu_snake.move_to_new_pos_and_change_to_any_direction(MAIN_MENU_PAGE_SNAKE_STARTING_GRID_POS, Direction.RIGHT) 

	def on_every_frame(self):
		"""
		Moves the menu snake forward one
		"""
		self.menu_snake.move_forward_by_one_with_teleport_at_wall()
		
	def display(self, win: pygame.surface.Surface):
		"""
		Displays all the Game Title and all Menu boxes.
		"""
		super().display(win)
		self.title_text_surface.display(win)
		self.menu_snake.display(win)

class SettingsTransitionPage(PageWithBoxesCompactedIntoSector):
	def create_boxes(self):
		"""
		Creates all the menu boxes for the pages. 
		Feeds them dummy positions to be corrected later.
		"""
		self.color_page_transition_box = TransitionMenuBox(PageName.SNAKE_SKIN_SETTINGS, self, PageName.SNAKE_SKIN_SETTINGS.value, MENU_BOX_DEFAULT_COLOR_TEXT_RENDERER, MENU_BOX_HIGHLIGHTED_COLOR_TEXT_RENDERER, pos_anchor = self.box_pos_anchor)
		self.screen_page_transition_box = TransitionMenuBox(PageName.SCREEN_SETTINGS, self, PageName.SCREEN_SETTINGS.value, MENU_BOX_DEFAULT_COLOR_TEXT_RENDERER, MENU_BOX_HIGHLIGHTED_COLOR_TEXT_RENDERER, pos_anchor = self.box_pos_anchor)
		self.menu_boxes = [self.color_page_transition_box, self.screen_page_transition_box]
		
class ColorSnakeSkinsSettingsPage(PageWithBoxesCompactedIntoSector):
	def __init__(self, snake_skin_manager: AbstractSkinManager, snake_to_edit: MenuSnake, menu: 'Menu', top_left_pos: tuple[int, int], bottom_right_pos: tuple[int, int], box_pos_anchor: str = TextSurfacePosAnchor.MIDDLE):
		self.snake_skin_manager = snake_skin_manager
		self.snake_to_edit = snake_to_edit
		super().__init__(menu, top_left_pos, bottom_right_pos, box_pos_anchor)

	def create_boxes(self):
		for skin in self.snake_skin_manager.get_all_skins():
			self.create_color_skin_box(skin)
	
	def create_color_skin_box(self, skin: SnakeColorSkin):
		"""
		Adds a Menu box to the boxes list that contains the Snake Color Skin
		Parameters: 
			- (SnakeColorSkin) skin: The current Snake Color Skin to make a Menu box out of 
		"""
		if len(skin.colors) > 1:
			text_renderer = TextRendererWithMultiColor(MENU_BOX_TEXT_SETTINGS, skin.colors)
		else:
			text_renderer = TextRendererWithSingleColor(MENU_BOX_TEXT_SETTINGS, skin.colors[0])
		
		lambda_change_color_func = lambda skin = skin: self.snake_to_edit.change_skin(skin)  
		self.menu_boxes.append(SettingsMenuBoxLambdaTry(lambda_change_color_func, self, skin.name, text_renderer, text_renderer))

	def on_enter(self):
		### Move snake to postiion and set it to static 
		self.snake_to_edit.move_to_new_pos_and_change_to_any_direction(MAIN_MENU_SNAKE_STARTING_GRID_POS_ON_SKINS_PAGE, Direction.UP)

	def display(self, win):
		super().display(win)
		self.snake_to_edit.display(win)

class ScreenSettingsPage(PageWithBoxesCompactedIntoSector):
	def __init__(self,  menu: 'Menu', top_left_pos: tuple[int, int], bottom_right_pos: tuple[int, int], box_pos_anchor: str = TextSurfacePosAnchor.MIDDLE):
		super().__init__(menu, top_left_pos, bottom_right_pos, box_pos_anchor)

	def create_boxes(self):
		test_box_text = "CENTER OF SCREEN"
		blank_holder_value = []
		test_box = SettingsMenuBox(blank_holder_value, CENTER_OF_SCREEN, self, test_box_text, MENU_BOX_DEFAULT_COLOR_TEXT_RENDERER, MENU_BOX_HIGHLIGHTED_COLOR_TEXT_RENDERER)
		self.menu_boxes.append(test_box)

class AbstractMenuBox(HighlightableEditableSingleLineTextSurface):
	DUMMY_POS = CENTER_OF_SCREEN

	def __init__(self, page: Page, text: str, default_text_renderer: BaseTextRenderer, highlighted_text_renderer: BaseTextRenderer,display_pos: tuple[int, int] = None, pos_anchor: str = TextSurfacePosAnchor.MIDDLE):
		if display_pos is None:
			display_pos = AbstractMenuBox.DUMMY_POS
		super().__init__(text, display_pos, default_text_renderer, highlighted_text_renderer, pos_anchor)
		self.page = page

	@abstractmethod
	def on_click(self):
		"""
		Method that is called when the user interacts with the Menu Box.
		Peforms the action that it's supposed to do 
		"""
		raise NotImplementedError()

class TransitionMenuBox(AbstractMenuBox):
	"""
	Subclass of MenuBox.
	Transitions to another page when iteracted with.
	"""
	def __init__(self, target_page_name: Page, page: Page, text: str, default_text_renderer: BaseTextRenderer, highlighted_text_renderer: BaseTextRenderer, display_pos: tuple[int, int] = None, pos_anchor: str = TextSurfacePosAnchor.MIDDLE):
		super().__init__(page, text, default_text_renderer, highlighted_text_renderer, display_pos, pos_anchor)
		self.target_page_name = target_page_name

	def on_click(self):
		"""
		Transfers to the child page that this Menubox references
		"""
		target_page = self.page.child_pages[self.target_page_name]
		self.page.menu.change_page(target_page)

class PlayMenuBox(AbstractMenuBox):
	"""
	Subclass of MenuBox.
	MenuBox that starts the game when clicked
	"""
	def on_click(self):
		"""
		Ends the menu loop and starts the game
		"""
		self.page.menu.start_game()

class QuitProgramMenuBox(AbstractMenuBox):
	def on_click(self):
		"""
		Closes the program application 
		"""
		quit_program()

class SettingsMenuBox(AbstractMenuBox):
	"""
	Subclass of MenuBox.
	For MenuBoxes that alter a game setting variable.
	When clicked, it will the change the variable_to_change_on_click 
	to the new_data_for_variable both passed in constructor
	"""
	def __init__(self, mutable_variable_to_change_on_click, new_data_for_variable, page: Page, text: str, default_text_renderer: BaseTextRenderer, highlighted_text_renderer: BaseTextRenderer, display_pos: tuple[int, int] = None, pos_anchor: str = TextSurfacePosAnchor.MIDDLE):
		super().__init__(page, text, default_text_renderer, highlighted_text_renderer, display_pos, pos_anchor)
		self.variable_to_change = mutable_variable_to_change_on_click
		self.new_data_for_variable = new_data_for_variable
	
	def on_click(self):
		"""
		Change the held settings variable to the new data
		"""
		self.variable_to_change = self.new_data_for_variable

class SettingsMenuBoxLambdaTry(AbstractMenuBox):
	"""
	Subclass of MenuBox.
	For MenuBoxes that alter a game setting variable.
	When clicked, it will the change the variable_to_change_on_click 
	to the new_data_for_variable both passed in constructor
	"""
	def __init__(self, lambda_on_click_func, page: Page, text: str, default_text_renderer: BaseTextRenderer, highlighted_text_renderer: BaseTextRenderer, display_pos: tuple[int, int] = None, pos_anchor: str = TextSurfacePosAnchor.MIDDLE):
		super().__init__(page, text, default_text_renderer, highlighted_text_renderer, display_pos, pos_anchor)
		self.on_click_func = lambda_on_click_func
	
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

		self.selected_box: AbstractMenuBox = self.menu.selected_box
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

	def change_box(self, new_box: AbstractMenuBox):
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



"""

	def create_boxes(self):
		for color_name, color_rgb in self.colors.items():
			text = color_name
			default_text_renderer = TextRendererWithSingleColor(MENU_BOX_TEXT_SETTINGS, color_rgb)
			#self.menu_boxes.append(SettingsMenuBox(self.snake_to_edit, color_rgb, self, text, default_text_renderer, default_text_renderer))
			lambda_change_color_func = lambda color=color_rgb: self.snake_to_edit.change_color(color)  
			self.menu_boxes.append(SettingsMenuBoxLambdaTry(lambda_change_color_func, self, text, default_text_renderer, default_text_renderer))

		## Adding Rainbow Menu Box
		rainbow_text = "RAINBOW"
		rainbow_color_menu_box = SettingsMenuBox(self.snake_to_edit, RAINBOW_SNAKE_COLORS, self, rainbow_text, RAINBOW_MENU_BOX_TEXT_RENDERER, RAINBOW_MENU_BOX_TEXT_RENDERER)
		self.menu_boxes.append(rainbow_color_menu_box)

"""