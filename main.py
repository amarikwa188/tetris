import pygame
from pygame import Surface

import game_settings as s


def run_game() -> None:
    pygame.init()
    pygame.display.set_caption("Tetris")

    screen: Surface = pygame.display.set_mode((s.SCREEN_WIDTH,
                                               s.SCREEN_HEIGHT))
    
    while True:
        pass


if __name__ == "__main__":
    run_game()