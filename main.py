from pinout import LEDSTRIP
import logging
from time import sleep
    
from Network.network import WebSocketController
from Motion.motioncontroller import MotionController
from auxilliary.boardIO import BoardIO
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
    ws = WebSocketController()
    # ws.run()
    mctrl = MotionController()
    mctrl.startController()
    bio = BoardIO()
    state_machine = fsm.FSM(state=fsm.states.INITIALIZE)
    
    
    i=0
    test_limit = 500
    while i<test_limit:
        print(i)
        if state_machine == fsm.states.INITIALIZE:
            state_machine, bio = fsm.initialize(state_machine, bio)
        
        elif state_machine == fsm.states.WAIT_FOR_SERVER_CONNECTION:
            pass
        
        elif state_machine == fsm.states.WAIT_FOR_USER_INPUT:
            state_machine, bio = fsm.wait_for_user_input(fsm, bio)
        
        elif state_machine == fsm.states.WAIT_FOR_SERVER_MOVE:
            pass
        
        elif state_machine == fsm.states.WAIT_FOR_USER_MOVE:
            state_machine = fsm.wait_for_user_move(fsm)
        
        elif state_machine == fsm.states.FINISHED:
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
