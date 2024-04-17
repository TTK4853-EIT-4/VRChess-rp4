import json
import socketio
from time import sleep
from game_helper import GameHelper

sio = socketio.Client()
server_url = 'http://77.71.71.125:5000/'
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
        d = json.loads(data)
        if d is not None:
            helper.room_created(d)
        else:
            helper.reset()

    @sio.on('room_updated_')
    def room_updated(data):
        d = json.loads(data)
        if d['room_opponent'] is not None:
            helper.player_joined(d['room_owner'], d['room_id'], d['room_opponent'])
        print('Room updated:', data)
 
    @sio.on('authenticated')
    def authenticated(data):
        print('Authenticated:', data)
        sio.disconnect()
        sio.sleep(2)
        sio.connect(server_url, wait_timeout=10, headers={'Cookie': 'AuthToken=' + data['token']})
        while not helper.get_connetion_status():
            sleep(1)
        helper.set_authenticated()
        

    @sio.on('piece_moved_')
    def piece_moved(data):
        print('Piece moved:', data)
        move = data['move']
        helper.move_piece(move)

    @sio.on('room_created_status_self')
    def room_created_status_self(data):
        print('Room created status self:', data)
        if data['status'] == 'success':
            helper.room_created(data['data'])
        else:
            helper.reset()

def get_helper():
    return helper