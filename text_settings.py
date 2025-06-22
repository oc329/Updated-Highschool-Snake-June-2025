from abc import ABC
from os import path
from pygame.font import Font, SysFont 
from pygame.surface import Surface
from pygame import SRCALPHA
from collections.abc import Iterable


from colors import GAME_OVER_MSG_FONT_COLOR, GAME_SCORE_FONT_COLOR, MENU_BOX_DEFAULT_FONT_COLOR, MENU_BOX_DEFAULT_FONT_COLOR, MENU_BOX_HIGHLIGHTED_FONT_COLOR, MENU_TITLE_FONT_COLOR, RAINBOW_SNAKE_COLORS
from file_paths import emulogic_absolute_file_path
from screen_info import GAME_OVER_MSG_FONT_SIZE, GAME_SCORE_FONT_SIZE, MENU_BOX_DEFAULT_FONT_SIZE, MENU_TITLE_FONT_SIZE




GAME_SCORE_FONT = SysFont("freemono", GAME_SCORE_FONT_SIZE)
GAME_OVER_MSG_FONT = Font(emulogic_absolute_file_path, GAME_OVER_MSG_FONT_SIZE)
MENU_TITLE_FONT = Font(emulogic_absolute_file_path, MENU_TITLE_FONT_SIZE)
MENU_BOX_FONT = SysFont("freemono", MENU_BOX_DEFAULT_FONT_SIZE)

from dataclasses import dataclass

@dataclass (frozen = True)
class TextSettings(ABC):  
	font: Font
	anti_aliasing_is_on = True 

@dataclass (frozen = True)
class BaseTextRenderer(ABC): 
	text_settings: TextSettings

	def render(self, text: str) -> Surface:
		"""
		Returns a surface containing the rendered text 
		based on this renderer's text settings and color(s).
		Parameters:
			- (str) text: The text to be rendered

		Returns:
			- The rendered pygame surface of the text
		"""
		raise NotImplementedError()
	
	def change_color(self, color):
		"""
		Changes the color(s) to new color(s)
		"""
		raise NotImplementedError()
	
	def get_font_height(self) -> int:
		"""
		Returns the height of a character in this text settings' font
		"""
		return self.text_settings.font.get_height()
	def get_font(self) -> Font:
		"""
		Returns this renderer's text settings' font object
		"""
		return self.text_settings.font
@dataclass (frozen = True)
class TextRendererWithSingleColor(BaseTextRenderer):
	color: tuple[int, int, int]
	
	def render(self, text: str) -> Surface:
		"""
		Returns a surface containing the rendered text 
		based on this text settings object's color, font and anti_aliasing bool
		Parameters:
			- (str) text: The text to be rendered
		Returns:
			- The rendered pygame surface of the text
		"""
		return self.text_settings.font.render(text, self.text_settings.anti_aliasing_is_on, self.color)
	
@dataclass (frozen = True)
class TextRendererWithMultiColor(BaseTextRenderer):
	colors: Iterable[tuple[int, int ,int]] 
	"""
	Text renderer class whose render_surface method 
	returns a rendered text with multiple colors.
	"""
	def render(self, text: str,) -> Surface:
		"""
		Returns a surface with the rendered text. 
		The each character in the text has a color and if the text is longer 
		than the colors list, then it loops through the colors again.
		Parameters: 
			- (str) text: The text to render
			- (Iterable[tuple[int, int, int]])): The iterable of colors to display the text with
		"""
		num_colors = len(self.colors)
		char_surfaces: list[Surface] = []
		for char_i, char in enumerate(text):
			current_color = self.colors[char_i % num_colors] 
			char_surface = self.text_settings.font.render(char, self.text_settings.anti_aliasing_is_on, current_color)
			char_surfaces.append(char_surface)
		
		## Every char is the same width and height
		char_width, text_height = char_surfaces[0].get_size()
		text_width = char_width * len(text)
		text_surface = Surface((text_width, text_height), SRCALPHA)
		text_surface.set_alpha(255)

		for char_surface_i, char_surface in enumerate(char_surfaces):
			text_surface.blit(char_surface, (char_width * char_surface_i, 0))

		return text_surface
	
GAME_SCORE_TEXT_SETTINGS = TextSettings(GAME_SCORE_FONT)
MENU_TITLE_TEXT_SETTINGS = TextSettings(MENU_TITLE_FONT)
GAME_OVER_MSG_TEXT_SETTINGS = TextSettings(GAME_OVER_MSG_FONT)
MENU_BOX_TEXT_SETTINGS = TextSettings(MENU_BOX_FONT)

GAME_SCORE_TEXT_RENDERER = TextRendererWithSingleColor(GAME_SCORE_TEXT_SETTINGS, GAME_SCORE_FONT_COLOR)
MENU_TITLE_TEXT_RENDERER = TextRendererWithSingleColor(MENU_TITLE_TEXT_SETTINGS, MENU_TITLE_FONT_COLOR)
GAME_OVER_MSG_TEXT_RENDERER = TextRendererWithSingleColor(GAME_OVER_MSG_TEXT_SETTINGS, GAME_OVER_MSG_FONT_COLOR)

MENU_BOX_DEFAULT_COLOR_TEXT_RENDERER = TextRendererWithSingleColor(MENU_BOX_TEXT_SETTINGS, MENU_BOX_DEFAULT_FONT_COLOR)
MENU_BOX_HIGHLIGHTED_COLOR_TEXT_RENDERER= TextRendererWithSingleColor(MENU_BOX_TEXT_SETTINGS, MENU_BOX_HIGHLIGHTED_FONT_COLOR)
RAINBOW_MENU_BOX_TEXT_RENDERER = TextRendererWithMultiColor(MENU_BOX_TEXT_SETTINGS, RAINBOW_SNAKE_COLORS)