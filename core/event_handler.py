from abc import ABC, abstractclassmethod
import pygame 
from sys import exit

pygame.init()

from resource_modules.enums import Direction

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
            key_name = key_name.replace(" ", "_") ## Replaces spaces with underscores

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
                    #print(pygame.key.name(event.key))
                    is_pressed = (event.type == pygame.KEYDOWN)
                    self.key_states[event.key] = is_pressed
            elif event.type == pygame.QUIT:
                quit_program()


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
        self._last_direction_pressed: Direction | None = None
        self._held_direction_stack: list[Direction] = []
        self.key_to_direction = {
        pygame.K_UP: Direction.UP,
        pygame.K_DOWN: Direction.DOWN,
        pygame.K_LEFT: Direction.LEFT,
        pygame.K_RIGHT: Direction.RIGHT,
        }
        super().__init__(keys_to_track)
    
    def arrow_key_to_direction(self, key: int):
        """
        Converts the arrow given arrow key pressed to the corresponding snake Direction 
        """
        print(key)
        if key not in self._keys_to_track: 
            raise ValueError("Non arrow key given")
        
        return self.key_to_direction[key]
    def record_input(self):
        """
        Updates key_states based on KEYDOWN/KEYUP events.
        """
        for event in pygame.event.get():
            if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                if event.key in self.key_states:
                    #print(pygame.key.name(event.key))
                    is_pressed = (event.type == pygame.KEYDOWN)
                    self.key_states[event.key] = is_pressed
                    direction = self.arrow_key_to_direction(event.key)
                    if is_pressed:
                        self._held_direction_stack.append(direction)
                    else: 
                        self._held_direction_stack.remove(direction)

                     
            elif event.type == pygame.QUIT:
                quit_program()


    def direction_key_pressed(self) -> Direction | None:
        """
        Returns the Direction of the currently pressed arrow key.
        The direction is the Direction enum.
        If no arrow key is pressed, returns None.
        """
        print(self._held_direction_stack)
        if self._held_direction_stack:
            return self._held_direction_stack[-1]
        return None
        # if self.right_arrow_key_is_pressed:
        #     return Direction.RIGHT
        # elif self.left_arrow_key_is_pressed:
        #     return Direction.LEFT
        # elif self.up_arrow_key_is_pressed:
        #     return Direction.UP
        # elif self.down_arrow_key_is_pressed:
        #     return Direction.DOWN
        return None


        