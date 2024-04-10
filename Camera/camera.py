print('camera testing 1')
from picamera2 import Picamera2
from libcamera import controls
from time import sleep  
from uuid import uuid4
from auxilliary.fen_reader import matrix2fen
from PIL import Image, ImageDraw
import cv2
import numpy as np
# import the inference-sdk
from inference_sdk import InferenceHTTPClient


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
        newcrop(self.picture)
    
    def _computer_vision(self):
        """Do all the computer vision stuff"""
        self.cv_board = vision2000(self.picture)
        return
    
    def _construct_board(self) -> str:
        """Construct board as fen str from cv_board"""
        return matrix2fen(self.cv_board)
    


def initialize_camera() -> Picamera2:
	cam = Picamera2()
	cfg = cam.create_still_configuration(main={"size": (4608, 2592)})
	cam.configure(cfg)
	return cam





def vision2000(imgStr:str) -> list[list[str]]:
    treshold = 0.3

    squares = {
        "boxes": [
            {
                "label": "A8",
                "x": "301.85",
                "y": "347.09",
                "width": "200.00",
                "height": "210.00",
                "color": "#8622FF"
            },
            {
                "label": "B8",
                "x": "515.68",
                "y": "345.30",
                "width": "213.98",
                "height": "232.11",
                "color": "#FE0056"
            },
            {
                "label": "C8",
                "x": "735.11",
                "y": "344.93",
                "width": "220.75",
                "height": "230.69",
                "color": "#00FFCE"
            },
            {
                "label": "D8",
                "x": "956.42",
                "y": "343.83",
                "width": "217.44",
                "height": "230.69",
                "color": "#FF8000"
            },
            {
                "label": "E8",
                "x": "1175.52",
                "y": "341.62",
                "width": "220.75",
                "height": "232.90",
                "color": "#00B7EB"
            },
            {
                "label": "F8",
                "x": "1397.93",
                "y": "347.14",
                "width": "228.48",
                "height": "232.90",
                "color": "#FFFF00"
            },
            {
                "label": "G8",
                "x": "1624.20",
                "y": "343.27",
                "width": "226.27",
                "height": "238.42",
                "color": "#FF00FF"
            },
            {
                "label": "H8",
                "x": "1853.79",
                "y": "341.62",
                "width": "230.69",
                "height": "239.52",
                "color": "#0E7AFE"
            },
            {
                "label": "H7",
                "x": "1849.37",
                "y": "578.38",
                "width": "226.27",
                "height": "225.17",
                "color": "#FFABAB"
            },
            {
                "label": "H6",
                "x": "1843.85",
                "y": "810.17",
                "width": "230.69",
                "height": "225.17",
                "color": "#0000FF"
            },
            {
                "label": "H5",
                "x": "1841.10",
                "y": "1029.27",
                "width": "231.79",
                "height": "235.10",
                "color": "#a0522d"
            },
            {
                "label": "H4",
                "x": "1835.02",
                "y": "1251.68",
                "width": "232.90",
                "height": "225.17",
                "color": "#808000"
            },
            {
                "label": "H3",
                "x": "1830.06",
                "y": "1473.54",
                "width": "229.59",
                "height": "222.96",
                "color": "#483d8b"
            },
            {
                "label": "H2",
                "x": "1824.54",
                "y": "1693.74",
                "width": "231.79",
                "height": "224.07",
                "color": "#8b008b"
            },
            {
                "label": "H1",
                "x": "1818.47",
                "y": "1914.50",
                "width": "232.90",
                "height": "226.27",
                "color": "#ff4500"
            },
            {
                "label": "G1",
                "x": "1592.75",
                "y": "1909.53",
                "width": "214.13",
                "height": "225.17",
                "color": "#dc143c"
            },
            {
                "label": "G2",
                "x": "1597.16",
                "y": "1689.33",
                "width": "222.96",
                "height": "224.07",
                "color": "#00ffff"
            },
            {
                "label": "G3",
                "x": "1603.23",
                "y": "1468.02",
                "width": "219.65",
                "height": "222.96",
                "color": "#d8bfd8"
            },
            {
                "label": "G4",
                "x": "1606.54",
                "y": "1245.61",
                "width": "217.44",
                "height": "224.07",
                "color": "#ff1493"
            },
            {
                "label": "G5",
                "x": "1609.85",
                "y": "1020.99",
                "width": "213.03",
                "height": "222.96",
                "color": "#ffe4b5"
            },
            {
                "label": "G6",
                "x": "1615.93",
                "y": "800.24",
                "width": "222.96",
                "height": "231.79",
                "color": "#db7093"
            },
            {
                "label": "G7",
                "x": "1620.89",
                "y": "572.31",
                "width": "226.27",
                "height": "221.86",
                "color": "#deb887"
            },
            {
                "label": "F1",
                "x": "1371.44",
                "y": "1904.01",
                "width": "219.65",
                "height": "222.96",
                "color": "#6495ed"
            },
            {
                "label": "F2",
                "x": "1377.51",
                "y": "1683.81",
                "width": "218.55",
                "height": "219.65",
                "color": "#C7FC00"
            },
            {
                "label": "F3",
                "x": "1381.93",
                "y": "1464.16",
                "width": "216.34",
                "height": "221.86",
                "color": "#8622FF"
            },
            {
                "label": "F4",
                "x": "1384.13",
                "y": "1242.85",
                "width": "214.13",
                "height": "227.38",
                "color": "#FE0056"
            },
            {
                "label": "F5",
                "x": "1390.20",
                "y": "1018.78",
                "width": "217.44",
                "height": "220.75",
                "color": "#00FFCE"
            },
            {
                "label": "F6",
                "x": "1390.76",
                "y": "793.06",
                "width": "218.55",
                "height": "224.07",
                "color": "#FF8000"
            },
            {
                "label": "F7",
                "x": "1395.17",
                "y": "573.96",
                "width": "220.75",
                "height": "222.96",
                "color": "#00B7EB"
            },
            {
                "label": "E7",
                "x": "1172.76",
                "y": "572.86",
                "width": "219.65",
                "height": "222.96",
                "color": "#FFFF00"
            },
            {
                "label": "E6",
                "x": "1171.10",
                "y": "796.37",
                "width": "214.13",
                "height": "219.65",
                "color": "#FF00FF"
            },
            {
                "label": "E5",
                "x": "1166.14",
                "y": "1018.78",
                "width": "215.24",
                "height": "222.96",
                "color": "#0E7AFE"
            },
            {
                "label": "E4",
                "x": "1163.93",
                "y": "1241.19",
                "width": "217.44",
                "height": "219.65",
                "color": "#FFABAB"
            },
            {
                "label": "E3",
                "x": "1160.07",
                "y": "1461.40",
                "width": "218.55",
                "height": "222.96",
                "color": "#0000FF"
            },
            {
                "label": "E2",
                "x": "1155.10",
                "y": "1681.60",
                "width": "215.24",
                "height": "219.65",
                "color": "#a0522d"
            },
            {
                "label": "E1",
                "x": "1152.34",
                "y": "1899.60",
                "width": "209.72",
                "height": "220.75",
                "color": "#808000"
            },
            {
                "label": "D1",
                "x": "936.55",
                "y": "1906.22",
                "width": "215.24",
                "height": "247.25",
                "color": "#483d8b"
            },
            {
                "label": "D2",
                "x": "936.00",
                "y": "1673.87",
                "width": "216.34",
                "height": "219.65",
                "color": "#8b008b"
            },
            {
                "label": "D3",
                "x": "940.42",
                "y": "1454.22",
                "width": "211.92",
                "height": "215.24",
                "color": "#ff4500"
            },
            {
                "label": "D4",
                "x": "942.07",
                "y": "1234.02",
                "width": "217.44",
                "height": "218.55",
                "color": "#dc143c"
            },
            {
                "label": "D5",
                "x": "944.83",
                "y": "1012.71",
                "width": "214.13",
                "height": "219.65",
                "color": "#00ffff"
            },
            {
                "label": "D6",
                "x": "946.49",
                "y": "789.75",
                "width": "215.24",
                "height": "219.65",
                "color": "#d8bfd8"
            },
            {
                "label": "D7",
                "x": "951.45",
                "y": "570.65",
                "width": "211.92",
                "height": "216.34",
                "color": "#ff1493"
            },
            {
                "label": "C7",
                "x": "731.80",
                "y": "571.76",
                "width": "214.13",
                "height": "220.75",
                "color": "#ffe4b5"
            },
            {
                "label": "C6",
                "x": "727.94",
                "y": "791.96",
                "width": "213.03",
                "height": "215.24",
                "color": "#db7093"
            },
            {
                "label": "C5",
                "x": "726.28",
                "y": "1012.71",
                "width": "216.34",
                "height": "217.44",
                "color": "#deb887"
            },
            {
                "label": "C4",
                "x": "724.08",
                "y": "1235.68",
                "width": "211.92",
                "height": "217.44",
                "color": "#6495ed"
            },
            {
                "label": "C3",
                "x": "721.87",
                "y": "1453.12",
                "width": "214.13",
                "height": "215.24",
                "color": "#C7FC00"
            },
            {
                "label": "C2",
                "x": "716.35",
                "y": "1672.22",
                "width": "214.13",
                "height": "214.13",
                "color": "#8622FF"
            },
            {
                "label": "C1",
                "x": "716.35",
                "y": "1887.45",
                "width": "216.34",
                "height": "216.34",
                "color": "#FE0056"
            },
            {
                "label": "B1",
                "x": "499.46",
                "y": "1880.83",
                "width": "208.61",
                "height": "216.34",
                "color": "#00FFCE"
            },
            {
                "label": "B2",
                "x": "504.42",
                "y": "1663.39",
                "width": "211.92",
                "height": "220.75",
                "color": "#FF8000"
            },
            {
                "label": "B3",
                "x": "507.74",
                "y": "1447.05",
                "width": "214.13",
                "height": "216.34",
                "color": "#00B7EB"
            },
            {
                "label": "B4",
                "x": "507.74",
                "y": "1229.60",
                "width": "211.92",
                "height": "222.96",
                "color": "#FFFF00"
            },
            {
                "label": "B5",
                "x": "507.74",
                "y": "1009.95",
                "width": "211.92",
                "height": "220.75",
                "color": "#FF00FF"
            },
            {
                "label": "B6",
                "x": "508.84",
                "y": "789.75",
                "width": "209.72",
                "height": "219.65",
                "color": "#0E7AFE"
            },
            {
                "label": "B7",
                "x": "512.70",
                "y": "571.20",
                "width": "213.03",
                "height": "217.44",
                "color": "#FFABAB"
            },
            {
                "label": "A7",
                "x": "284.77",
                "y": "569.00",
                "width": "231.79",
                "height": "219.65",
                "color": "#0000FF"
            },
            {
                "label": "A6",
                "x": "282.57",
                "y": "789.75",
                "width": "229.59",
                "height": "217.44",
                "color": "#a0522d"
            },
            {
                "label": "A5",
                "x": "272.08",
                "y": "1007.75",
                "width": "243.93",
                "height": "216.34",
                "color": "#808000"
            },
            {
                "label": "A4",
                "x": "266.01",
                "y": "1227.95",
                "width": "262.70",
                "height": "217.44",
                "color": "#483d8b"
            },
            {
                "label": "A3",
                "x": "266.01",
                "y": "1448.15",
                "width": "260.49",
                "height": "211.92",
                "color": "#8b008b"
            },
            {
                "label": "A2",
                "x": "265.46",
                "y": "1664.49",
                "width": "257.18",
                "height": "209.72",
                "color": "#ff4500"
            },
            {
                "label": "A1",
                "x": "263.25",
                "y": "1880.28",
                "width": "254.97",
                "height": "208.61",
                "color": "#dc143c"
            }
        ],
        "height": 2241,
        "key": "1.jpg",
        "width": 2157
    }



    # initialize the client
    CLIENT = InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key="c5QPWVhpoXPdibiJg5kn"
    )

    # infer on a local image
    result = CLIENT.infer(imgStr, model_id="chessboard-1/1")


    localResult = result




    # Only the prediction:
    localPrediction = localResult['predictions']
    #Sort the predictions by confidence
    localPrediction = sorted(localPrediction, key=lambda x: x['confidence'], reverse=True)
    #Print amount of predictions:
    # print(len(localPrediction))
    #Remove all predictions with a confidence lower than treshold:
    localPrediction = [x for x in localPrediction if x['confidence'] > treshold]
    #Print the new amount of predictions:
    # print(len(localPrediction))


 
    #The chess board is 8x8, and the squares are annotated from a1 to h8, in the squares variable, like this: squares = {
        # "boxes": [
        #     {
        #         "label": "A8",
        #         "x": "301.85",
        #         "y": "347.09",
        #         "width": "200.00",
        #         "height": "210.00",
        #         "color": "#8622FF"
        #     },
        #     {
        #         "label": "B8",
        #         "x": "515.68",



    # Display the image with the predictions and squares:
    # display = Image.open(imgStr)
    # draw = ImageDraw.Draw(display)
    # for i in range(len(localPrediction)):
    #     x = localPrediction[i]['x']
    #     y = localPrediction[i]['y']
    #     draw.rectangle([x, y, x+5, y+5], outline='red', width=2)
    #     draw.text((x, y), localPrediction[i]['class'], fill='red')

    # for i in range(len(squares['boxes'])):
    #     x = float(squares['boxes'][i]['x'])
    #     y = float(squares['boxes'][i]['y'])
    #     width = float(squares['boxes'][i]['width'])
    #     height = float(squares['boxes'][i]['height'])
    #     #The x and y is the center of the square, so we need to calculate the top left corner
    #     x = x - width/2
    #     y = y - height/2
    #     draw.rectangle([x, y, x+width, y+height], outline='blue', width=2)
    #     draw.text((x, y), squares['boxes'][i]['label'], fill='blue')
        
    # display.show()

    # Find which square the predictions are in:

    #Create a list of the squares:
    squareList = []
    for i in range(len(squares['boxes'])):
        x = float(squares['boxes'][i]['x'])
        y = float(squares['boxes'][i]['y'])
        width = float(squares['boxes'][i]['width'])
        height = float(squares['boxes'][i]['height'])
        #The x and y is the center of the square, so we need to calculate the top left corner
        x = x - width/2
        y = y - height/2
        squareList.append([x, y, x+width, y+height, squares['boxes'][i]['label']])
    #Check which square the predictions are in, and create a map of all the squares to either null or the class of the prediction. If there are multiple predictions in the same square, the one with the highest confidence will be chosen.

    squareMap = {}
    for i in range(len(localPrediction)):
        x = localPrediction[i]['x']
        y = localPrediction[i]['y']
        for j in range(len(squareList)):
            if x > squareList[j][0] and x < squareList[j][2] and y > squareList[j][1] and y < squareList[j][3]:
                if squareList[j][4] in squareMap:
                    if localPrediction[i]['confidence'] > squareMap[squareList[j][4]][1]:
                        squareMap[squareList[j][4]] = [localPrediction[i]['class'], localPrediction[i]['confidence']]
                else:
                    squareMap[squareList[j][4]] = [localPrediction[i]['class'], localPrediction[i]['confidence']]

    #Print the map:
    # print(squareMap)
    #Fill the blank squares with null:
    for i in range(len(squareList)):
        if squareList[i][4] not in squareMap:
            squareMap[squareList[i][4]] = [None, 0]
    #Print the map again:
    # print(squareMap)

    #Convert into a matrix of the chess board:
    chessBoard = []
    for i in range(8):
        chessBoard.append([squareMap[chr(65+j)+str(8-i)][0] for j in range(8)])
    #Print the matrix:

    # print(chessBoard)


    #Uppercase is white, lowercase is black
    # Empty = ""
    # p is BlackPawn
    # r is BlackTower
    # n is BlackHorse
    # b is BlackLoper
    # q is BlackQueen
    # k is BlackKing

    # P is WhitePawn
    # R is WhiteTower
    # N is WhiteHorse
    # B is WhiteLoper
    # Q is WhiteQueen
    # K is WhiteKing


    # Convert matrix to new matrix with the correct pieces based on the comment above. Remember to keep the old names in one word
    newChessBoard = []
    for i in range(8):
        newChessBoard.append([None]*8)
    for i in range(8):
        for j in range(8):
            if chessBoard[i][j] == None:
                newChessBoard[i][j] = ""
            elif chessBoard[i][j] == "BlackPawn":
                newChessBoard[i][j] = "p"
            elif chessBoard[i][j] == "BlackTower":
                newChessBoard[i][j] = "r"
            elif chessBoard[i][j] == "BlackHorse":
                newChessBoard[i][j] = "n"
            elif chessBoard[i][j] == "BlackLoper":
                newChessBoard[i][j] = "b"
            elif chessBoard[i][j] == "BlackQueen":
                newChessBoard[i][j] = "q"
            elif chessBoard[i][j] == "BlackKing":
                newChessBoard[i][j] = "k"
            elif chessBoard[i][j] == "WhitePawn":
                newChessBoard[i][j] = "P"
            elif chessBoard[i][j] == "WhiteTower":
                newChessBoard[i][j] = "R"
            elif chessBoard[i][j] == "WhiteHorse":
                newChessBoard[i][j] = "N"
            elif chessBoard[i][j] == "WhiteLoper":
                newChessBoard[i][j] = "B"
            elif chessBoard[i][j] == "WhiteQueen":
                newChessBoard[i][j] = "Q"
            elif chessBoard[i][j] == "WhiteKing":
                newChessBoard[i][j] = "K"

    #Return the new matrix:
    return (newChessBoard)

def send_nudes(cam: Picamera2) -> str:
	global PICS_FOLDER
	cam.start()
	unique_filename = PICS_FOLDER + str(uuid4())+ ".jpg"
	cam.capture_file(unique_filename)
	cam.stop()
	return unique_filename


def newcrop(img):
    img = cv2.imread(img)
    # points for test.jpg
    cnt = np.array([
            [[1230, 480]],
            [[3410, 329]],
            [[3471, 2486]],
            [[1229, 2485]]
        ])
    # print("shape of cnt: {}".format(cnt.shape))
    rect = cv2.minAreaRect(cnt)
    # print("rect: {}".format(rect))

    # the order of the box points: bottom left, top left, top right,
    # bottom right
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    # print("bounding box: {}".format(box))
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
	
