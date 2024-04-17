from enum import Enum
import socketio
from GameRoom import GameRoom, GameStatus, SideColor
import chess
import json

# Player modes enum
class PlayerMode(Enum):
    STANDARD = 1 # Standard multiplayer game with two players on different devices/clients
    BOARD_TWO_PLAYER = 2 # Two players on the same physical board
    # For BOARD_TWO_PLAYERS the opponent will be set by username on the room creation

class GameHelper:
    def __init__(self, sio: socketio.Client, server_url: str):
        self.sio = sio
        self.server_url = server_url
        self._game_over = False
        self._game_started = False
        self._room = None
        self.white = True
        self.last_move = None
        self._authenticated = False

    # Create a room
    def create_room(self, mode = PlayerMode.STANDARD, opponent_username = None):
        self.sio.emit('create_room', data={'player_mode': mode.value, 'opponent': opponent_username, 'side': 'white'})

    def get_connetion_status(self):
        return self.sio.connected

    def run(self):
        self.sio.connect(self.server_url, headers = None)
        return self.sio.connected
    
    def player_joined(self, room_owner, room_id, room_opponent):
        if self._room is None or self._room.room_id != room_id:
            self._room = GameRoom(room_owner)
            self._room.room_id = room_id
            self._room.player_mode = PlayerMode.STANDARD   
        self._room.room_opponent = room_opponent
        self._game_started = True           
    
    def is_game_started(self):
        return self._game_started
    
    def piece_move(self, fen):
        print(f'Piece move: {fen}')
        Nf3 = self._room.get_move(fen)
        if Nf3 is None:
            return {'status': 'error', 'message': 'Invalid move'}
        print(f'Pushing move: {Nf3}')
        self._room.game.push(Nf3)
        self.validate_outcome()
        return_data = {'room_id': self._room.room_id, 'move': {'fen': self._room.game.fen()}}
        self.last_move = None
        self.sio.emit('piece_move_notify', return_data, room=self._room.room_id)
        return {'status': 'success', 'data': return_data}
    
    def validate_outcome(self):
        outcome = self._room.game.outcome()
        if outcome is not None:
            self._game_over = True
            if outcome.termination == chess.Termination.CHECKMATE:
                if outcome.winner == chess.WHITE:
                    self._room.game_winner = self._room.room_owner
                    self._room.game_loser = self._room.room_opponent
                    self._room.end_game(winnerSide = SideColor.WHITE)
                else:
                    self._room.game_winner = self._room.room_opponent
                    self._room.game_loser = self._room.room_owner
                    self._room.end_game(winnerSide = SideColor.BLACK)
            else:
                self._room.game_draw = True
            self._room.game_status = GameStatus.ENDED
    
    def get_move(self):
        return self.last_move

    def room_created(self, data):
        print(data.room_id)
        print(f'Room created: {data}')
        d = json.loads(data)
        print(f'Room data loaded: {d}')
        self._room = GameRoom(d['room_owner'])
        self._room.room_id = d['room_id']
        self._room.player_mode = PlayerMode(d['player_mode'])
        self.sio.emit('subscribe_to_room', data={'room_id': self._room.room_id})
        if self._room.player_mode == PlayerMode.BOARD_TWO_PLAYER:
            print('Room created for two players on the same board')
            self._room.add_opponent('Board_player_2')
            self._game_started = True

    def set_authenticated(self):
        self._authenticated = True

    def move_piece(self, move):
        Nf3 = chess.Move.from_uci(move['source'] + move['target'])
        self._room.game.push(Nf3)
        self.validate_outcome()
        self.last_move = move

    def login(self, username, password):
        self.sio.emit('login', data={'username': username, 'password': password})

    def reset(self):
        print('Full reset of game board')
        self._game_over = False
        self._game_started = False
        self._room = None
        self.white = True
        self.last_move = None
        self._authenticated = False
        self.sio.disconnect()

helper: GameHelper = None

def room_create_callback(data):
    '''
    This function is called when the server responds on the room_create emit

    Args:
        data (dict): The data returned from the server if format: {'status': str(success|error), 'message': str, 'data': dict(GameRoom object.. look the server code for more info)}
    '''
    if data['status'] == 'success':
        helper.room_created(data)
    
    print('room_create_callback:', data)

    