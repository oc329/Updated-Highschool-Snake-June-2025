from abc import ABC
from itertools import batched
import pygame
from pygame.font import Font
from math import ceil

from colors import WHITE
from screen_info import ensure_pos_is_on_screen
from text_settings import BaseTextRenderer

pygame.init()




def get_chunk_str_into_list_of_str_using_batched(str_to_split: str, chunk_size: int):
    """
    Converts str into a list of strings split at intervals of size.
    Ex. ("12345", 3) --> ["123", "45]
    Converts Batched object of string tuples ('1', '2', '3'), ('4', '5') into list of string
    Parameters 
    - (str) str_to_split: The string to split into chunks 
    - (int) chunk_size: the size of each chunk out of str (interval to split str at)
    Returns: 
    - List of the string split into chunks
    """
    batched_obj = batched(str_to_split, chunk_size)
    chunked_str_list = [] 
    for text_tuple in batched_obj:
        chunked_str_list.append("".join(text_tuple))
    return chunked_str_list


class BaseTextSurface(ABC):
    """
    Abstract Text Surface Class
    """
    
    def __init__(self, text: str, display_pos: tuple[int], text_renderer: BaseTextRenderer,
                 pos_anchor = "start"):
        """
        Parameters:
        - text (str): The text to be displayed.
        - display_pos (tuple): The position (x, y) of the text.
        - font_obj (Font): The font object to be used for rendering.
        - text_renderer (BaseTextRenderer): The BaseTextRenderer object that contains the font, color and anti_alliasing info
        - pos_anchor (str): 'start', 'middle', or 'end' – controls how text is aligned relative to `pos`
        """
        self.text = text
        self.text_renderer = text_renderer
        self.pos_anchor = pos_anchor
        self.display_pos = display_pos
        
        self._render_current_text()
        self._calculate_display_pos_based_on_anchor()
    
    @property
    def display_pos(self):
        return self.display_pos
    
    @display_pos.setter
    def display_pos(self, new_display_pos: tuple[int, int]):
        """
        Raises ValueError if display position is not on screen
        """
        ensure_pos_is_on_screen()
        self.display_pos = new_display_pos

    def change_pos_anchor(self, new_pos_anchor: str):
        """
        Changes the position anchor and 
        updates the display position accordingly.
        Raises an error if the position anchor isn't 'start', 'middle' or 'end'
        """
        if new_pos_anchor not in ('start', 'middle', 'end'):
            raise ValueError("anchor must be 'start', 'middle', or 'end'")
        self.pos_anchor = new_pos_anchor
        self._calculate_display_pos_based_on_anchor()

    def _calculate_display_pos_based_on_anchor(self):
        """
        Calculates and sets the display position based on the anchor attribute ('start', 'middle', 'end')
        """ 
        if self.pos_anchor == 'middle':
            self._calculate_display_pos_from_middle(self.display_pos)
        elif self.pos_anchor == 'end':
            self._calculate_display_pos_from_end(self.display_pos)

        ensure_pos_is_on_screen(self.display_pos)

    def _calculate_display_pos_from_middle(self, middle_pos: str):
        """
        Sets the display pos from the given middle position
        """
        half_text_width = self.get_width() // 2
        self.display_pos = (middle_pos[0] - half_text_width, middle_pos[1])

    def _calculate_display_pos_from_end(self, end_pos: str):
        """
        Sets the display position from the end.
        (End position - the text surface width).
        """
        self.display_pos = (end_pos[0] - self.get_width(), end_pos[1])


    def get_width(self):
        """
        Returns the width of the text surface
        """
        raise NotImplementedError()
    
    def get_height(self):
        """
        Returns the height of the text surface
        """
        raise NotImplementedError()
    
    def _render_current_text(self): 
        raise NotImplementedError()

    def display(self, win):
        raise NotImplementedError()

class MultiLineTextSurface(BaseTextSurface):
    """
    Editable text surface that can have the text split into rows of a certain number of characters per row.
    Only splits text that doesn't have words or spaces
    """
    def __init__(self, row_char_limit: int, text: str, pos: tuple[int], text_renderer: BaseTextRenderer,
                 pos_is_centered_on_middle=False):
        self.row_char_limit = row_char_limit
        self.texts = []
        self.rendered_texts = []
        super().__init__(text, pos, text_renderer, pos_is_centered_on_middle)
    
    def _get_text_chunks(self):
        """
        Chunks the text at intervals and returns it as a list
        """
        return get_chunk_str_into_list_of_str_using_batched(self.text, self.row_char_limit)

    def get_width(self):
        return max((rendered_text.get_width() for rendered_text in self.rendered_texts), default=0)
    
    def get_height(self):
        num_lines = len(self.rendered_texts)
        height = num_lines * self.text_renderer.get_font().get_height()
        return height
    
    def _render_current_text(self):
        if self.text != "":
            self.texts = self._get_text_chunks()
            self.rendered_texts = [self.text_renderer.render(line) for line in self.texts]

    def _calculate_display_pos_from_middle(self, middle_pos: tuple[int, int]):
        """
        Calculates the display pos based on the passed middle pos. 
        Centers the text horizontally and vertically 
        """
        half_text_width = self.get_width() // 2
        half_text_height = self.get_height() // 2
        self.display_pos = (middle_pos[0] - half_text_width, middle_pos[1] - half_text_height)    
    
    def _calculate_display_pos_from_end(self, end_pos: str):
        self.display_pos = (end_pos[0] - self.get_width(), end_pos[1])

    def display(self, win):
        x, y = self.display_pos
        line_height = self.text_renderer.font.get_height()
        line_spacing = 5 // 4  # Space in-btw lines as ratio of line height
        for row_index, surface in enumerate(self.rendered_texts):
            row_offset = (row_index - self.current_center_row_i) * line_height * line_spacing
            win.blit(surface, (x, y + row_offset))

