import socketio
from game_helper import GameHelper

sio = socketio.Client()
server_url = 'http://chess.datagonia.no:5000/'
helper = GameHelper(sio, server_url)

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

def get_helper():
    return helper