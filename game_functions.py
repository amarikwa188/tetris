import pygame, sys


def check_events() -> None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def update_screen() -> None:
    pygame.display.update()