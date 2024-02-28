from queue import SimpleQueue, Empty
from threading import Thread
from time import time, sleep
from Motion.electromagnet import ElectroMagnet
from Motion.engine import EngineIO
import logging
import chess

mctrl_logger = logging.getLogger("vrcLog.motioncontroller")

# TODO: Stop engine if thread dies due to error
# TODO: move should encompass: what piece to move (coords), new_position, board
# TODO: piece location have to be converted to steps needed.
# TODO: algorithm for choosing path to take
class MotionController:
    
    def __init__(self) -> None:
        # states:
        self._is_moving = False
        self._q_moves = SimpleQueue()
        self._movement_thread = Thread()
        self._ctrl_running = False
        self._stop = False
        
        self._engines = EngineIO()
        self._electromagnet = ElectroMagnet()
        self._grave = Graveyard(16)
        pass
    
    def __enter__(self):
        return self
    
    def request_move(self, move):
        # add to queue
        # move {piece: coords, new_coords}
        
        self._q_moves.put_nowait(move)
        pass
    
    def startController(self):
        if not self._ctrl_running:
            #start
            # connect and stuff...
            self._stop = False
            self._movement_thread = Thread(target=self.__Controller__)
            self._movement_thread.start()
        else:
            pass
        
        return
    
    def stop_controller(self):
        self._stop = True
    
    def __Controller__(self):
        wait_time = 1/10  # <1!
        self._ctrl_running = True
        mctrl_logger.info("MotionController started")
        while not self._stop:
            new_move = False
            start_time = time()
            try:
                new_move = self._q_moves.get_nowait()
            except Empty:
                pass
            if new_move:
                piece = new_move[0]
                old_pos = new_move[1]
                new_pos = new_move[2]
                board = new_move[3]
                # TODO: make sure engines don't move when enabled
                self._engines.enable()
                # 1. move to piece position
                self._engines.move_single(old_pos)
                # 2. activate electromagnet
                self._electromagnet.activate()
                # 3. move to new position (need algorithm?)
                path = self._get_best_path(piece, old_pos, new_pos, board)
                self._engines.move_path(path)
                # 4. deactivate electromagnet
                self._electromagnet.deactivate(wait=0.1)
                # 5. return to start position
                self._engines.reset()  # return to start, poll end detectors.
                self._engines.disable()
                pass
            while time() - start_time < wait_time: sleep(wait_time*5)
        self._ctrl_running = False
        self._engines.disable()
        mctrl_logger.info("MotionController stopped")
        return
    
    def _get_best_path(self, piece, old_position, new_position, current_board) -> list[list[int]]:
        # somehow get steps needited for engines.
        # Rx old_pos and new_pos. New_pos can be graveyard.
        step_length = self._engines.STEP_LENGTH  # currently 1 cm
        square_side_length = 0.05  # 5 cm
        
        
        
        if new_position == "graveyard":
            grave_index = self._grave.add_piece(piece)
        
        
        
        # return: 2D list of moves: [[25, 25], [0, 10], [25, 25]]... '
        dumy = [[25, 25], [0, 10], [25, 25]]
        return dumy
    
    
class Graveyard:
    def __init__(self, number_of_positions) -> None:
        self.graveyard = ["" for _ in range(number_of_positions+10)]
        self.graveyard_index = {}
        self._i = 0

    def add_piece(self, piece):
        self.graveyard[self._i] = piece
        self.graveyard_index[piece] = self._i
        self._i += 1
        return self._i - 1
    
    def reset(self):
        self.graveyard = ["" for _ in range(len(self.graveyard))]
        self._i = 0
        self.graveyard_index = {}
        
    def pop_by_piece(self, piece):
        index = self.graveyard_index[piece]
        self.graveyard[index] = ""
        self.graveyard_index.pop(piece)
        return index
        
    def pop_by_index(self, index):
        piece = self.graveyard[index]
        self.graveyard[index] = ""
        self.graveyard_index.pop(piece)
        return piece
        
if __name__ == '__main__':
    pass