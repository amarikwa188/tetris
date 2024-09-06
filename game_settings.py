######### IMPORTS ##########
from typing import Any

import pygame
from pygame import Surface

from states.main_menu import MainMenu
############################

# screen dimensions
SCREEN_WIDTH: int = 500
SCREEN_HEIGHT: int = 500

# screen
screen: Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# track game state
current_state: Any = MainMenu(screen)

# framerate
FRAMERATE: int = 60