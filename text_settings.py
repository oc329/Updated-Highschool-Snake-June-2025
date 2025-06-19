from abc import ABC
from pygame.font import Font, SysFont 
from pygame.surface import Surface
from pygame import SRCALPHA
from collections.abc import Iterable
from colors import GAME_OVER_MSG_FONT_COLOR, GAME_SCORE_FONT_COLOR, MENU_BOX_DEFAULT_FONT_COLOR, MENU_BOX_DEFAULT_FONT_COLOR, MENU_BOX_HIGHLIGHTED_FONT_COLOR, MENU_TITLE_FONT_COLOR, RAINBOW_SNAKE_COLORS
from screen_info import GAME_OVER_MSG_FONT_SIZE, GAME_SCORE_FONT_SIZE, MENU_BOX_DEFAULT_FONT_SIZE, MENU_TITLE_FONT_SIZE

GAME_SCORE_FONT = SysFont("freemono", GAME_SCORE_FONT_SIZE)
GAME_OVER_MSG_FONT = Font("Emulogic.ttf", GAME_OVER_MSG_FONT_SIZE)
MENU_TITLE_FONT = Font("Emulogic.ttf", MENU_TITLE_FONT_SIZE)
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

# @dataclass (frozen = True)
# class TextRendererWithTwoColors(BaseTextRenderer):
# 	first_color: tuple[int, int, int]
# 	second_color: tuple[int, int, int]
	
	
# 	def render(self) -> tuple[Surface, Surface]:
# 		"""
# 		Renders a tuple of 2 surfaces of the rendered text. 
# 		Each surface has the same font and anti-aliasing bool. 
# 		The first surface is the first_color
# 		and the second is the second_color (Can be used for highlighting) 

# 		Parameters:
# 				- (str) text: The text to be rendered
# 		Returns:
# 				- tuple[Surface, Surface] containing the default and highlighted text
# 		"""
# 		default_surface = super().render_surface()
# 		highlight_surface = None
# 		if self.highlight_color:
# 			highlight_surface = self.font.render(self.text, True, self.highlight_color)
# 		return default_surface, highlight_surface


# @dataclass (frozen = True)
# class TextRendererWithoutColor(BaseTextSettings):
# 	def render_surface(self, text: str, color: tuple[int, int, int]) -> Surface:
# 		"""
# 		Returns a surface containing the rendered text 
# 		based on this text settings object's color, font and anti_aliasing bool
# 		Parameters:
# 			- (str) text: The text to be rendered
# 		Returns:
# 			- The rendered pygame surface of the text
# 		"""
# 		return self.font.render(self.text, self.anti_aliasing_is_on, color)