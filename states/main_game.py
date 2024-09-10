import random as rng
from typing import Literal

import pygame
from pygame import Vector2
from pygame import Surface, Rect
from pygame.event import Event
from pygame.sprite import Sprite, Group
from pygame.font import Font

import game_settings as gs
from state_manager import StateManager
from audio_handler import AudioHandler


### GAME STATE CLASS ###
class Tetris:
    """Represents the tetris game state."""
    def __init__(self, screen: Surface, state_manager: StateManager,
                 audio_handler: AudioHandler) -> None:
        """
        Initialize an instance of the tetris game scene.

        :param screen: the game screen.
        :param state_manager: a reference to the state manager.
        """
        self.screen: Surface = screen
        self.state_manager: StateManager =  state_manager
        self.audio_handler: AudioHandler = audio_handler

        self.bg_color: tuple[int,int,int] = gs.DARKBLUE
        self.ui_font: Font = pygame.font.Font("assets/fonts/gameboy.ttf", 20)

        self.score: int = 0

        self.set_timer()

        self.block_group: Group = Group()
        self.field_array: list[list[Block | Literal[0]]] = \
            self.get_field_array()
        self.tetromino: Tetronimo = Tetronimo(screen, self.block_group, self)
        self.next_tetronimo: Tetronimo = \
            Tetronimo(screen, self.block_group, self, False)

        self.game_paused: bool = False
        self.game_over: bool = False
        self.create_pause_screen()
        self.create_end_screen()


    def run(self) -> None:
        """
        Run the tetris game state.
        """
        if not self.game_over:
            self.screen.fill(self.bg_color)
            self.draw_grid()
            self.draw_ui()
        
            if not self.game_paused:
                pygame.mouse.set_visible(False)

                self.block_group.update()

                self.check_tetronimo_landed()

                self.check_full_lines()

            for block in self.block_group.sprites():
                block.draw_block()

            if self.game_paused:
                pygame.mouse.set_visible(True)
                self.display_pause_screen()
        
        if self.game_over:
            pygame.mouse.set_visible(True)
            self.display_end_screen()


    def handle_events(self, event: Event) -> None:
        """
        Handle user input.

        :param event: the given user event.
        """
        if event.type == pygame.KEYDOWN and not self.game_over:
            if not self.game_paused:
                if event.key == pygame.K_LEFT:
                    self.tetromino.move('left')
                if event.key == pygame.K_RIGHT:
                    self.tetromino.move('right')
                if event.key == pygame.K_SPACE:
                    self.tetromino.rotate()
                if event.key == pygame.K_DOWN:
                    pygame.time.set_timer(self.user_event,
                                          gs.FAST_TIME_INTERVAL)

            if event.key == pygame.K_ESCAPE:
                self.audio_handler.pause_click.play()
                self.game_paused = not self.game_paused
        
        if event.type == self.user_event and not self.game_paused:
            self.tetromino.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos: tuple[int,int] = pygame.mouse.get_pos()

            if self.game_paused:
                if self.resume_alt_rect.collidepoint(pos):
                    self.game_paused = False
                    self.audio_handler.pause_click.play()
                elif self.menu_alt_rect.collidepoint(pos):
                    self.audio_handler.pause_click.play()
                    menu_class = self.state_manager.get_state("main_menu")
                    self.state_manager.set_state(menu_class(self.screen,
                                                        self.state_manager,
                                                        self.audio_handler))
                    

    def reset_game(self) -> None:
        """
        Start a new game.
        """
        self.__init__(self.screen, self.state_manager, self.audio_handler)
            

    def draw_grid(self) -> None:
        """
        Draw the playing area to the screen.
        """
        for col in range(gs.grid_width):
            for row in range(gs.grid_height):
                col_pos: int = col * gs.tile_size + gs.grid_start_x
                row_pos: int = row * gs.tile_size + gs.grid_start_y

                pygame.draw.rect(self.screen, gs.GREY,
                                 (col_pos, row_pos, gs.tile_size,
                                  gs.tile_size), 1)
                
        pygame.draw.rect(self.screen, gs.WHITE,
                         (gs.grid_start_x, gs.grid_start_y,
                         gs.tile_size * gs.grid_width,
                         gs.tile_size * gs.grid_height), 2)
        

    def draw_ui(self) -> None:
        """
        Draw the game ui to the screen.
        """
        self.display_next_block()
        self.display_score()

    
    def create_end_screen(self) -> None:
        self.end_screen: Surface = Surface((gs.screen_width,
                                            gs.screen_height))
        self.end_screen_rect: Rect =self.end_screen.get_rect()
        self.end_screen_rect.center = (gs.screen_width//2,
                                       gs.screen_height//2)

        game_over_font: Font = pygame.font.Font("assets/fonts/gameboy.ttf",
                                                40)
        
        self.over_text: Surface = game_over_font.render("GAME OVER", 
                                                             True,
                                                             gs.WHITE)
        self.over_rect: Rect = self.over_text.get_rect()
        self.over_rect.center = (gs.screen_width//2, 200)

        

        
    
    def display_end_screen(self) -> None:
        self.end_screen.fill(gs.DARKBLUE)
        self.screen.blit(self.end_screen, self.end_screen_rect)

        self.screen.blit(self.over_text, self.over_rect)
        

    def create_pause_screen(self) -> None:
        # main background surface
        self.pause_screen: Surface = Surface((gs.screen_width,
                                             gs.screen_height))
        
        self.pause_screen_rect: Rect = self.pause_screen.get_rect()
        self.pause_screen_rect.center = (gs.screen_width//2,
                                         gs.screen_height//2)
        
        # pause font
        pause_font: Font = pygame.font\
                            .Font("assets/fonts/gameboy.ttf", 50)
        
        self.pause_text_image: Surface = pause_font\
                        .render("PAUSED", True, gs.WHITE)
        self.pause_text_rect: Rect = self.pause_text_image.get_rect()
        self.pause_text_rect.center = (gs.screen_width//2+10, 200)
        
        # options text
        self.options_font: Font = pygame.font\
                            .Font("assets/fonts/gameboy.ttf", 20)
        
        ## resume
        self.resume_image: Surface = self.options_font.render("RESUME", True,
                                                              gs.WHITE)
        self.resume_rect: Rect = self.resume_image.get_rect()
        self.resume_rect.center = (gs.screen_width//2, 270)

        self.resume_alt_image: Surface = self.options_font.render("-RESUME-",
                                                                  True,
                                                                  gs.WHITE)
        self.resume_alt_rect: Rect = self.resume_alt_image.get_rect()
        self.resume_alt_rect.center = (gs.screen_width//2, 270)

        # menu
        self.menu_image: Surface = self.options_font.render("MENU", True,
                                                            gs.WHITE)
        self.menu_rect: Rect = self.menu_image.get_rect()
        self.menu_rect.center = (gs.screen_width//2, 320)

        self.menu_alt_image: Surface = self.options_font.render("-MENU-", 
                                                                True,
                                                                gs.WHITE)
        self.menu_alt_rect: Rect = self.menu_alt_image.get_rect()
        self.menu_alt_rect.center = (gs.screen_width//2, 320)
        

    def display_pause_screen(self) -> None:
        self.pause_screen.fill(gs.BLACK)
        self.pause_screen.set_alpha(220)

        self.screen.blit(self.pause_screen, self.pause_screen_rect)
        self.screen.blit(self.pause_text_image, self.pause_text_rect)

        pos: tuple[int,int] = pygame.mouse.get_pos()
        if self.resume_rect.collidepoint(pos):
            self.screen.blit(self.resume_alt_image, self.resume_alt_rect)
        else:
            self.screen.blit(self.resume_image, self.resume_rect)

        if self.menu_rect.collidepoint(pos):
            self.screen.blit(self.menu_alt_image, self.menu_alt_rect)
        else:
            self.screen.blit(self.menu_image, self.menu_rect)


    def display_next_block(self) -> None:
        """
        Display the next block.
        """
        # display 'next' text
        next_text_image: Surface = self.ui_font.render("NEXT", True, gs.WHITE)
        next_text_rect: Rect = next_text_image.get_rect(center=(317, 80))
        self.screen.blit(next_text_image, next_text_rect)

        # draw bounding box around the block
        next_rect: Rect = Rect(0,0, 100, 100)
        next_rect.center = (315, 150)

        pygame.draw.rect(self.screen, gs.WHITE, next_rect, 2, 7)

        # draw the appropriate tetronimo
        next_image: Surface = pygame.image\
                    .load(f"assets/game/{self.next_tetronimo.shape}.png")
        next_image_rect: Rect = next_image.get_rect(center=(315,150))
        self.screen.blit(next_image, next_image_rect)

    
    def display_score(self) -> None:
        """
        Display the current score.
        """
        # display 'score' text
        score_text_image: Surface = self.ui_font.render("SCORE", True,
                                                        gs.WHITE)
        score_text_rect: Rect = score_text_image.get_rect(center=(317, 305))
        self.screen.blit(score_text_image, score_text_rect)

        # draw bounding rectangle
        score_rect: Rect = Rect(0,0, 120, 70)
        score_rect.center = (315, 360)

        pygame.draw.rect(self.screen, gs.WHITE, score_rect, 2, 7)

        # display score
        score_image: Surface = self.ui_font.render(f"{self.score:03d}", True,
                                                   gs.WHITE)
        score_rect: Rect = score_image.get_rect(center=(315, 360))
        self.screen.blit(score_image, score_rect)
                

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
            if self.is_game_over():
                self.game_over = True
                self.display_end_screen()
            else:
                self.score += 10
                self.audio_handler.landed.play()
                pygame.time.set_timer(self.user_event, gs.TIME_INTERVAL)
                self.put_blocks_in_array()
                self.next_tetronimo.current = True
                self.tetromino = self.next_tetronimo
                self.next_tetronimo = Tetronimo(self.screen,
                                                self.block_group, self, False)


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
                self.audio_handler.full_line.play()
                self.score += 100
                for block in current_line:
                    block.alive = False
                    block = 0
            else:
                row -= 1


    def is_game_over(self) -> bool:
        """
        Check when the game is over.

        :return: True -> game over, False -> not game over.
        """
        if self.tetromino.blocks[0].pos.y == gs.initial_offset[1]:
            return True


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
        :param current: whether this tetronimo object is in play.
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