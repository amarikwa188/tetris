import pygame
from pygame import Surface, Rect


class Button:
    """Represents an instance of the button class."""
    def __init__(self, surface: Surface, x: int, y: int, image: str, 
                 hover_image: str='') -> None:
        """
        Initialize a button object.

        :param surface: the surface where the button is rendered.
        :param x: the center x position of the button.
        :param y: the center y position of the button.
        :param image: the default image of the button.
        :param hover_image: the image of the button when the mouse is hovering
        over it. If none is entered, the default image is always used.
        """
        self.surface: Surface = surface

        self.main_image: Surface = pygame.image.load(image)

        if hover_image:
            self.hover_image: Surface = pygame.image.load(hover_image)
        else:
            self.hover_image = None

        self.image: Surface = self.main_image

        self.rect: Rect = self.image.get_rect(center=(x,y))
    

    def hover(self) -> None:
        """
        Display the appropriate image depending on whether the mouse is
        hovering over the button or not.
        Note: This method is called within the draw_button() method.
        """
        pos: tuple[int,int] = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos) and self.image != self.hover_image:
            self.image = self.hover_image

        if not self.rect.collidepoint(pos) and self.image != self.main_image:
            self.image = self.main_image


    def draw_button(self) -> None:
        """
        Draw the button to the screen.
        """
        if self.hover_image:
            self.hover()
        self.surface.blit(self.image, self.rect)