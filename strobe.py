#Script that tests the LED strip

import socket

from time import sleep
from random import randint
from pinout import LEDSTRIP_ALT
import neopixel

tick = 0

def wifiLED(pixels: neopixel.Neopixel, wifistatus: int):
    if wifistatus == 1:
        pixels[8] = (0,255,0)
    if wifistatus == 2:
        pixels[8] = (255,0,0)
    if wifistatus == 0:
        pixels[8] = (0,0,0)


def boot_led(pixels: neopixel.Neopixel):
    for i in range (100, 0, -1):
        if i % 2 == 0:
            pixels.fill((255,255,255))
        if i % 2 == 1:
            pixels.fill((0,0,0))

        if i % 5 == 0:

            pixels[5] = (0,0,255)
            pixels[4] = (0,0,255)
            
        sleep(0.05)
        
    pixels.fill((0,0,0))   


pixels = neopixel.NeoPixel(LEDSTRIP_ALT, 10)

#Bootup sequence LEDs:
boot_led(pixels)



#Check internet connection:
#TODO: TEST THIS
sleep(1)


#0 is gone :(
        



sleep(10)
print("Done")
pixels.fill((0,0,0))
exit()