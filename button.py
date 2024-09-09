import pygame
from pygame import Surface, Rect


class Button:
    """Represents an instance of the button class."""
    def __init__(self, surface: Surface, x: int, y: int, image: str, 
                 hover_image: str='', scale: float=1.0) -> None:
        """
        Initialize a button object.

        :param surface: the surface where the button is rendered.
        :param x: the center x position of the button.
        :param y: the center y position of the button.
        :param image: the default image of the button.
        :param hover_image: the image of the button when the mouse is hovering
        over it. If none is entered, the default image is always used.
        :param scale: the scale of the button.
        """
        self.surface: Surface = surface

        self.main_image: Surface = pygame.image.load(image)
        

        if hover_image:
            self.hover_image: Surface = pygame.image.load(hover_image)
        else:
            self.hover_image = None

        self.scale_images(scale)

        self.image: Surface = self.main_image

        self.rect: Rect = self.image.get_rect(center=(x,y))

        self.button_clicked: bool = False


    def scale_images(self, scale: float) -> None:
        """
        Resize the button images according to the given scale.

        :param scale: the desired scale as a multiplier on the original
        image dimensions. A value of one results in the original image size.
        """
        self.main_image_width: int  = int(self.main_image.get_width() * scale)
        self.main_image_height: int = int(self.main_image.get_height() * scale)

        self.main_image_scaled: Surface = \
            pygame.transform.scale(self.main_image, (self.main_image_width,
                                                     self.main_image_height))
        self.main_image = self.main_image_scaled

        if self.hover_image:
            self.hover_image_width: int  = int(self.hover_image.get_width() \
                                               * scale)
            self.hover_image_height: int = int(self.hover_image.get_height() \
                                               * scale)

            self.hover_image_scaled: Surface = \
                pygame.transform.scale(self.hover_image, 
                                       (self.hover_image_width,
                                        self.hover_image_height))
            self.hover_image = self.hover_image_scaled
        

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


    def clicked(self) -> bool:
        """
        Check if the button has been clicked. The button registers as clicked
        when the left mouse button is released and the mouse is hovering over
        the button.

        :return: True -> clicked, False -> not clicked.
        """
        
        pos: tuple[int,int] = pygame.mouse.get_pos()

        mouse_pressed = pygame.mouse.get_pressed()[0] == 1

        if mouse_pressed and self.rect.collidepoint(pos) and \
             not self.button_clicked:
            self.button_clicked = True

        if not self.rect.collidepoint(pos):
            self.button_clicked = False

        if not mouse_pressed and self.button_clicked and \
             self.rect.collidepoint(pos):
            self.button_clicked = False
            return True
        
        return False