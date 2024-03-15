import socketio
import jwt
from enum import Enum

sio = socketio.Client()
server_url = 'http://localhost:5000'

# Player modes enum
class PlayerMode(Enum):
    STANDARD = 1 # Standard multiplayer game with two players on different devices/clients
    BOARD_TWO_PLAYER = 2 # Two players on the same physical board
    # For BOARD_TWO_PLAYERS the opponent will be set by username on the room creation

class WebSocketController:

    def __init__(self):
        self.sio = sio
        self.game_over = False
        self.game_started = False

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

    def emit(self, event, data, sid=None):
        if sid:
            self.sio.emit(event, data, room=sid)
        else:
            self.sio.emit(event, data)
    
    @sio.on('room_created')
    def room_created(data):
        print('Room created:', data)

    @sio.on('player_joined')
    def player_joined(self, data):
        self.game_started = True
    
    def is_game_started(self):
        return self.game_started
 
    @sio.on('authenticated')
    def authenticated(data):
        print('Authenticated:', data)

        sio.disconnect()
        sio.connect(server_url, headers={'Cookies': 'AuthToken:' + data['token']})

    def login(self, username, password):
        sio.emit('login', data={'username': username, 'password': password})

    # Callback for the created room
    def room_create_callback(self, data):
        '''
        This function is called when the server responds on the room_create emit

        Args:
            data (dict): The data returned from the server if format: {'status': str(success|error), 'message': str, 'data': dict(GameRoom object.. look the server code for more info)}
        '''
        print('room_create_callback:', data)

    # Create a room
    def create_room(self, mode, opponent_username):
        sio.emit('create_room', data={'mode': mode, 'opponent': opponent_username}, callback = self.room_create_callback)

    def get_connetion_status(self):
        return sio.connected

    def run(self):
        sio.connect(server_url, headers = None)
        return sio.connected