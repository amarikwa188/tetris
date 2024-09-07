# screen dimensions
screen_width: int = 400
screen_height: int = 500

# framerate
framerate: int = 60

# game stats
tile_size: int = 20

grid_width: int = 10
grid_height: int = 20
grid_size: tuple[int,int] = (grid_width, grid_height)

grid_start_x: int = 25
grid_start_y: int = 50

TETROMINOES: dict[str, list[tuple[int,int]]] = {'T': [(0,0),(-1,0),(1,0),(0,-1)],
                                                'O': [(0,0),(0,-1),(1,0),(1,-1)],
                                                'J': [(0,0),(-1,0),(0,-1),(0,-2)],
                                                'L': [(0,0),(1,0),(0,-1),(0,-2)],
                                                'I': [(0,0),(0,1),(0,-1),(0,-2)],
                                                'S': [(0,0),(-1,0),(0,-1),(1,-1)],
                                                'Z': [(0,0),(1,0),(0,-1),(-1,-1)],}