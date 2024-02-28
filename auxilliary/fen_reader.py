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
class FEN_Reader:
    # Prob not needed, delete.
    _current_board_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    
    def __init__(self) -> None:
        pass
    
    
def parse_fen(chess_fen: str):
    board, move, castling, passant, halfmove, fullmove = chess_fen.split(" ")
    halfmove = int(halfmove)
    fullmove = int(fullmove)
    return board, move, castling, passant, halfmove, fullmove
    
########################## END FEN

########################## PATH:

# Move identifiers
HORSE = "horse"
CASTLING = "castling"
GRAVEYARD = "graveyard"
D2G = "distance2graveyard"

COLUMN = ["@", "A", "B", "C", "D", "E", "F", "G", "H", "I"]
ROW = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
COLUMN_OFFSET = 1
ROW_OFFSET = 2


#COLUMN = ["A", "B", "C", "D", "E", "F", "G", "H"]
#ROW = [1, 2, 3, 4, 5, 6, 7, 8]

def check_for_open_path(board: str, old_pos: str, new_pos: str):
    """Check if there is an open path from current position to new position.

    Args:
        board (str): FEN string, board part.
        old_pos (str): Typically G5 or g5
        new_pos (str): Typically G5 or g5

    Returns:
        _type_: _description_
    """
    open_path = []
    old_pos = old_pos
    new_pos = new_pos
    
    old_coord = position_to_coords(old_pos)
    new_coord = position_to_coords(new_pos)
    
    special_move = False
    min_dist, is_diagonal = get_open_distance(old_coord, new_coord)
    # Normal move:
    if not special_move:
        path = get_direct_path(old_pos, new_pos, is_diagonal)
    elif special_move:
        path = get_displaced_path(old_pos, new_pos)
    return open_path


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
    new_pos = coords_to_position(new_pos)
    
    if special_identifier == GRAVEYARD:  # either old or new is in graveyard. Old if pawn switch to new piece
        # TODO:
        # find path to edge
        # add distance 2 graveyard when passing over "@" or "I".
        # find path to spot
        
        
        # Path will look somewhat like: [2Edge, edge1, edge2, edge3, dist2grave, edge3, 2Spot]
        
        print("The piece was yoted")
        
    # horse and castling is the same in the eyes of this algo....
    elif special_identifier == HORSE or special_identifier == CASTLING:  # new_pos is actual location
        pass
    path = ""
    return path


def start_edgerun(start_coord, end_coord):
    """Find the best edgepoint to start at.
    Assume that best start point is always closest to end point

    Returns:
        _type_: _description_
    """
    dx = abs(start_coord[0] - end_coord[0])
    dy = abs(start_coord[1] - end_coord[1])
    edge = []
    if dx >= dy:  # prioritize horizontal
        if start_coord[1] - end_coord[1] >= 0: # end lower
            # "move to upper edge"
            up = (start_coord[0], start_coord[1]+1)
            edge = [start_coord, up]
        elif start_coord[1] - end_coord[1] < 0: # end higher
            # "move to lower edge"
            down = (start_coord[0], start_coord[1]-1)
            edge = [start_coord, down]
    else:  # prioritize vertical
        if start_coord[0] - end_coord[0] >= 0: # end left
            # "move to left edge"
            left = (start_coord[0]-1, start_coord[1])
            edge = [start_coord, left]
        elif start_coord[0] - end_coord[0] < 0: # end right
            # "move to right edge"
            right = (start_coord[0]+1, start_coord[1])
            edge = [start_coord, right]
    return edge
        
    
    

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
    col = chr(coord[0]-1- COLUMN_OFFSET)
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
    
############## END PATH
    
    
#        |d| : distance between board and grave       
#   Grave|d|Board for drawing "edges"|d|    
#    0 1  2 3 4 5 6 7 8 9 10 11 12 13
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