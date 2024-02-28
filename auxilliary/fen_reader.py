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

COLUMN = ["A", "B", "C", "D", "E", "F", "G", "H"]
ROW = [1, 2, 3, 4, 5, 6, 7, 8]

# TODO: Parse FEN string
# TODO: If "open" route, give open route.
# TODO: If no open route possible, calculate a closed route.
# TODO: Note that only "special moves" such as castling, graveyard and horses require "threading" the pieces
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

    Args:
        old_coord (tuple[int, int]): _description_
        new_coord (tuple[int, int]): _description_
        is_diagonal (bool): _description_

    Returns:
        _type_: _description_
    """
    if is_diagonal:
        letters = [COLUMN[i] for i in range(old_coord[0], new_coord[0])]
        numbers = [ROW[i] for i in range(old_coord[1], new_coord[1])]
    else:  # straight
        if old_coord[0] - new_coord[0] == 0: # straight along letter axis
            letters = [COLUMN[old_coord[0]-1] for _ in range(old_coord[1], new_coord[1])]
            numbers = [ROW[i] for i in range(old_coord[1], new_coord[1])]
        elif old_coord[1] - new_coord[1] == 0: # straight along number axis
            letters = [COLUMN[i] for i in range(old_coord[0], new_coord[0])]
            numbers = [ROW[old_coord[1]-1] for _ in range(old_coord[0], new_coord[0])]
            
    path = [(letters[i], numbers[i]) for i in range(len(letters))]
    # If self is needed, uncomment line:
    # path = coords_to_position(old_coord) + path
    return path
    
def get_displaced_path(old_pos: str, new_pos: str):
    # Get the displace path of a special move.
    if new_pos == "graveyard":
        # find free graveyard spot.
        print("The piece was yoted")
    else:  # new_pos is actual location
        print("Horse, castling etc...")
    
    
    path = ""
    return path


def position_to_coords(pos: str):
    """A1 = (1, 1), H8 = (8, 8) 

    Args:
        pos (str): _description_
    """
    col = ord(pos[0].upper()) - ord('A') + 1
    row = int(pos[1])
    return (col, row)


def coords_to_position(coord: tuple[int, int]):
    col = chr(coord[0]-1)
    row = coord[1]
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
    
    
    