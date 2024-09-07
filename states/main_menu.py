import sys
import pygame
from pygame import Surface
from pygame.event import Event

import game_settings as gs
from state_manager import StateManager
from states.main_game import Tetris

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

        # main menu buttons
        self.start_button: Button = Button(screen, gs.screen_width//2, 300,
                                           "assets/ui/sprite_0.png",
                                           "assets/ui/sprite_1.png")
        
        self.options_button: Button = Button(screen, gs.screen_width//2, 350,
                                             "assets/ui/options_button.png",
                                             "assets/ui/options_button_H.png")
        self.quit_button: Button = Button(screen, gs.screen_width//2, 400,
                                          "assets/ui/quit_button.png",
                                          "assets/ui/quit_button_H.png")
        
        self.options_screen_active: bool = False

        # options screen buttons
        self.back_button: Button = Button(screen, gs.screen_width//2, 450,
                                          "assets/ui/back_button.png",
                                          "assets/ui/back_button_H.png")

    
    def run(self) -> None:
        """
        Run the menu screen.
        """
        self.screen.fill((100,100,150))

        if not self.options_screen_active:
            # main menu
            self.start_button.draw_button()
            self.options_button.draw_button()
            self.quit_button.draw_button()
        else:
            # options menu
            self.back_button.draw_button()


    def handle_events(self, event: Event) -> None:
        """
        Handle user input.

        :param event: the given user event.
        """
        if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
            self.clicked = True

            pos: tuple[int,int] = pygame.mouse.get_pos()

            # main menu buttons
            if self.start_button.rect.collidepoint(pos) and \
                not self.options_screen_active:
                self.game_class = self.state_manager.get_state("main_game")
                self.state_manager.set_state(self.game_class(self.screen,
                                                             self.state_manager))

            if self.options_button.rect.collidepoint(pos):
                self.options_screen_active = True

            if self.quit_button.rect.collidepoint(pos) and \
                not self.options_screen_active:
                sys.exit()

            # options screen buttons
            if self.back_button.rect.collidepoint(pos) and \
                self.options_screen_active:
                self.options_screen_active = False
                

        if event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False
            