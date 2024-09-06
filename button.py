import pygame
from pygame import Surface, Rect


class Button:
    def __init__(self, screen: Surface, x: int, y: int, image: str, 
                 hover_image: str='') -> None:
        self.screen: Surface = screen

        self.main_image: Surface = pygame.image.load(image)

        if hover_image:
            self.hover_image: Surface = pygame.image.load(hover_image)
        else:
            self.hover_image = None

        self.image: Surface = self.main_image

        self.rect: Rect = self.image.get_rect(center=(x,y))
    

    def hover(self) -> None:
        pos: tuple[int,int] = pygame.mouse.get_pos()

        if self.hover_image:
            if self.rect.collidepoint(pos) and self.image != self.hover_image:
                self.image = self.hover_image

        if not self.rect.collidepoint(pos) and self.image != self.main_image:
            self.image = self.main_image


    def draw_button(self) -> None:
        self.hover()
        self.screen.blit(self.image, self.rect)