class SingleLineTextSurface(BaseTextSurface):
    def _render_current_text(self):
        self.rendered_text = self.text_renderer.render(self.text)

    def get_width(self):
        return self.rendered_text.get_width()
    
    def get_height(self):
        return self.rendered_text.get_height()
    
    def display(self, win):
        win.blit(self.rendered_text, self.display_pos)

class HighlightableSingleLineTextSurface(SingleLineTextSurface):
    def __init__(self, text, pos, default_text_renderer: BaseTextRenderer, highlight_text_renderer: BaseTextRenderer, pos_is_centered_on_middle=False):
        super().__init__(text, pos, default_text_renderer, pos_is_centered_on_middle)
        self.default_rendered_text = self.rendered_text
        self.highlighted_rendered_text = highlight_text_renderer.render(text)

    def highlight(self):
        """
		Switches the text's color to the highlighted color
		"""
        self.rendered_text = self.highlighted_rendered_text 

    def unhighlight(self):
        """
		Switches the text's color to the default color
		"""
        self.rendered_text = self.default_rendered_text


class EditableTextSurfaceMixin:
    def change_text(self, new_text: str):
        """
        Changes the text to the new text and
        updates display position based on pos anchor attribute
        """
        self.text = new_text
        self._render_current_text()
        self._calculate_display_pos_based_on_anchor()

    def change_pos(self, new_pos: tuple[int, int]):
        """
        Sets display position to the new position. 
        Sets it based on position anchor attribute ('start', 'middle', 'end')
        Parameters:
            - (tuple[int, int]) new_pos: The x, y display position of the text based on position anchor
        """
        self.display_pos = new_pos
        self._calculate_display_pos_based_on_anchor()

    def change_color(self, new_color):
        self.text_renderer.change_color(new_color)
        self._render_current_text()
    
    def change_text_and_pos(self, new_text: str, new_pos: tuple[int, int]):
        self.change_pos(new_pos)
        self.change_text(new_text)

    def rerender_text_and_pos(self):
        """
        Rerenders the text in case changes have been made
        and updates the position in case the middle of the text has changed
        """
        self._render_current_text()
        self._calculate_display_pos_based_on_anchor(self.display_pos)
        
 
class EditableSingleLineTextSurface(SingleLineTextSurface, EditableTextSurfaceMixin):
    """
    Combines Editing Functionality from Mixin with Single Line Text Surface Class
    
    Surface Class that stores text and blits it to the screen. Text and position can change with methods.
    """
    pass

class EditableMultiLineTextSurface(MultiLineTextSurface, EditableTextSurfaceMixin):
    """
    Combines Editing Functionality from Mixin with Multi Line Text Surface Class
    Surface Class that stores text and blits it to the screen. Text and position can change with methods.
    """
    def remove_last_line(self): 
        self.texts.pop()
        self.rendered_texts.pop()
        self._u()

    def _rerender_last_line(self):
        """
        Rerenders the text in case changes have been made
        and updates the position in case the middle of the text has changed
        """
        self.rendered_texts[-1] = self.text_renderer.render(self.texts[-1])
        self._calculate_display_pos_based_on_anchor()
    
    def _add_new_line_and_char(self, char: str):
        """
        Adds a new line to the text Surface and adds the character to it
        """
        self.texts.append(char)
        self.rendered_texts.append(self.text_renderer.render(self.texts[-1]))
        self._calculate_display_pos_based_on_anchor()()
    
    def add_char(self, char: str):
        """
        Adds a single character to the text surface, automatically wrapping
        to a new line if the current line exceeds the row character limit.

        Parameters:
            char (str): A single character to add to the text surface.

        Raises:
            ValueError: If `char` is not exactly one character long.
        """
        if len(char) != 1:
            raise ValueError("char should be exactly one character long")
        
        ## Start a new line if there are no lines yet or if the last line is full
        if len(self.texts) == 0 or len(self.texts[-1]) >= self.row_char_limit:
            self._add_new_line_and_char(char)
        else:
            ## Append character to current line and rerender it
            self.texts[-1] += char
            self._rerender_last_line()
