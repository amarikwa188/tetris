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

        self.block_group: Group = Group()
        self.tetromino: Tetronimo = Tetronimo(self.block_group)


    def run(self) -> None:
        self.screen.fill((230,230,230))
        self.draw_grid()

        self.tetromino.update()

        self.block_group.update()
        self.block_group.draw(self.screen)


    def handle_events(self, event: Event) -> None:
        pass


    def draw_grid(self) -> None:
        for col in range(gs.grid_width):
            for row in range(gs.grid_height):
                col_pos: int = col * gs.tile_size + gs.grid_start_x
                row_pos: int = row * gs.tile_size + gs.grid_start_y

                pygame.draw.rect(self.screen, (0,0,0),
                                 (col_pos, row_pos, gs.tile_size, gs.tile_size),
                                  1)

class Tetronimo:
    def __init__(self, block_group: Group) -> None:
        self.block_group: Group = block_group
        
        self.shape: str = 'T'
        self.block: Block = [Block(pos, self.block_group) 
                             for pos in gs.TETROMINOES[self.shape]]

    def update(self) -> None:
        pass


class Block(Sprite):
    def __init__(self, position: tuple[int,int], block_group: Group) -> None:
        super().__init__()
        block_group.add(self)

        self.image: Surface = Surface((gs.tile_size, gs.tile_size))
        self.image.fill("red")

        self.rect: Rect = self.image.get_rect()
        self.rect.topleft = position[0] * gs.tile_size + gs.grid_start_x, \
                            position[1] * gs.tile_size + gs.grid_start_y
