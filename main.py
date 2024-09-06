import sys
from typing import Any

import pygame
from pygame import Surface
from pygame.time import Clock

import game_settings as gs

from states.main_menu import MainMenu


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen: Surface = pygame.display.set_mode((gs.screen_width,
                                                        gs.screen_height))
        self.clock: Clock = pygame.time.Clock()

        self.current_state: Any = MainMenu(self.screen)


    def run(self) -> None:
        while True:
            self.clock.tick(gs.framerate)
            self.check_events()
            self.current_state.run()
            pygame.display.update()


    def check_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            self.current_state.handle_events(event)
        

if __name__ == "__main__":
    game: Game = Game()
    game.run()