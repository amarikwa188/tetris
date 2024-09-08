import random as rng
from typing import Literal

import pygame
from pygame import Vector2
from pygame import Surface, Rect
from pygame.event import Event
from pygame.sprite import Sprite, Group

import game_settings as gs
from state_manager import StateManager


### GAME STATE CLASS ###
class Tetris:
    """Represents the tetris game state."""
    def __init__(self, screen: Surface, state_manager: StateManager) -> None:
        """
        Initialize an instance of the tetris game scene.

        :param screen: the game screen.
        :param state_manager: a reference to the state manager.
        """
        self.screen: Surface = screen
        self.state_manager: StateManager =  state_manager

        self.set_timer()

        self.block_group: Group = Group()
        self.field_array: list[list[Block | Literal[0]]] = \
            self.get_field_array()
        self.tetromino: Tetronimo = Tetronimo(screen, self.block_group, self)


    def run(self) -> None:
        """
        Run the tetris game state.
        """
        self.screen.fill((230,230,230))
        self.draw_grid()

        self.block_group.update()

        self.check_tetronimo_landed()


    def handle_events(self, event: Event) -> None:
        """
        Handle user input.

        :param event: the given user event.
        """
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
        """
        Draw the playing area to the screen.
        """
        for col in range(gs.grid_width):
            for row in range(gs.grid_height):
                col_pos: int = col * gs.tile_size + gs.grid_start_x
                row_pos: int = row * gs.tile_size + gs.grid_start_y

                pygame.draw.rect(self.screen, (0,0,0),
                                 (col_pos, row_pos, gs.tile_size,
                                  gs.tile_size), 1)
                

    def put_blocks_in_array(self) -> None:
        """
        Store the location of landed blocks in the field array to track
        collisions with other blocks.
        """
        for block in self.tetromino.blocks:
            x,y = int(block.pos.x), int(block.pos.y)
            self.field_array[x][y] = block


    def get_field_array(self) -> None:
        """
        Create a two-dimensional array to store the status of cells on the
        grid.
        """
        return [[0 for _ in range(gs.grid_height)]
                for _ in range(gs.grid_width)]

                
    def set_timer(self) -> None:
        """
        Create a user event to handle the movement of the blocks. 
        """
        self.user_event: int = pygame.USEREVENT + 0
        pygame.time.set_timer(self.user_event, gs.TIME_INTERVAL)   


    def check_tetronimo_landed(self) -> None:
        """
        Store the blocks of a tetronimo in the field array and load a new one
        when it has landed.
        """
        if self.tetromino.landed:
            self.put_blocks_in_array()
            self.tetromino = Tetronimo(self.screen, self.block_group, self)


### PIECE CLASS ####
class Tetronimo:
    def __init__(self, screen: Surface, block_group: Group,
                 tetris: Tetris) -> None:
        self.tetris: Tetris = tetris

        self.screen: Surface = screen
        self.block_group: Group = block_group
        
        self.shape: str = rng.choice(list(gs.TETROMINOES))
        self.blocks: list[Block] = [Block(self.screen, pos, self.block_group,
                                          self) 
                                    for pos in gs.TETROMINOES[self.shape]]
        
        self.landed: bool = False
        
    def move(self, direction: str) -> None:
        move_direction: Vector2 = gs.MOVE_DIRECTIONS[direction.lower()]

        new_block_positions = [block.pos + move_direction for block in self.blocks]
        is_collide: bool = self.is_collide(new_block_positions)

        if not self.landed:
            if not is_collide:
                for block in self.blocks:
                    block.pos += move_direction
            elif direction == 'down':
                self.landed =  True

    def update(self) -> None:
        self.move('down')

    def is_collide(self, block_positions: list[Vector2]) -> bool:
        return any(map(Block.is_collide, self.blocks, block_positions))



### INDIVIDUAL BLOCK CLASS ###
class Block(Sprite):
    def __init__(self, screen: Surface, position: tuple[int,int],
                 block_group: Group, tetronimo: Tetronimo) -> None:
        super().__init__()
        self.screen: Surface = screen

        self.tetronimo: Tetronimo = tetronimo

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

    def is_collide(self, position: Vector2) -> bool:
        x,y = int(position.x), int(position.y)
        if 0 <= x < gs.grid_width and y < gs.grid_height and \
            (y < 0 or not self.tetronimo.tetris.field_array[x][y]):
            return False
        return True

