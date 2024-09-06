import pygame, sys

import game_settings as gs


def check_events() -> None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def update_screen() -> None:
    gs.current_state.draw_ui()
    pygame.display.update()