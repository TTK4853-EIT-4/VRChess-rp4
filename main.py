from pinout import LEDSTRIP
from Motion.motioncontroller import MotionController
import logging
from time import sleep
    
    
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
    # Comms with server
    # MotionCtrl
    # Logging
    # Camera / Comp Vision
    
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
    
    # logger == logging cookbook
    mctrl = MotionController()
    mctrl.startController()
    sleep(1)
    mctrl.stop_controller()
    sleep(1)
    # comms = CommunicationController()
    # camera = CameraController()
    
    " main "
    return

if __name__ == '__main__':
    main()
