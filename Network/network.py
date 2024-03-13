import socketio
import jwt

sio = socketio.Client()
server_url = 'http://localhost:5000'

class WebSocketController:

    BOARD_SINGLE_PLAYER = 'single_player'
    BOARD_MULTI_PLAYER = 'multi_player'

    def __init__(self):
        self.sio = sio
        self.game_over = False
        self.game_started = False

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
        sio.connect(server_url, headers = {'Cookies': 'AuthToken:' + data['token']})
        sio.emit('try_join_game', data = {})

    def login(self, username, password, opponent=None, mode=BOARD_SINGLE_PLAYER):
        sio.emit('login', data={'username': username, 'password': password, 'mode': mode, 'opponent': opponent})

    def get_connetion_status(self):
        return sio.connected

    def run(self):
        sio.connect(server_url, headers = None)
        return sio.connected