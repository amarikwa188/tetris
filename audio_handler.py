import pygame
from pygame.mixer import Sound


class AudioHandler:
    def __init__(self) -> None:
        self.click_sfx: Sound = Sound("assets/audio/click3.mp3")
        self.landed: Sound = Sound("assets/audio/landed.mp3")
        self.full_line: Sound = Sound("assets/audio/full_line.mp3")