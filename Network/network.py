import socketio
import chess
from enum import Enum
from GameRoom import GameRoom, get_uci

sio = socketio.Client()
server_url = 'http://chess.datagonia.no:5000/'

# Player modes enum
class PlayerMode(Enum):
    STANDARD = 1 # Standard multiplayer game with two players on different devices/clients
    BOARD_TWO_PLAYER = 2 # Two players on the same physical board
    # For BOARD_TWO_PLAYERS the opponent will be set by username on the room creation

class WebSocketController:

    def __init__(self):
        self.sio = sio
        self._game_over = False
        self._game_started = False
        self._room = None
        self.white = True
        self.last_move = None
        self._authenticated = False

    # Invoked when the connection is established
    @sio.event
    def connect():
        print("I'm connected!")

    # Invoked when the connection is failed
    @sio.event
    def connect_error(data):
        print("The connection failed!")

    # Invoked when the connection is disconnected
    @sio.event
    def disconnect():
        print("I'm disconnected!")

    @sio.on('message')
    def message(self, sid, data):
        print('message', sid, data)
    
    @sio.on('room_created')
    def room_created(data):
        print('Room created:', data)

    @sio.on('room_updated_')
    def room_updated(self, data):
        self._room = GameRoom(data.get('room_owner'))
        self._room.room_id = data.get('room_id')
        self._room.room_opponent = data.get('room_opponent')
        if self._room.opponent is not None:
            self.player_joined()
        print('Room updated:', data)
 
    @sio.on('authenticated')
    def authenticated(self, data):
        print('Authenticated:', data)
        self._authenticated =True
        sio.disconnect()
        sio.connect(server_url, headers={'Cookies': 'AuthToken:' + data['token']})

    @sio.on('piece_moved')
    def piece_moved(self, data):
        print('Piece moved:', data)
        move = data['move']
        Nf3 = chess.Move.from_uci(move['source'] + move['target'])
        self._room.game.push(Nf3)
        self.last_move = move

    def login(self, username, password):
        sio.emit('login', data={'username': username, 'password': password})

    # Callback for the created room
    def room_create_callback(data):
        '''
        This function is called when the server responds on the room_create emit

        Args:
            data (dict): The data returned from the server if format: {'status': str(success|error), 'message': str, 'data': dict(GameRoom object.. look the server code for more info)}
        '''
        if data['status'] == 'success':
            room_created(data)
        
        print('room_create_callback:', data)

    # Create a room
    def create_room(self, mode = PlayerMode.STANDARD, opponent_username = None):
        sio.emit('create_room', data={'mode': mode.value, 'opponent': opponent_username}, callback = self.room_create_callback)

    def get_connetion_status(self):
        return sio.connected

    def run(self):
        sio.connect(server_url, headers = None)
        return sio.connected
    
    def player_joined(self):
        self._game_started = True
    
    def is_game_started(self):
        return self._game_started
    
    def piece_move(self, fen, color):
        uci = get_uci(self._room.game.fen(), fen, color)
        Nf3 = chess.Move.from_uci(uci)

        move = {'source': chess.square_name(Nf3.from_square), 
                'target': chess.square_name(Nf3.to_square), 
                'piece': chess.piece_name(Nf3.promotion)}

        # check if the move is valid
        if Nf3 not in self._room.game.legal_moves:
            return {'status': 'error', 'message': f"{Nf3} is not a legal move."}
        self._room.game.push(Nf3)
        return_data = {'move': move, 'fen': self._room.game.fen()}
        self.last_move = None
        sio.emit('piece_moved', return_data, room=self._room.room_id)
        return {'status': 'success', 'data': return_data}
    
    def get_move(self):
        return self.last_move

def room_created(self, data):
    room_data = data['data']
    self._room = GameRoom(room_data['room_owner'])
    self._room.room_id = room_data['room_id']
    sio.emit('subscribe_to_room', data={'room_id': self._room.room_id})
    if self._room.player_mode == PlayerMode.BOARD_TWO_PLAYER:
        print('Room created for two players on the same board')
        self._room.add_opponent('Board_player_2')
        self.player_joined()