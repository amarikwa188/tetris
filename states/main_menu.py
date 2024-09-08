import sys
import pygame
from pygame import Surface
from pygame.event import Event

import game_settings as gs
from state_manager import StateManager

from button import Button


class MainMenu:
    """Represents the main menu state."""
    def __init__(self, screen: Surface, state_manager: StateManager) -> None:
        """
        Initialize an instance of the main menu.

        :param screen: the game screen.
        :param state_manager: the state manager.
        """
        self.screen: Surface = screen
        self.state_manager: StateManager = state_manager

        self.clicked: bool = False

        # main menu bg
        self.background: Surface = pygame.image\
            .load("assets/ui/main_menu_bg.png")

        # main menu buttons
        self.start_button: Button = Button(screen, gs.screen_width//2, 330,
                                           "assets/ui/play_wide.png",
                                           "assets/ui/play_wide_H.png", 0.9)

        self.quit_button: Button = Button(screen, gs.screen_width//2, 370,
                                          "assets/ui/exit.png",
                                          "assets/ui/exit_H.png", 0.8)

    
    def run(self) -> None:
        """
        Run the menu screen.
        """
        self.screen.blit(self.background, (0,0))

        self.start_button.draw_button()
        self.quit_button.draw_button()


    def handle_events(self, event: Event) -> None:
        """
        Handle user input.

        :param event: the given user event.
        """
        if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
            self.clicked = True

            pos: tuple[int,int] = pygame.mouse.get_pos()

            if self.start_button.rect.collidepoint(pos):
                self.game_class = self.state_manager.get_state("main_game")
                self.state_manager.set_state(self.game_class(self.screen,
                                                             self.state_manager))

            if self.quit_button.rect.collidepoint(pos):
                sys.exit()
                

        if event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False
            