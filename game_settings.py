from pygame import Vector2

# screen dimensions
screen_width: int = 400
screen_height: int = 500

# framerate
framerate: int = 60

# game stats
tile_size: int = 20

# grid dimensions
grid_width: int = 10
grid_height: int = 20
grid_size: tuple[int,int] = (grid_width, grid_height)

grid_start_x: int = 25
grid_start_y: int = 50

# tetronimo data
initial_offset: Vector2 = Vector2(grid_width//2, 0)
MOVE_DIRECTIONS: dict[str, Vector2] = {'left': Vector2(-1,0),
                                       'right': Vector2(1,0),
                                       'down': Vector2(0,1)}

TETROMINOES: dict[str, list[tuple[int,int]]] = {'T': [(0,0),(-1,0),(1,0),(0,-1)],
                                                'O': [(0,0),(0,-1),(1,0),(1,-1)],
                                                'J': [(0,0),(-1,0),(0,-1),(0,-2)],
                                                'L': [(0,0),(1,0),(0,-1),(0,-2)],
                                                'I': [(0,0),(0,1),(0,-1),(0,-2)],
                                                'S': [(0,0),(-1,0),(0,-1),(1,-1)],
                                                'Z': [(0,0),(1,0),(0,-1),(-1,-1)],}

## handle block movement 
TIME_INTERVAL: int = 200 # milliseconds
FAST_TIME_INTERVAL: int = 10