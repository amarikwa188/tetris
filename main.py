import pygame
from pygame import Surface
from pygame.time import Clock

import game_settings as gs
import game_functions as gf


def run_game() -> None:
    pygame.init()
    pygame.display.set_caption("Tetris")

    screen: Surface = pygame.display.set_mode((gs.SCREEN_WIDTH,
                                               gs.SCREEN_HEIGHT))
    clock: Clock = pygame.time.Clock()
    
    while True:
        clock.tick(gs.FRAMERATE)
        gf.check_events()
        gf.update_screen()


if __name__ == "__main__":
    run_game()