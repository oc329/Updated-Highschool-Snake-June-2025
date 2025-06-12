import os
import pygame
import time 
pygame.mixer.init()

from game_state_manager import GameStateManager

game_state_manager = GameStateManager()

game_state_manager.run()