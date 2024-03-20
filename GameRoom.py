from enum import Enum
import uuid
import chess
from json import JSONEncoder
import json

class GameStatus(Enum):
    WAITING = 1
    STARTED = 2
    ENDED = 3

class PlayerMode(Enum):
    STANDARD = 1 # Standard multiplayer game with two players on different devices/clients
    BOARD_TWO_PLAYER = 2 # Two players on the same physical board
    # For BOARD_TWO_PLAYERS the opponent will be set by username on the room creation

class GameRoom:
    def __init__(self, room_owner):
        self.room_id = str(uuid.uuid1())
        self.room_owner = room_owner
        self.room_opponent = None
        self.observers = []
        self.game = chess.Board()
        self.game_status = GameStatus.WAITING
        self.game_winner = None
        self.game_loser = None
        self.player_mode = PlayerMode.STANDARD

    def add_opponent(self, opponent):
        # Check if there is already an opponent in the room
        if self.room_opponent is  None:
            self.room_opponent = opponent
            return True
        else :
            return False
        
    def add_observer(self, observer):
        # Check if the observer is already in the room
        for obser in self.observers :
            if obser.id == observer.id :
                return False 
        self.observers.append(observer)
        return True


    def start_game(self):
        self.game = chess.Board()
        self.game_status = GameStatus.STARTED

    def end_game(self, winner, loser, draw):
        self.game_winner = winner
        self.game_loser = loser
        self.game_draw = draw
        self.game_status = GameStatus.ENDED

    def get_game_state(self):
        return self.game_status

    def get_game_winner(self):
        return self.game_winner

    def get_game_loser(self):
        return self.game_loser

    def get_game_draw(self):
        return self.game_draw

    def get_game_winner(self):
        return self.game_winner

    def get_game_loser(self):
        return self.game_loser

    def get_game_draw(self):
        return self.game_draw

    def get_players(self):
        return self.room_owner, self.room_opponent

    def get_room_id(self):
        return self.room_id

    def get_room_owner(self):
        return self.room_owner

    def get_game(self):
        return self.game
    
    def get_player_mode(self):
        return self.player_mode
    
    def set_player_mode(self, player_mode):
        self.player_mode = player_mode
    
    def serialize(self):
        return json.dumps(self, cls=GameRoomJSONEncoder)
    
class GameRoomJSONEncoder(JSONEncoder):
    def default(self, obj): 
        if isinstance(obj, GameRoom):
            return {
                "room_id": obj.room_id,
                "room_owner": obj.room_owner.serialize() if obj.room_owner else None,
                "room_opponent": obj.room_opponent.serialize() if obj.room_opponent else None,
                "observers": [observer.serialize() for observer in obj.observers],
                "game_status": obj.game_status.value,
                "game_winner": obj.game_winner,
                "game_loser": obj.game_loser,
                "game": obj.game.fen() if obj.game else None,
                "player_mode": obj.player_mode
            }
        # Let the base class default method raise the TypeError
        return JSONEncoder.default(self, obj)
    
nums = {1:"a", 2:"b", 3:"c", 4:"d", 5:"e", 6:"f", 7:"g", 8:"h"}
def get_uci(board1, board2, who_moved):
    str_board = str(board1).split("\n")
    str_board2 = str(board2).split("\n")
    move = ""
    flip = False
    if who_moved == "w":
        for i in range(8)[::-1]:
            for x in range(15)[::-1]:
                if str_board[i][x] != str_board2[i][x]:
                    if str_board[i][x] == "." and move == "":
                        flip = True
                    move+=str(nums.get(round(x/2)+1))+str(9-(i+1))
    else:
        for i in range(8):
            for x in range(15):
                if str_board[i][x] != str_board2[i][x]:
                    if str_board[i][x] == "." and move == "":
                        flip = True
                    move+=str(nums.get(round(x/2)+1))+str(9-(i+1))
    if flip:
        move = move[2]+move[3]+move[0]+move[1]
    return move