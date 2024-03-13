print('camera testing 1')
from picamera2 import Picamera2
from libcamera import controls
from time import sleep  
from uuid import uuid4
from auxilliary.fen_reader import matrix2fen

PICS_FOLDER = "PICS/"

#picam2.start(show_preview=True)
#picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})

class CameraController:
    def __init__(self) -> None:
        self.cam = initialize_camera()
        self.picture = ""
        self.cv_board = [["" for _ in range(8)] for _ in range(8)]
        
    def analyze_board(self) -> str:
        """Analyze current picture and return a FEN string of the current board.

        Returns:
            str: FEN string, current board
        """
        self._take_picture()
        self._computer_vision()
        return self._construct_board()
    
    def _take_picture(self):
        self.picture = send_nudes(self.cam)
    
    # TODO:
    def _computer_vision(self):
        """Do all the computer vision stuff"""
        self.cv_board = self.cv_board
        return
    
    def _construct_board(self) -> str:
        """Construct board as fen str from cv_board"""
        return matrix2fen(self.cv_board)
    


def initialize_camera() -> Picamera2:
	cam = Picamera2()
	cfg = cam.create_still_configuration(main={"size": (4608, 2592)})
	cam.configure(cfg)
	return cam


def send_nudes(cam: Picamera2) -> str:
	global PICS_FOLDER
	cam.start()
	unique_filename = PICS_FOLDER + str(uuid4())+ ".jpg"
	cam.capture_file(unique_filename)
	cam.stop()
	return unique_filename


if __name__ == '__main__':
	pc2 = initialize_camera()
	pic = send_nudes(pc2)
	print(f"New pic stored at {pic}")
	
