import sys
import pygame
from pygame import Surface, Rect
from pygame.event import Event

import game_settings as gs
from state_manager import StateManager

from button import Button


class MainMenu:
    def __init__(self, screen: Surface, state_manager: StateManager) -> None:
        self.screen: Surface = screen
        self.state_manager: StateManager = state_manager

        self.start_button: Button = Button(screen, gs.screen_width//2, 300,
                                           "assets/ui/start_button.png",
                                           "assets/ui/start_button_H.png")
        self.options_button: Button = Button(screen, gs.screen_width//2, 350,
                                             "assets/ui/options_button.png",
                                             "assets/ui/options_button_H.png")
        self.quit_button: Button = Button(screen, gs.screen_width//2, 400,
                                          "assets/ui/quit_button.png",
                                          "assets/ui/quit_button_H.png")
        
        self.options_screen_active: bool = False

    
    def run(self) -> None:
        self.screen.fill((100,100,150))

        if not self.options_screen_active:
            # main menu
            self.start_button.draw_button()
            self.options_button.draw_button()
            self.quit_button.draw_button()
        else:
            # options menu
            pass


    def handle_events(self, event: Event) -> None:
        if event.type ==  pygame.MOUSEBUTTONDOWN:
            pos: tuple[int,int] = pygame.mouse.get_pos()

            if self.start_button.rect.collidepoint(pos) and \
                not self.options_screen_active:
                self.state_manager.current_state = \
                    self.state_manager.states['main_game']

            if self.options_button.rect.collidepoint(pos):
                self.options_screen_active = True

            if self.quit_button.rect.collidepoint(pos) and \
                not self.options_screen_active:
                sys.exit()