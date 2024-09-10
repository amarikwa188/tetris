import sys
import pygame
from pygame import Surface, Rect
from pygame.event import Event
from pygame.font import Font

import game_settings as gs
from state_manager import StateManager
from audio_handler import AudioHandler

from button import Button


class MainMenu:
    """Represents the main menu state."""
    def __init__(self, screen: Surface, state_manager: StateManager,
                 audio_handler: AudioHandler) -> None:
        """
        Initialize an instance of the main menu.

        :param screen: the game screen.
        :param state_manager: the state manager.
        """
        self.screen: Surface = screen
        self.state_manager: StateManager = state_manager
        self.audio_handler: AudioHandler = audio_handler

        # main menu bg
        self.background: Surface = pygame.image\
            .load("assets/ui/main_menu_bg.png")

        # main menu buttons
        self.start_button: Button = Button(screen, gs.screen_width//2, 290,
                                           "assets/ui/play.png",
                                           "assets/ui/play_H.png", 0.9,
                                           self.audio_handler.pause_click)

        self.quit_button: Button = Button(screen, gs.screen_width//2, 340,
                                          "assets/ui/exit.png",
                                          "assets/ui/exit_H.png", 0.7,
                                          self.audio_handler.pause_click)
        
        self.credits: Font = pygame.font.Font("assets/fonts/gameboy.ttf", 12)

    
    def run(self) -> None:
        """
        Run the menu screen.
        """
        self.screen.blit(self.background, (0,0))

        self.draw_logo(gs.screen_width//2 - 3, 180)

        self.start_button.draw_button()
        self.quit_button.draw_button()

        self.draw_credits()

    def handle_events(self, event: Event) -> None:
        """
        Handle user input.

        :param event: the given user event.
        """
        if self.start_button.clicked():
            self.game_class = self.state_manager.get_state("main_game")
            self.state_manager.set_state(self.game_class(self.screen,
                                                         self.state_manager,
                                                         self.audio_handler))

        if self.quit_button.clicked():
            sys.exit()


    def draw_logo(self, x: int, y: int) -> None:
        """
        Draw the title logo to the screen.

        :param x: the center x position.
        :param y: the center y position.
        """
        self.logo_image: Surface = pygame.image.load("assets/ui/logo.png")
        self.logo_rect: Rect = self.logo_image.get_rect(center=(x,y))
        self.screen.blit(self.logo_image, self.logo_rect)


    def draw_credits(self) -> None:
        """
        Render the credits on the screen.
        """
        image: Surface = self.credits.render("A.AMARIKWA", True,
                                             gs.WHITE)
        rect: Rect = image.get_rect()
        rect.centerx = gs.screen_width//2
        rect.centery = gs.screen_height - 105

        self.screen.blit(image, rect)
            