from pinout import LEDSTRIP
import logging
from time import sleep
    
from Network.network import WebSocketController
from Motion.motioncontroller import MotionController
from auxilliary import boardIO
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
    ws.run()
    mctrl = MotionController()
    mctrl.startController()
    bio = boardIO.BoardIO()
    state_machine = fsm.FSM(state=fsm.states.INITIALIZE)
    
    state_machine, bio = fsm.initialize(state_machine, bio)
    # Comms with server
    # MotionCtrl
    # Logging
    # Camera / Comp Vision
    
    while True:
        if bio.started():
            ws.login('board_player_1', 'board_pwd')
        elif bio.extraed():
            ws.login('board_player_1', 'board_pwd', 'board_player_2', ws.BOARD_MULTI_PLAYER)
        elif ws.game_over:
            break
    
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
