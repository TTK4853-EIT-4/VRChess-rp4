from enum import Enum
from dataclasses import dataclass
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
    fsm.set_state(states.WAIT_FOR_USER_INPUT)
    return fsm, bio

# TODO:  DELETE
def wait_for_server_connection(fsm: FSM, ws: WebSocketController)->tuple[FSM, Board]:
    # Currently want:
    # ping server and check for answer.
    # Server good -> show user
    # Server bad -> show user
    # next state: wait for user input
    
    # NOT a state -> subthread of socketController? some intervaltimer, just ping every 5 seconds?
    return


def wait_for_user_input(fsm: FSM, bio: BoardIO)->tuple[FSM, Board]:
    # What does the player want?
    if bio.started():
        # update board state with computervision
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