import pygame
from pygame import Surface


def run_game() -> None:
    pygame.init()
    pygame.display.set_caption("Tetris")


if __name__ == "__main__":
    run_game()