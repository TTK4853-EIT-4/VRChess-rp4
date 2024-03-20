
print('camera testing 1')
from picamera2 import Picamera2
from libcamera import controls
from time import sleep  
from uuid import uuid4


PICS_FOLDER = "PICS/"


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
	
