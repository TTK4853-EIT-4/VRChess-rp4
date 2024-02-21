#Script that tests the LED strip

import socket

from time import sleep
from random import randint
from pinout import LEDSTRIP_ALT
import neopixel

tick = 0

def wifiLED(wifistatus):
    if wifistatus == 1:
        pixels[8] = (0,255,0)
    if wifistatus == 2:
        pixels[8] = (255,0,0)
    if wifistatus == 0:
        pixels[8] = (0,0,0)






print(LEDSTRIP_ALT)
pixels = neopixel.NeoPixel(LEDSTRIP_ALT, 10)

#Bootup sequence LEDs:

for i in range (20, 0, -1):
    if i // 2 == 0:
        pixels.fill((255,255,255))
    else:
        pixels.fill((0,0,0))
    sleep(0.1)
    
pixels.fill((0,0,0))   


#Check internet connection:
#TODO: TEST THIS
sleep(1)


#0 is gone :(
        



sleep(10)
print("Done")
pixels.fill((0,0,0))
exit()