from enum import Enum
from dataclasses import dataclass
from time import sleep
from chess import Board

from Motion.motioncontroller import MotionController
from Network.network import WebSocketController
from auxilliary.boardIO import BoardIO


# Terminology: Server == External opponent
    # User == Physical player

    # Setup Logger
    ########### LOOP:
    # Check for incoming messages
    # (Send outgoing messages?)

    #== FSM?
    ### State: Initial state:
    #   Setup internet connection and threads...
    #   Enter Wait for user input
    #
    ### State: Wait for user input:
    #   Wait for user input...
    # 
    ### State: Wait for server move
    #   Be able to exit..?
    #   Still to health check (if safety is importantes)
    #   If two server players, do not enter user move mode.
    # 
    ### State: Wait for user to move
    #   Poll comp vision to know move is done? Or user hit btn to say I have moved?
    #   Send move to server
    #   Enter wait for server, if two user players do not enter wait for server
    #
    ### State: Board reset
    #   Somehow enter board reset
    #   Reset board
    #   Enter wait for user input
    #== END FSM
    # Let pcu breathe...
    ########### END LOOP


class states(Enum):
    INITIALIZE = 0
    WAIT_FOR_SERVER_CONNECTION = 1  # Not needed in miminal goal
    WAIT_FOR_USER_INPUT = 2
    WAIT_FOR_SERVER_MOVE = 3  # Not need in minimal goal
    WAIT_FOR_USER_MOVE = 4  # only operation state in minimal goal
    FINISHED = 5
    
@dataclass(init=True,eq=True)
class FSM():
    state: int
    
    def set_state(self, state: int):
        self.state = state

def initialize(fsm: FSM, bio: BoardIO)->tuple[FSM, BoardIO]:
    # nothing needs be done, except assert states?
    bio.reset()
    # TODO: ?
    # reset engine?
    # reset connection?
    # next state: wait for user input
    print('Board initialized')
    fsm.set_state(states.WAIT_FOR_USER_INPUT)
    return fsm, bio

# TODO:  DELETE
def wait_for_server_connection(fsm: FSM, ws: WebSocketController)->tuple[FSM, WebSocketController]:
    # Currently want:
    # ping server and check for answer.
    # Server good -> show user
    # Server bad -> show user
    # next state: wait for user input
    connected = ws.run()
    while not connected:
        sleep(1)
        connected = ws.get_connetion_status()

    print('Server connected')
    fsm.set_state(states.WAIT_FOR_USER_INPUT)
    
    # NOT a state -> subthread of socketController? some intervaltimer, just ping every 5 seconds?
    return fsm, ws


def wait_for_user_input(fsm: FSM, bio: BoardIO, ws: WebSocketController)->tuple[FSM, BoardIO, WebSocketController]:
    # What does the player want?
    if bio.started():
        ws.login('board_player_1', 'password')
    elif bio.extraed():
        # TODO: ...
        # Please do not mix the login functionality with the room creation functionality as we need to keep the logic for different functionalities in different clients relatively the same
        # 1. You should login first
        # 2. Then you should create a room
        #   2.1. You can use create_room(PlayerMode.BOARD_TWO_PLAYER, 'opponent_username') to create a room. The server will return:
        #       2.1.1. {status: 'success', message: 'Room created', data: GameRoom object}
        #       2.1.2. OR {status: 'error', message: 'User <opponent_username> is not found'}
        #       2.1.3. OR {status: 'error', message: 'User <opponent_username> is already in a room'}
        # 3. After the room is created, you should subscribe to the socket.io room by using the room_id from the GameRoom object in order to receive/send the game events for the specific room. Read (https://socket.io/docs/v3/rooms/) for more information about the socket rooms
        # 4. Then you can consider to start the game

        # Note: The room can be created with the following parameters as well:
        # create_room(PlayerMode.STANDARD, None) # For standard game mode (1 player vs 1 player) each player will have its own client board/web/vr (in case we implement the mooving part)
        
        # So.. instead of this:
        ws.login('board_player_1', 'password', opponent='board_player_2', mode=WebSocketController.BOARD_MULTI_PLAYER)
        # we should do only this:
        # ws.login('board_player_1', 'password')
        # And when the client is authenticated, the state machine should create the room like this:
        # ws.create_room(PlayerMode.BOARD_TWO_PLAYER, 'opponent_username')
        # and make sure that the status is 'success' before moving to the next state
        # Then subscribe to the room and start the game // We have't implemented 'socket rooms' in the server side yet. Soon we will plan and implement it.
        

    while not ws.is_game_started():
        sleep(1)

    print('Game started')
    fsm.set_state(states.WAIT_FOR_USER_MOVE)
    
    # Extended:
    # Find player == start btn..
    return fsm



def wait_for_user_move(fsm: FSM)->FSM:
    # when move is realized ( btn extra? ):
    #   validate move?
    #   if valid -> send move to server
    #   else notify user with led?
    # else:
    #   check for user disconnect/reset through new btn_start press 
    
    return