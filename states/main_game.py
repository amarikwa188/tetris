import pygame
from pygame import Surface, Rect
from pygame.event import Event
from pygame.sprite import Sprite, Group

import game_settings as gs
from state_manager import StateManager


class Tetris:
    def __init__(self, screen: Surface, state_manager: StateManager) -> None:
        self.screen: Surface = screen
        self.state_manager: StateManager =  state_manager


    def run(self) -> None:
        self.screen.fill((230,230,230))
        self.draw_grid()

    def handle_events(self, event: Event) -> None:
        pass

    def draw_grid(self) -> None:
        for col in range(gs.grid_width):
            for row in range(gs.grid_height):
                col_pos: int = col * gs.tile_size + gs.grid_start_x
                row_pos: int = row * gs.tile_size + gs.grid_start_y

                # print(col_pos, row_pos) # (x,y) co-ordinates

                pygame.draw.rect(self.screen, (0,0,0),
                                 (col_pos, row_pos, gs.tile_size, gs.tile_size),
                                  1)

class Tetronimo:
    def __init__(self) -> None:
        pass


class Block(Sprite):
    def __init__(self, tetronimo: Tetronimo, position: tuple[int,int]) -> None:
        super().__init__()