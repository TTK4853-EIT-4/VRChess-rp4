from enum import Enum
from dataclasses import dataclass
from time import sleep

from Motion.motioncontroller import MotionController
from auxilliary.boardIO import BoardIO, COLOR
from Camera.camera import CameraController
from GameRoom import GameStatus
from game_helper import GameHelper, PlayerMode


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
    # Initialize board
    bio.reset()
    print('Board initialized')
    fsm.set_state(states.WAIT_FOR_SERVER_CONNECTION)
    return fsm, bio

# TODO:  DELETE
def wait_for_server_connection(fsm: FSM, helper: GameHelper)->tuple[FSM, GameHelper]:
    # Wait for server connection
    connected = helper.run()
    while not connected:
        sleep(1)
        connected = helper.get_connetion_status()

    print('Server connected')
    fsm.set_state(states.WAIT_FOR_USER_INPUT)

    return fsm, helper


def wait_for_user_input(fsm: FSM, bio: BoardIO, helper: GameHelper)->tuple[FSM, BoardIO, GameHelper]:
    # Wait for user input
    while not bio.started():
        sleep(1)
    
    helper.login('board_player_1', 'password')

    while not helper._authenticated:
        sleep(1)
        
    # set a timer to wait for 30 seconds
    # if the button is pressed again, set two player mode
    timer = 30
    while timer > 0:
        if not bio.started():
            break
        sleep(1)
        timer -= 1

    if bio.started():
        helper.create_room()
    else:
        helper.create_room(PlayerMode.BOARD_TWO_PLAYER, 'Board_player_2')

    while not helper.is_game_started():
        sleep(1)

    print('Game started')
    fsm.set_state(states.WAIT_FOR_USER_MOVE)
    
    return fsm, bio, helper



def wait_for_user_move(fsm: FSM, bio: BoardIO, helper: GameHelper, cc: CameraController)->tuple[FSM, BoardIO, GameHelper, CameraController]:
    while not bio.moved():
        sleep(1)

    fen = cc.analyze_board()
    move_attempt = helper.piece_move(fen)
    if move_attempt.get('status') == 'success':
        if helper._room.game_status == GameStatus.ENDED:
            fsm.set_state(states.FINISHED)
        elif helper._room.player_mode == PlayerMode.BOARD_TWO_PLAYER:
            fsm.set_state(states.WAIT_FOR_USER_MOVE)
        else:   
            fsm.set_state(states.WAIT_FOR_SERVER_MOVE)
    else:
        bio.led_blink(COLOR.RED, 3)
        fsm.set_state(states.WAIT_FOR_USER_MOVE)

    bio._extra = False
    return fsm, bio, helper, cc

def wait_for_server_move(fsm: FSM, bio: BoardIO, helper: GameHelper, mc: MotionController, cc: CameraController)->tuple[FSM, BoardIO, GameHelper, MotionController, CameraController]:
    # Wait for server move
    while not helper.get_move():
        sleep(1)

    if helper._room.game_status == GameStatus.ENDED:
        fsm.set_state(states.FINISHED)
    else:
        # Get move from server
        move = helper.get_move()
        if move:
            mc.request_move(move)
            cc.analyze_board()
            fsm.set_state(states.WAIT_FOR_USER_MOVE)
        else:
            fsm.set_state(states.WAIT_FOR_SERVER_MOVE)
    return fsm, bio, helper, mc, cc

def finished(fsm: FSM, bio: BoardIO, helper: GameHelper, mc: MotionController, cc: CameraController)->FSM:
    # Finished
    bio.reset()
    helper.reset()
    fsm.set_state(states.WAIT_FOR_USER_INPUT)
    return fsm