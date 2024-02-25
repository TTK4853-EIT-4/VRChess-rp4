from queue import SimpleQueue, Empty
from threading import Thread
from time import time, sleep


# TODO: Stop engine if thread dies due to error
class MotionController:
    
    def __init__(self) -> None:
        # states:
        self._is_moving = False
        self._q_moves = SimpleQueue()
        self._movement_thread = Thread()
        self._ctrl_running = False
        self._stop = False
        
        pass
    
    def __enter__(self):
        return self
    
    def request_move(self, move):
        # add to queue
        self._q_moves.put_nowait(move)
        pass
    
    def startController(self):
        if not self._ctrl_running:
            #start
            # connect and stuff...
            self._stop = False
            self._movement_thread = Thread(target=self.__Controller__)
        else:
            pass
        
        return
    
    def stop_controller(self):
        self._stop = True
    
    def __Controller__(self):
        wait_time = 1/10  # <1!
        self._ctrl_running = True
        while not self._stop:
            start_time = time()
            try:
                new_move = self._q_moves.get_nowait()
            except Empty:
                pass
            if new_move:
                # 1. move to piece position
                # 2. activate electromagnet
                # 3. move to new position (need algorithm?)
                # 4. deactivate electromagnet
                # 5. return to start position
                pass
            while time() - start_time < wait_time: sleep(wait_time*5)
        
        return