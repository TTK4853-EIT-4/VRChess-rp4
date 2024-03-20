
print('camera testing 1')
from picamera2 import Picamera2
from libcamera import controls
import cv2
from time import sleep  
from uuid import uuid4
import numpy as np


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

def cropImg(img, x, y, w, h):
    img = cv2.imread(img)
    print(img.shape) # Print image shape
    cropped_image = img[y:y+h, x:x+w]
    # Display cropped image
    cv2.imshow("cropped", cropped_image)
    # Save the cropped image
    cv2.imwrite("Cropped Image.jpg", cropped_image)

if __name__ == '__main__':
	pc2 = initialize_camera()
	pic = send_nudes(pc2)
	print(f"New pic stored at {pic}")
	cropImg(pic, 100, 100, 200, 200)
	
