import pygame
from pygame import Surface, Rect


class Button:
    def __init__(self, screen: Surface, x: int, y: int, image: str) -> None:
        self.screen: Surface = screen

        self.image: Surface = pygame.image.load(image)
        self.rect: Rect = self.image.get_rect(center=(x,y))

    def draw_button(self) -> None:
        self.screen.blit(self.image, self.rect)