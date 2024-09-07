import random as rng

import pygame
from pygame import Vector2
from pygame import Surface, Rect
from pygame.event import Event
from pygame.sprite import Sprite, Group

import game_settings as gs
from state_manager import StateManager


### GAME STATE CLASS ###
class Tetris:
    def __init__(self, screen: Surface, state_manager: StateManager) -> None:
        self.screen: Surface = screen
        self.state_manager: StateManager =  state_manager

        self.set_timer()

        self.block_group: Group = Group()
        self.tetromino: Tetronimo = Tetronimo(screen, self.block_group)


    def run(self) -> None:
        self.screen.fill((230,230,230))
        self.draw_grid()

        self.block_group.update()


    def handle_events(self, event: Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                menu_class = self.state_manager.get_state("main_menu")
                self.state_manager.set_state(menu_class(self.screen,
                                                        self.state_manager))
            if event.key == pygame.K_LEFT:
                self.tetromino.move('left')
            if event.key == pygame.K_RIGHT:
                self.tetromino.move('right')
        
        if event.type == self.user_event:
            self.tetromino.update()


    def draw_grid(self) -> None:
        for col in range(gs.grid_width):
            for row in range(gs.grid_height):
                col_pos: int = col * gs.tile_size + gs.grid_start_x
                row_pos: int = row * gs.tile_size + gs.grid_start_y

                pygame.draw.rect(self.screen, (0,0,0),
                                 (col_pos, row_pos, gs.tile_size, gs.tile_size),
                                  1)
                
    def set_timer(self) -> None:
        self.user_event: int = pygame.USEREVENT + 0
        pygame.time.set_timer(self.user_event, gs.TIME_INTERVAL)   


### PIECE CLASS ####
class Tetronimo:
    def __init__(self, screen: Surface, block_group: Group) -> None:
        self.screen: Surface = screen
        self.block_group: Group = block_group
        
        self.shape: str = rng.choice(list(gs.TETROMINOES))
        self.blocks: list[Block] = [Block(self.screen, pos, self.block_group) 
                             for pos in gs.TETROMINOES[self.shape]]
        
    def move(self, direction: str) -> None:
        move_direction: Vector2 = gs.MOVE_DIRECTIONS[direction.lower()]
        for block in self.blocks:
            block.pos += move_direction

    def update(self) -> None:
        self.move('down')


### INDIVIDUAL BLOCK CLASS ###
class Block(Sprite):
    def __init__(self, screen: Surface, position: tuple[int,int],
                 block_group: Group) -> None:
        super().__init__()
        self.screen: Surface = screen

        self.block_group: Group = block_group
        self.block_group.add(self)

        self.pos: Vector2 = Vector2(position) + gs.initial_offset

        self.image: Surface = Surface((gs.tile_size, gs.tile_size))
        self.image.fill("red")

        self.rect: Rect = self.image.get_rect()
        
    def update(self) -> None:
        self.rect.topleft = self.pos * gs.tile_size + \
                            Vector2(gs.grid_start_x, gs.grid_start_y)
        
        self.draw_block()

    def draw_block(self) -> None:
        if self.rect.top >= gs.grid_start_y:
            self.screen.blit(self.image, self.rect)

