import pygame
from pygame import Surface
from pygame.event import Event

import game_settings as gs
from state_manager import StateManager


class Tetris:
    def __init__(self, screen: Surface, state_manager: StateManager) -> None:
        self.screen: Surface = screen
        self.state_manager: StateManager =  state_manager

    def run(self) -> None:
        self.screen.fill((230,230,230))

    def handle_events(self, event: Event) -> None:
        pass