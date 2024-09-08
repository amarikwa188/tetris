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
    """Represents an instance of a class."""
    def __init__(self) -> None:
        """Inititialize an instance of the game."""
        pygame.init()
        pygame.display.set_caption("Tetris")
        self.screen: Surface = pygame.display.set_mode((gs.screen_width,
                                                        gs.screen_height))
        self.clock: Clock = pygame.time.Clock()

        self.state_manager: StateManager = StateManager()
        self.initialize_states()
        self.state_manager.current_state = MainMenu(self.screen, self.state_manager)


    def run(self) -> None:
        """Run the game loop."""
        while True:
            self.clock.tick(gs.framerate)
            self.check_events()
            self.state_manager.current_state.run()
            pygame.display.update()


    def check_events(self) -> None:
        """Handle user input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            self.state_manager.current_state.handle_events(event)


    def initialize_states(self) -> None:
        """Create instances of the different game states."""
        self.main_menu: MainMenu = MainMenu
        self.main_game: Tetris = Tetris

        states: dict[str, Any] = {'main_menu': self.main_menu,
                                  'main_game': self.main_game}
        self.state_manager.states = states
        

if __name__ == "__main__":
    game: Game = Game()
    game.run()