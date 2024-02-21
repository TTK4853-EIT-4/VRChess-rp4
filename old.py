#Script that tests the LED strip

import board
from time import sleep
from random import randint
from pinout import LEDSTRIP
import neopixel
pixels = neopixel.NeoPixel(LEDSTRIP, 10)
tick = 0

print(board.D18)
#Check internet connection 

while True:
    if tick == 0:
        for i in range (10):
            pixels[randint(0,9)] = (255,0,0)
            sleep(0.1)
        for i in range (10):
            pixels[i] = (0,255,0)
            sleep(0.1)
        sleep(0.3)
        tick = 1
        
    if tick == 1:
        pixels[1] = (0, 0, 255)
        pixels[2] = (255, 0, 0)
        sleep(0.3)
        tick = 0


#0 is gone :(

pixels[1] = (255, 0, 0)
pixels[2] = (255, 0, 0)
pixels[3] = (255, 0, 0)
pixels[4] = (255, 0, 0)

sleep(1)

pixels[4] = (0, 0, 255)
pixels[8] = (255, 0, 0)
