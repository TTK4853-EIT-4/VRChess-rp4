#Script that tests the LED strip

from time import sleep
from random import randint
from pinout import LEDSTRIP_ALT
import neopixel

tick = 0

print(LEDSTRIP_ALT)
pixels = neopixel.NeoPixel(LEDSTRIP_ALT, 10)
#Check internet connection 

while tick < 3:
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
        tick = 3
    print(tick)


#0 is gone :(
        

pixels.fill((0,0,0))

sleep(1)
print("Done")

exit()