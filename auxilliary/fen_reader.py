import chess

'''
A FEN string:
rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
Split by " ":
1. Board. lowercase = black. Upper case = WHITE. 1-8 digits are empty spaces. / is new rank.
2. w for white move, b for black move.
3. Caslting availability. K: white king side, Q: white queen side. Same for black.
4. En passant target square. No target is "-". 
5. Halfmove clock used for fifty move clock.
6. Fullmove number, number of full moves. Starts at 1 and is incremented afte Blacks move.

Definitions:
Open: An open move is defined as a move along a path of squares that all are empty.
Closed: A move along a path of squares that contains one or more pieces, and must therefore follow the edge. 
'''
# ASSUMES servers knows board state. 

# TODO: Note that only "special moves" such as castling, graveyard and horses require "threading" the pieces
########################### FEN:
    
def parse_fen(chess_fen: str):
    board, move, castling, passant, halfmove, fullmove = chess_fen.split(" ")
    halfmove = int(halfmove)
    fullmove = int(fullmove)
    return board, move, castling, passant, halfmove, fullmove
    
########################## END FEN

########################## PATH:

# Move identifiers
NORMAL = "normal"
HORSE = "horse"
CASTLING = "castling"
GRAVEYARD = "graveyard"
D2G = "distance2graveyard"

# Board frame
COLUMN = ["@", "A", "B", "C", "D", "E", "F", "G", "H", "I"]
ROW = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
COLUMN_OFFSET = 1
ROW_OFFSET = 2
# Edge frame 
E_COLUMN = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
E_ROW = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]



def get_path(board: str, old_pos: str, new_pos: str, move_type: str):
    """Return a path from old position to new position. Move_type=='normal' will assume path is open.
    Move_type == 'horse', 'castling' or 'graveyard' will assume a path is blocked, and will return a path along the edges.

    Args:
        board (str): FEN string, board part.
        old_pos (str): Typically G5 or g5
        new_pos (str): Typically G5 or g5
        move_type (str): normal, horse, castling or graveyard

    Returns:
        list[tuple[int, int] | str]: Path
    """
    path = []
    old_pos = old_pos
    new_pos = new_pos
    
    old_coord = position_to_coords(old_pos)
    new_coord = position_to_coords(new_pos)
    
    min_dist, is_diagonal = get_open_distance(old_coord, new_coord)
    # Normal move:
    if move_type == NORMAL:
        path = get_direct_path(old_coord, new_coord, is_diagonal)
    elif HORSE or CASTLING or GRAVEYARD:
        path = get_displaced_path(old_coord, new_coord, move_type)
    return path


def get_direct_path(old_coord: tuple[int, int], new_coord: tuple[int, int], is_diagonal: bool):
    """Assumes no blocking pieces in path. Does not include position of self.
    Assumes that path is either a diagonal or a straight run.

    Args:
        old_coord (tuple[int, int]): _description_
        new_coord (tuple[int, int]): _description_
        is_diagonal (bool): _description_

    Returns:
        _type_: _description_
    """
    letters = []
    numbers = []
    if is_diagonal:
        letters = [COLUMN[i] for i in range(old_coord[0], new_coord[0])]
        numbers = [ROW[i]-ROW_OFFSET+1 for i in range(old_coord[1], new_coord[1])]
    else:  # straight
        if old_coord[0] - new_coord[0] == 0: # straight along letter axis
            letters = [COLUMN[old_coord[0]-1] for _ in range(old_coord[1], new_coord[1])]
            numbers = [ROW[i]-ROW_OFFSET+1 for i in range(old_coord[1], new_coord[1])]
        elif old_coord[1] - new_coord[1] == 0: # straight along number axis
            letters = [COLUMN[i] for i in range(old_coord[0], new_coord[0])]
            numbers = [ROW[old_coord[1]-ROW_OFFSET] for _ in range(old_coord[0], new_coord[0])]
            
    path = [(letters[i], numbers[i]) for i in range(len(letters))]
    # If self is needed, uncomment line:
    # path = coords_to_position(old_coord) + path
    return path
    
def get_displaced_path(old_coord: tuple[int, int], new_coord: tuple[int, int] | str, special_identifier: str):
    # Get the displace path of a special move.
    
    # Line defined as: B5B6, the line between B5 and B6.
    # Edge case: B8B9, the line between B6 and out of bounds.
    old_pos = coords_to_position(old_coord)
    new_pos = coords_to_position(new_coord)
    
    if special_identifier == GRAVEYARD:  # either old or new is in graveyard. Old if pawn switch to new piece
        # TODO:
        # find path to edge
        first_edge = start_edgerun(old_coord, new_coord)
        last_edge = start_edgerun(new_coord, old_coord)
        edge_path = straight_edgerun(first_edge, last_edge)
        # add distance 2 graveyard when passing over "@" or "I".
        edge_path = add_graveyard_jump(edge_path)
        enter_pos = end_edgerun(new_coord)
        # Path will look somewhat like: [2Edge, edge1, edge2, edge3, dist2grave, edge3, 2Spot]
        path = [first_edge] + edge_path + [enter_pos] # TODO want first edge?
        print("The piece was yoted")
    # horse and castling is the same in the eyes of this algo....
    elif special_identifier == HORSE or special_identifier == CASTLING:  # new_pos is actual location
        first_edge = start_edgerun(old_coord, new_coord)
        last_edge = start_edgerun(new_coord, old_coord)
        edge_path = straight_edgerun(first_edge, last_edge)
        enter_pos = end_edgerun(new_coord)
        path = [first_edge] + edge_path + [enter_pos]
    return path


