from Network.network import PlayerMode
import socketio
import GameRoom
import chess

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
        self.sio.emit('create_room', data={'mode': mode.value, 'opponent': opponent_username}, callback = self.room_create_callback)

    def get_connetion_status(self):
        return self.sio.connected

    def run(self):
        self.sio.connect(self.server_url, headers = None)
        return self.sio.connected
    
    def player_joined(self, room_owner, room_id, room_opponent):
        self._room = GameRoom(room_owner)
        self._room.room_id = room_id
        self._room.room_opponent = room_opponent
        if self._room.opponent is None:
            return 
        self._game_started = True
    
    def is_game_started(self):
        return self._game_started
    
    def piece_move(self, fen):
        Nf3 = self._room.get_move(fen)
        self._room.game.push(Nf3)
        return_data = {'room_id': self._room.room_id, 'move': {'fen': self._room.game.fen()}}
        self.last_move = None
        self.sio.emit('piece_move_notify', return_data, room=self._room.room_id)
        return {'status': 'success', 'data': return_data}
    
    def get_move(self):
        return self.last_move

    def room_created(self, data):
        room_data = data['data']
        self._room = GameRoom(room_data['room_owner'])
        self._room.room_id = room_data['room_id']
        self.sio.emit('subscribe_to_room', data={'room_id': self._room.room_id})
        if self._room.player_mode == PlayerMode.BOARD_TWO_PLAYER:
            print('Room created for two players on the same board')
            self._room.add_opponent('Board_player_2')
            self.player_joined(self._room.room_owner, self._room.room_id, self.__room.room_opponent)

    def set_authenticated(self):
        self._authenticated = True

    def move_piece(self, move):
        Nf3 = chess.Move.from_uci(move['source'] + move['target'])
        self._room.game.push(Nf3)
        self.last_move = move

    def login(self, username, password):
        self.sio.emit('login', data={'username': username, 'password': password})

    def reset(self):
        self._game_over = False
        self._game_started = False
        self._room = None
        self.white = True
        self.last_move = None
        self._authenticated = False