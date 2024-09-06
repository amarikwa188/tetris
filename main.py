import sys
from typing import Any

import pygame
from pygame import Surface
from pygame.time import Clock

import game_settings as gs

from state_manager import StateManager
from states.main_menu import MainMenu
from states.main_game import Tetris


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen: Surface = pygame.display.set_mode((gs.screen_width,
                                                        gs.screen_height))
        self.clock: Clock = pygame.time.Clock()

        self.state_manager: StateManager = StateManager()
        self.initialize_states()
        self.state_manager.current_state = self.main_menu


    def run(self) -> None:
        while True:
            self.clock.tick(gs.framerate)
            self.check_events()
            self.state_manager.current_state.run()
            pygame.display.update()


    def check_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            self.state_manager.current_state.handle_events(event)


    def initialize_states(self) -> None:
        self.main_menu: MainMenu = MainMenu(self.screen, self.state_manager)
        self.main_game: Tetris = Tetris(self.screen, self.state_manager)

        states: dict[str, Any] = {'main_menu': self.main_menu,
                                  'main_game': self.main_game}
        self.state_manager.states = states
        

if __name__ == "__main__":
    game: Game = Game()
    game.run()