def start_edgerun(start_coord, end_coord) -> tuple[int, int]:  # 1. Find corner
    """Find the best edgepoint to start at.
    Assume that best start point is always closest to end point

    Returns:
        tuple[int, int]: edge in edge-frame
    """
    dx = abs(start_coord[0] - end_coord[0])
    dy = abs(start_coord[1] - end_coord[1])
    edge = []
    if dy >= 0 and dx >= 0: # top left
        direction = "tl"
    elif dy >= 0 and dx < 0: # top right
        direction = "tr"
    elif dy < 0 and dx >= 0: # bot left
        direction = "bl"
    elif dy < 0 and dx < 0: # bot right
        direction = "br"
    edge = b2e_frame(start_coord, direction=direction)
    return edge
    
def straight_edgerun(start_edge: tuple[int, int], end_edge: tuple[int, int]):  # 2 and 3. find straights.
    """Returns the path along the edges. Does not handle D2G.

    Args:
        start_edge (tuple[int, int]):
        end_edge (tuple[int, int]):

    Returns:
        list of edges
    """
    # Get a straight
    dx = abs(start_edge[0] - end_edge[0])
    sgnx = int((-start_edge[0]+end_edge[0])/dx)
    dy = abs(start_edge[1] - end_edge[1])
    sgny = int((-start_edge[1]+end_edge[1])/dy)
    
    def move_dir(start_edge, dx, sgnx, dy, sgny, dirn):
        if dirn: #x (letters)
            path = [(start_edge[0]+i*sgnx, start_edge[1]) for i in range(1, dx + 1)]
        else: #y
            path = [(start_edge[0], start_edge[1]+i*sgny) for i in range(1, dy + 1)]    
        return path
    
    if dx >= dy: # choose to move dy first
        path_gen = [0, 1]
    else: # choose to move dx first
        path_gen = [1, 0]
    path1 = move_dir(start_edge, dx, sgnx, dy, sgny, path_gen[0])
    path2 = move_dir(path1[-1], dx, sgnx, dy, sgny, path_gen[1])
    return path1 + path2

# Add D2G if applicable
def add_graveyard_jump(path: list[tuple[int, int]]) -> list[tuple[int, int]]:
    new_path = path
    for i in range(len(path)-1):
        if (path[i][0] == 1 and path[i+1][0] == 2) or \
            (path[i][0] == 2 and path[i+1][0] == 1) or \
            (path[i][0] == 10 and path[i+1][0] == 11) or \
            (path[i][0] == 11 and path[i+1][0] == 10):
            new_path = new_path[:i] + [D2G] + new_path[i:]
    return new_path
    
        
def end_edgerun(new_coord):  # exit edge
    return new_coord
    
    

########### HELPER FUNCS:

def position_to_coords(pos: str):
    """ 

    Args:
        pos (str): _description_
    """
    col = ord(pos[0].upper()) - ord('A') + 1 + COLUMN_OFFSET
    row = int(pos[1]) + ROW_OFFSET
    return (col, row)


def coords_to_position(coord: tuple[int, int]):
    col = chr(coord[0]+ord('A')-1- COLUMN_OFFSET)
    row = coord[1] - ROW_OFFSET
    return col + repr(row)
    

def get_open_distance(coord1, coord2) -> tuple[int, bool]:
    diagonal = False
    dx = abs(coord1[0] - coord2[0])
    dy = abs(coord1[1] - coord2[1])
    total = dx + dy
    if dx == dy: # diagonal move
        total = dx
        diagonal = True
    return total, diagonal


def b2e_frame(b_coord: tuple[int, int], direction: str):
    c_ofs = 0
    r_ofs = 0
    if direction == "tl":
        c_ofs = 0
        r_ofs = 1
    elif direction == "tr":
        c_ofs = 1
        r_ofs = 1
    elif direction == "bl":
        c_ofs = 0
        r_ofs = 0
    elif direction == "br":
        c_ofs = 1
        r_ofs = 0
    return (b_coord[0]+c_ofs, b_coord[1]+r_ofs)

    
############## END PATH
    
# BOARD FRAME:   
#        |d| : distance between board and grave       
#   Grave|d|Board for drawing "edges"|d|    
#   -1 0  1 2 3 4 5 6 7 8 9 10 11
#    > ?  @ A B C D E F G H  I  J  K
#         9 
#         8 
#         7 
#         6 
#         5 
#         4 
#         3 
#         2 
#         1 
#         0 
#   
# EDGE FRAME:    
#   -1 0 1 | 2 3 4 5 6 7 8 9 0 | 1 2 3 
#          0
#          9 
#          8 
#          7 
#          6 
#          5 
#          4 
#          3 
#          2 
#          1 
#          0 
#

if __name__ == '__main__':
    p = get_path("", "B3", "?7", move_type=GRAVEYARD)
    print(p)
    
    p = get_path("", "?7", "B3", move_type=GRAVEYARD)
    print(p)
    
    p = get_path("", ">2", "J7", move_type=GRAVEYARD)
    print(p)
    
