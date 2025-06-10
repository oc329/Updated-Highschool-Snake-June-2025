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
    
    def __init__(self, text: str, pos: tuple[int], text_renderer: BaseTextRenderer,
                 pos_is_centered_on_middle=False):
        """
        Parameters:
        - text (str): The text to be displayed.
        - pos (tuple): The position (x, y) of the text.
        - font_obj (Font): The font object to be used for rendering.
        - text_renderer (BaseTextRenderer): The BaseTextRenderer object that contains the font, color and anti_alliasing info
        - pos_is_centered_on_middle (bool): Whether the text is center around the middle. Default is False.
        """
        self.text = text
        self.text_renderer = text_renderer
        self.pos_is_centered_on_middle = pos_is_centered_on_middle
        self.middle_of_text_pos = pos if pos_is_centered_on_middle else None
        
        self._render_current_text()
        self._update_position(pos)

    def _update_position(self, pos):
        """
        Takes in a new pos and changes the pos of the text
        Parameters:
        pos (tuple): The position new x,y pos of the text.
        """
        if self.pos_is_centered_on_middle:
            self._calculate_display_pos_from_middle(pos)
        else:
            self.display_pos = pos
            ensure_pos_is_on_screen(self.display_pos)

    def _calculate_display_pos_from_middle(self, pos):
        half_text_width = self.get_width() // 2
        self.display_pos = (pos[0] - half_text_width, pos[1])
        ensure_pos_is_on_screen(self.display_pos)
    
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


class SingleLineTextSurface(BaseTextSurface):
    def _render_current_text(self):
        self.rendered_text = self.text_renderer.render(self.text)

    def get_width(self):
        return self.rendered_text.get_width()
    
    def get_height(self):
        return self.rendered_text.get_height()
    
    def display(self, win):
        win.blit(self.rendered_text, self.display_pos)


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
        num_lines = len(self.rendered_texts) * self.text_renderer.get_font().get_height()
    
    def _render_current_text(self):
        if self.text != "":
            self.texts = self._get_text_chunks()
            self.rendered_texts = [self.text_renderer.render(line) for line in self.texts]
   
    def _calculate_center_row(self):
        number_of_rows = len(self.texts)
        
        self.current_center_row_i  = number_of_rows // 2

    def _calculate_display_pos_from_middle(self, pos):
        half_text_width = self.get_width() // 2
        self._calculate_center_row()
        self.display_pos = (pos[0] - half_text_width, pos[1])
        ensure_pos_is_on_screen(self.display_pos)
    
    def display(self, win):
        x, y = self.display_pos
        line_height = self.text_renderer.font.get_height()
        line_spacing = 5 // 4  # Space in-btw lines as ratio of line height
        for row_index, surface in enumerate(self.rendered_texts):
            row_offset = (row_index - self.current_center_row_i) * line_height * line_spacing
            win.blit(surface, (x, y + row_offset))

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
    def change_text(self, new_text):
        self.text = new_text
        self._render_current_text()
        self._update_middle_position()

    def change_pos(self, new_pos, new_pos_is_middle=False):
        self.pos_is_centered_on_middle = new_pos_is_middle
        self._update_position(new_pos)

    def change_color(self, new_color):
        self.text_renderer.change_color(new_color)
        self._render_current_text()
        
    def _update_middle_position(self): 
        """
        Updates the display position. 
        Used to update where the middle of the text in case more characters have been added
        """
        if self.pos_is_centered_on_middle:
            self._calculate_display_pos_from_middle(self.middle_of_text_pos)

    def rerender_text_and_pos_if_middle(self):
        """
        Rerenders the text in case changes have been made
        and updates the position in case the middle of the text has changed
        """
        self._update_middle_position(self.display_pos)
        self._render_current_text()
        
 
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
        self._update_middle_position()

    def _rerender_last_line(self):
        """
        Rerenders the text in case changes have been made
        and updates the position in case the middle of the text has changed
        """
        self.rendered_texts[-1] = self.text_renderer.render(self.texts[-1])
        self._update_middle_position()
    
    def _add_new_line_and_char(self, char: str):
        """
        Adds a new line to the text Surface and adds the character to it
        """
        self.texts.append(char)
        self.rendered_texts.append(self.text_renderer.render(self.texts[-1]))
        self._update_middle_position()
    
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

        
