import socketio
from enum import Enum
from game_helper import GameHelper

sio = socketio.Client()
server_url = 'http://chess.datagonia.no:5000/'
helper = GameHelper(sio, server_url)

# Player modes enum
class PlayerMode(Enum):
    STANDARD = 1 # Standard multiplayer game with two players on different devices/clients
    BOARD_TWO_PLAYER = 2 # Two players on the same physical board
    # For BOARD_TWO_PLAYERS the opponent will be set by username on the room creation

class WebSocketController:

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
    def message(data, sid):
        print('message', sid, data)
    
    @sio.on('room_created')
    def room_created(data):
        print('Room created:', data)

    @sio.on('room_updated_')
    def room_updated(data):
        if data['room_opponent'] is not None:
            helper.player_joined(data['room_owner'], data['room_id'], data['room_opponent'])
        print('Room updated:', data)
 
    @sio.on('authenticated')
    def authenticated(data):
        print('Authenticated:', data)
        helper.set_authenticated()
        sio.disconnect()
        sio.connect(server_url, headers={'Cookies': 'AuthToken:' + data['token']})

    @sio.on('piece_moved_')
    def piece_moved(data):
        print('Piece moved:', data)
        move = data['move']
        helper.move_piece(move)

    # Callback for the created room
    def room_create_callback(data):
        '''
        This function is called when the server responds on the room_create emit

        Args:
            data (dict): The data returned from the server if format: {'status': str(success|error), 'message': str, 'data': dict(GameRoom object.. look the server code for more info)}
        '''
        if data['status'] == 'success':
            helper.room_created(data)
        
        print('room_create_callback:', data)

def get_helper():
    return helper