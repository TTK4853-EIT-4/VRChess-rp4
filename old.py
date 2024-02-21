#Script that tests the LED strip

from time import sleep
from random import randint
from pinout import LEDSTRIP_ALT
import neopixel

tick = 0

print(LEDSTRIP_ALT)
pixels = neopixel.NeoPixel(LEDSTRIP_ALT, 10)

#Bootup sequence LEDs:

for i in range (10):
    pixels[i] = (255,255,255)
    sleep(0.1)


#Check internet connection 

while tick < 3:
    sleep(0.3)
    tick += 1
  


#0 is gone :(
        

pixels.fill((0,0,0))

sleep(1)
print("Done")

exit()