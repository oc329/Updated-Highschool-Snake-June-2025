from abc import ABC, abstractclassmethod
import pygame 
from sys import exit

pygame.init()

from enums import Direction

def quit_program():
    pygame.display.quit() 
    pygame.quit()
    exit()

class AbstractEventHandler(ABC):
    def __init__(self, keys_to_track: tuple[int, ...]):
        self._keys_to_track = keys_to_track
        self.key_states = {key: False for key in keys_to_track}

        # Optional: auto-generate properties like up_arrow_pressed
        self._generate_key_properties()

    def _generate_key_properties(self):
        """
        ChatGPT code to dynamically create properties 
        of the key states with a naming format that I like.
        Creates property name as "key_name"_key_is pressed.
        And for arrow keys: "key_name"_arrow_key_is_pressed

        """
        for key_int_value in self._keys_to_track:
            key_name = pygame.key.name(key_int_value).lower()
            key_name_with_underscore_instead_of_space = key_name.replace(" ", "_")

            ## Adding arrow word to arrow key properties
            if key_name in ("up", "down", "left", "right"):
                property_name = f"{key_name}_arrow_key_is_pressed"
            else:
                property_name = f"{key_name}_key_is_pressed"

            setattr(self.__class__, property_name, property(lambda self, key_states_key = key_int_value: self.key_states[key_states_key]))
    
    def record_input(self):
        """
        Updates key_states based on KEYDOWN/KEYUP events.
        """
        for event in pygame.event.get():
            if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                if event.key in self.key_states:
                    is_pressed = (event.type == pygame.KEYDOWN)
                    self.key_states[event.key] = is_pressed


class MainMenuEventHamdler(AbstractEventHandler): 
    def __init__(self):
        keys_to_track = (
            pygame.K_UP,
            pygame.K_DOWN,
            pygame.K_RETURN,
            pygame.K_ESCAPE,

        )
        super().__init__(keys_to_track)



class GameLoopEventHandler(AbstractEventHandler): 
    def __init__(self):
        keys_to_track = (
            pygame.K_UP,
            pygame.K_DOWN,
            pygame.K_LEFT,
            pygame.K_RIGHT,
        )
        super().__init__(keys_to_track)
    
    
    def direction_key_pressed(self) -> str | None:
        """
        Returns the direction of the currently pressed arrow key.
        If no arrow key is pressed, returns None.
        """

        if self.right_arrow_key_is_pressed:
            return Direction.RIGHT
        elif self.left_arrow_key_is_pressed:
            return Direction.LEFT
        elif self.up_arrow_key_is_pressed:
            return Direction.UP
        elif self.down_arrow_key_is_pressed:
            return Direction.DOWN
        return None


        