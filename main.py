from pinout import LEDSTRIP
import logging
from time import sleep
    
from Network.network import helper as GameHelper
from Motion.motioncontroller import MotionController
from auxilliary.boardIO import BoardIO
from Camera.camera import CameraController
import Fsm.fsm as fsm
    
def main():
    # setup logit
    logger = logging.getLogger("vrcLog")
    logger.setLevel(logging.DEBUG)
    
    fh = logging.FileHandler("logs/debug.log")
    fh.setLevel(logging.WARNING)
    
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(threadName)s - %(levelname)s -| %(message)s")
    fh.setFormatter(formatter)
    console.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(console)
    
    # acquire log in modules på calling getLogger(vrcLog.module)
    
    logger.debug("test")
    logger.error("fuck")
    
    
    # modules:
    ws = GameHelper
    mctrl = MotionController()
    mctrl.startController()
    bio = BoardIO()
    cc = CameraController()
    state_machine = fsm.FSM(state=fsm.states.INITIALIZE)
    
    
    i=0
    test_limit = 500
    while i<test_limit:
        print(i, state_machine.state)
        if state_machine.state == fsm.states.INITIALIZE:
            state_machine, bio = fsm.initialize(state_machine, bio)
        
        elif state_machine.state == fsm.states.WAIT_FOR_SERVER_CONNECTION:
            state_machine, ws = fsm.wait_for_server_connection(state_machine, ws)
        
        elif state_machine.state == fsm.states.WAIT_FOR_USER_INPUT:
            state_machine, bio, ws = fsm.wait_for_user_input(fsm, bio, ws)
        
        elif state_machine.state == fsm.states.WAIT_FOR_SERVER_MOVE:
            state_machine = fsm.wait_for_server_move(fsm, bio, ws, mctrl, cc)
            pass
        
        elif state_machine.state == fsm.states.WAIT_FOR_USER_MOVE:
            state_machine = fsm.wait_for_user_move(fsm, bio, ws, cc)
        
        elif state_machine.state == fsm.states.FINISHED:
            state_machine = fsm.finished(fsm, bio, ws, mctrl, cc)
            pass
    
        i+=1
    # logger == logging cookbook
    sleep(1)
    mctrl.stop_controller()
    sleep(1)
    # comms = CommunicationController()
    # camera = CameraController()
    
    " main "
    return

if __name__ == '__main__':
    main()
