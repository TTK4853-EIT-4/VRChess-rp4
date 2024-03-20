
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


def newcrop(img):
    img = cv2.imread(img)
    # points for test.jpg
    cnt = np.array([
            [[64, 49]],
            [[1022, 101]],
            [[2901, 2026]],
            [[2008, 1073]]
        ])
    print("shape of cnt: {}".format(cnt.shape))
    rect = cv2.minAreaRect(cnt)
    print("rect: {}".format(rect))

    # the order of the box points: bottom left, top left, top right,
    # bottom right
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    print("bounding box: {}".format(box))
    cv2.drawContours(img, [box], 0, (0, 0, 255), 2)

    # get width and height of the detected rectangle
    width = int(rect[1][0])
    height = int(rect[1][1])

    src_pts = box.astype("float32")
    # coordinate of the points in box points after the rectangle has been
    # straightened
    dst_pts = np.array([[0, height-1],
                        [0, 0],
                        [width-1, 0],
                        [width-1, height-1]], dtype="float32")

    # the perspective transformation matrix
    M = cv2.getPerspectiveTransform(src_pts, dst_pts)

    # directly warp the rotated rectangle to get the straightened rectangle
    warped = cv2.warpPerspective(img, M, (width, height))

    cv2.imwrite("crop_img.jpg", warped)
    cv2.waitKey(0)

	
	
if __name__ == '__main__':
	pc2 = initialize_camera()
	pic = send_nudes(pc2)
	print(f"New pic stored at {pic}")
	# cropImg(pic, 1000, 1000, 2000, 2000)
	newcrop(pic)
	
	
