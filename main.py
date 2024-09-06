import pygame
from pygame.time import Clock

import game_settings as gs
import game_functions as gf


def run_game() -> None:
    pygame.init()
    pygame.display.set_caption("Tetris")

    clock: Clock = pygame.time.Clock()

    while True:
        clock.tick(gs.FRAMERATE)
        gf.check_events()
        gs.current_state.run()
        gf.update_screen()


if __name__ == "__main__":
    run_game()