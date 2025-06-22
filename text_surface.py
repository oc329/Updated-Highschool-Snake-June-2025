from abc import ABC
from itertools import batched
from pygame.font import Font
import pygame

from math import ceil

from colors import WHITE
from enums import TextSurfacePosAnchor
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
                 pos_anchor: TextSurfacePosAnchor = TextSurfacePosAnchor.START):
        """
        Parameters:
        - text (str): The text to be displayed.
        - display_pos (tuple): The position (x, y) of the text.
        - font_obj (Font): The font object to be used for rendering.
        - text_renderer (BaseTextRenderer): The BaseTextRenderer object that contains the font, color and anti_alliasing info
        - pos_anchor (TextSurfacePosAnchor): 'start', 'middle', or 'end' – controls how text is aligned relative to `pos`
        """
        self.text = text
        self.text_renderer = text_renderer
        self.pos_anchor = pos_anchor
        self.anchor_pos = display_pos
        self.display_pos = self.anchor_pos
        
        self._render_current_text()
        self._set_display_pos_based_on_anchor()
    
    
    def change_display_pos(self, new_display_pos: tuple[int, int]):
        """
        Raises ValueError if display position is not on screen
        """
        ensure_pos_is_on_screen(new_display_pos)
        self.display_pos = new_display_pos

    def change_pos_anchor(self, new_pos_anchor: str):
        """
        Changes the position anchor and 
        updates the display position accordingly.
        Raises an error if the position anchor isn't 'start', 'middle' or 'end'
        """
        possible_values = [pos_anchor.value for pos_anchor in TextSurfacePosAnchor]
        if new_pos_anchor not in possible_values:
            raise ValueError(f"Anchor should be {possible_values}")
        self.pos_anchor = new_pos_anchor
        self._set_display_pos_based_on_anchor()

    def _set_display_pos_based_on_anchor(self):
        """
        Calculates and sets the display position based on the anchor attribute ('start', 'middle', 'end')
        """ 
        
        if self.pos_anchor == 'middle':
            new_display_pos = self._calculate_display_pos_from_middle(self.anchor_pos)
        elif self.pos_anchor == 'end':
            new_display_pos = self._calculate_display_pos_from_end(self.anchor_pos)

        self.change_display_pos(new_display_pos)

    def _calculate_display_pos_from_middle(self, middle_pos: str):
        """
        Calculates the display pos based on the given middle position. 
        Returns the display position.
        """
        half_text_width = self.get_width() // 2
        pos_calculated_from_middle = (middle_pos[0] - half_text_width, middle_pos[1])
        return pos_calculated_from_middle

    def _calculate_display_pos_from_end(self, end_pos: str):
        """
        Calculates and returns the display position calculated from the given end position.
        (End position - the text surface width).
        """
        pos_calculated_from_end = (end_pos[0] - self.get_width(), end_pos[1])
        return pos_calculated_from_end


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
    Text surface that displays the text split into multiple lines based on the passed line character limit.
    Only splits text that doesn't have split at words or spaces.
    """
    def __init__(self, line_char_limit: int, text: str, pos: tuple[int], text_renderer: BaseTextRenderer,
                 pos_anchor = 'start'):
        self.line_char_limit = line_char_limit
        self.texts = []
        self.rendered_texts = []
        super().__init__(text, pos, text_renderer, pos_anchor)
    
    def _get_text_chunks(self):
        """
        Chunks the text at intervals and returns it as a list
        """
        return get_chunk_str_into_list_of_str_using_batched(self.text, self.line_char_limit)

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
        Calculates and returns the display pos based on the passed middle pos.
        Display positions is centered on the text horizontally and vertically 
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


class EditableTextSurfaceMixin:
    def change_text(self, new_text: str):
        """
        Changes the text to the new text and
        updates display position based on pos anchor attribute
        """
        self.text = new_text
        self._render_current_text()
        self._set_display_pos_based_on_anchor()

    def change_pos(self, new_pos: tuple[int, int]):
        """
        Sets display position to the new position. 
        Sets it based on position anchor attribute ('start', 'middle', 'end')
        Parameters:
            - (tuple[int, int]) new_pos: The x, y display position of the text based on position anchor
        """
        self.anchor_pos = new_pos
        self._set_display_pos_based_on_anchor()
    
    def change_text_and_pos(self, new_text: str, new_pos: tuple[int, int]):
        self.change_pos(new_pos)
        self.change_text(new_text)

    def rerender_text_and_pos(self):
        """
        Rerenders the text in case changes have been made
        and updates the position in case the middle of the text has changed
        """
        self._render_current_text()
        self._set_display_pos_based_on_anchor()
 

class EditableSingleLineTextSurface(SingleLineTextSurface, EditableTextSurfaceMixin):
    """
    Combines Editing Functionality from Mixin with Single Line Text Surface Class
    
    Surface Class that stores text and blits it to the screen. Text and position can change with methods.
    """
    pass

class HighlightableEditableSingleLineTextSurface(EditableSingleLineTextSurface):
    def __init__(self, text, display_pos: tuple[int, int], default_text_renderer: BaseTextRenderer, highlight_text_renderer: BaseTextRenderer, pos_anchor = 'start'):
        super().__init__(text, display_pos, default_text_renderer, pos_anchor)
        self.default_text_renderer = default_text_renderer
        self.highlight_text_renderer = highlight_text_renderer
        
    def highlight(self):
        """
		Switches the text's color to the highlighted color
		"""
        self.text_renderer = self.highlight_text_renderer 
        self._render_current_text()

    def unhighlight(self):
        """
		Switches the text's color to the default color
		"""
        self.text_renderer = self.default_text_renderer
        self._render_current_text()

class EditableMultiLineTextSurface(MultiLineTextSurface, EditableTextSurfaceMixin):
    """
    Combines Editing Functionality from Mixin with Multi Line Text Surface Class
    Surface Class that stores text and blits it to the screen in multiple lines based on a line character limit.
    Text and dispalay position can change with methods.
    """
    def remove_last_line(self): 
        self.texts.pop()
        self.rendered_texts.pop()
        self._set_display_pos_based_on_anchor()

    def _rerender_last_line(self):
        """
        Rerenders the text in case changes have been made
        and updates the position in case the middle of the text has changed
        """
        self.rendered_texts[-1] = self.text_renderer.render(self.texts[-1])
        self._set_display_pos_based_on_anchor()
    
    def _add_new_line_and_char(self, char: str):
        """
        Adds a new line to the text Surface and adds the character to it
        """
        self.texts.append(char)
        self.rendered_texts.append(self.text_renderer.render(self.texts[-1]))
        self._set_display_pos_based_on_anchor()
    
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
        if len(self.texts) == 0 or len(self.texts[-1]) >= self.line_char_limit:
            self._add_new_line_and_char(char)
        else:
            ## Append character to current line and rerender it
            self.texts[-1] += char
            self._rerender_last_line()
