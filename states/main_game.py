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

        self.bg_color: tuple[int,int,int] = (15,0,57)

        self.set_timer()

        self.block_group: Group = Group()
        self.field_array: list[list[Block | Literal[0]]] = \
            self.get_field_array()
        self.tetromino: Tetronimo = Tetronimo(screen, self.block_group, self)
        self.next_tetronimo: Tetronimo = \
            Tetronimo(screen, self.block_group, self, False)

        self.game_paused: bool = False
        


    def run(self) -> None:
        """
        Run the tetris game state.
        """
        if self.game_paused:
            self.bg_color = (255,255,255)
        else:
            self.bg_color = (15,0,57)

        self.screen.fill(self.bg_color)
        self.draw_grid()

        if not self.game_paused:
            self.block_group.update()

            self.check_tetronimo_landed()

            self.check_full_lines()

        for block in self.block_group.sprites():
            block.draw_block()


    def handle_events(self, event: Event) -> None:
        """
        Handle user input.

        :param event: the given user event.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                menu_class = self.state_manager.get_state("main_menu")
                self.state_manager.set_state(menu_class(self.screen,
                                                        self.state_manager))
            
            if not self.game_paused:
                if event.key == pygame.K_LEFT:
                    self.tetromino.move('left')
                if event.key == pygame.K_RIGHT:
                    self.tetromino.move('right')
                if event.key == pygame.K_SPACE:
                    self.tetromino.rotate()
                if event.key == pygame.K_DOWN:
                    pygame.time.set_timer(self.user_event, gs.FAST_TIME_INTERVAL)

            if event.key == pygame.K_ESCAPE:
                self.game_paused = not self.game_paused
        
        if event.type == self.user_event and not self.game_paused:
            self.tetromino.update()


    def draw_grid(self) -> None:
        """
        Draw the playing area to the screen.
        """
        for col in range(gs.grid_width):
            for row in range(gs.grid_height):
                col_pos: int = col * gs.tile_size + gs.grid_start_x
                row_pos: int = row * gs.tile_size + gs.grid_start_y

                pygame.draw.rect(self.screen, (150,150,150),
                                 (col_pos, row_pos, gs.tile_size,
                                  gs.tile_size), 1)
                
        pygame.draw.rect(self.screen, (255,255,255),
                         (gs.grid_start_x, gs.grid_start_y,
                         gs.tile_size * gs.grid_width,
                         gs.tile_size * gs.grid_height), 2)
                

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
            pygame.time.set_timer(self.user_event, gs.TIME_INTERVAL)
            self.put_blocks_in_array()
            self.tetromino = Tetronimo(self.screen, self.block_group, self)


    def check_full_lines(self) -> None:
        """
        Check for any completed rows.
        """
        row: int = gs.grid_height - 1

        for cell in range(gs.grid_height-1, -1, -1):
            current_line: list = []
            for line in range(gs.grid_width):
                current_line.append(self.field_array[line][cell])
                self.field_array[line][row] = self.field_array[line][cell]

                if self.field_array[line][cell]:
                    self.field_array[line][row].pos = Vector2(line, cell)
            
            if all(current_line):
                for block in current_line:
                    block.alive = False
                    block = 0
            else:
                row -= 1


### PIECE CLASS ####
class Tetronimo:
    """Represents an instance of a tetronimo"""
    def __init__(self, screen: Surface, block_group: Group,
                 tetris: Tetris, current: bool=True) -> None:
        """
        Initializes a tetronimo object.

        :param screen: the game screen.
        :param block_group: a sprite group containing all the blocks of
        the tetronimo.
        :param tetris: the game instance this tetronimo belongs to.
        """
        self.tetris: Tetris = tetris

        self.screen: Surface = screen
        self.block_group: Group = block_group
        
        self.shape: str = rng.choice(list(gs.TETROMINOES))
        self.blocks: list[Block] = [Block(self.screen, pos, self.block_group,
                                          self) 
                                    for pos in gs.TETROMINOES[self.shape]]
        
        self.landed: bool = False
        self.current: bool = current
        

    def move(self, direction: str) -> None:
        """
        Move the tetronimo one place in a given direction.

        :param direction: the direction to move 
        """
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
        """
        Move the tetronimo down.
        """
        self.move('down')


    def rotate(self) -> None:
        """
        Rotate the tetronimo by 90 degrees.
        """
        if self.shape == "O":
            return 
        
        pivot_pos: Vector2 = self.blocks[0].pos
        new_block_positions: list[Vector2] = [block.rotate(pivot_pos)
                                              for block in self.blocks]

        if not self.is_collide(new_block_positions):
            for idx, block in enumerate(self.blocks):
                block.pos = new_block_positions[idx]


    def is_collide(self, block_positions: list[Vector2]) -> bool:
        """
        Check if the tetronimo has collided with anything.

        :param block_positions: the positions of all blocks in the tetronimo.
        :return: whether any blocks have collided.
        """
        return any(map(Block.is_collide, self.blocks, block_positions))



### INDIVIDUAL BLOCK CLASS ###
class Block(Sprite):
    """Represents an instance of a single block."""
    def __init__(self, screen: Surface, position: tuple[int,int],
                 block_group: Group, tetronimo: Tetronimo) -> None:
        """
        Initialize a block object.

        :param screen: the game screen.
        :param position: the top left x and y grid coordinates.
        :param block_group: a sprite group containing all the blocks in a 
        specific tetronimo.
        :param tetronimo: the tetronimo object this block belongs to. 
        """
        super().__init__()
        self.screen: Surface = screen

        self.tetronimo: Tetronimo = tetronimo

        self.block_group: Group = block_group
        self.block_group.add(self)

        self.pos: Vector2 = Vector2(position) + gs.initial_offset
        self.next_pos: Vector2 = Vector2(position) + \
            gs.next_block_display_offset

        self.image: Surface = pygame.image.load("assets/game/block.png")

        self.rect: Rect = self.image.get_rect()

        self.alive: bool = True
        

    def update(self) -> None:
        """
        Update the position of the block and draw it to the screen
        """
        self.set_block_position()
        self.is_alive()


    def set_block_position(self) -> None:
        """
        Set the position of the rect.
        """
        pos: Vector2 = [self.next_pos, self.pos][self.tetronimo.current]
        self.rect.topleft = pos * gs.tile_size + \
                            Vector2(gs.grid_start_x, gs.grid_start_y)


    def rotate(self, pivot_pos: Vector2) -> None:
        """
        Rotate the block by 90 degrees.

        :param pivot_pos: the axis around which the block is rotated.
        """
        translated: Vector2 = self.pos - pivot_pos
        rotated: Vector2 = translated.rotate(90.0)
        return rotated + pivot_pos


    def draw_block(self) -> None:
        """
        Draw the block to the screen.
        """
        if self.rect.top >= gs.grid_start_y:
            self.screen.blit(self.image, self.rect)


    def is_collide(self, position: Vector2) -> bool:
        """
        Check whether a block has collided with the sides of the grid
        or other blocks.

        :param position: the position of the block.
        :return: whether the block has collided.
        """
        x,y = int(position.x), int(position.y)
        if 0 <= x < gs.grid_width and y < gs.grid_height and \
            (y < 0 or not self.tetronimo.tetris.field_array[x][y]):
            return False
        return True
    

    def is_alive(self) -> None:
        """
        Check if th block has been removed from the grid.
        """
        if not self.alive:
            self.kill()