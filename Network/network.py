import socketio
import jwt

sio = socketio.Client()
server_url = 'http://localhost:5000'
BOARD_SINGLE_PLAYER = 'single_player'
BOARD_MULTI_PLAYER = 'multi_player'

class WebSocketController:
    def __init__(self):
        self.sio = sio

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
    def player_joined(data):
        print('Player joined:', data)

    @sio.on('authenticated')
    def authenticated(data):
        print('Authenticated:', data)
        sio.emit('try_join_game', data = {'AuthToken': data['token'], 'Board': BOARD_SINGLE_PLAYER})

    def run(self):
        sio.connect(server_url, headers = None)
        sio.emit('login', data={'Board': BOARD_SINGLE_PLAYER})
        sio.wait()