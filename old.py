#Script that tests the LED strip
import urllib

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

for i in range (9, 0, -1):
    pixels[i] = (255,255,255)
    sleep(0.2)
    
pixels.fill((0,0,0))   
pixels[9] = (255,255,255) #PWR

#Check internet connection:
sleep(1)

import socket
def check_internet():
    try:
        res = socket.getaddrinfo('google.com',80)
        return True
    except:
        return False
    
if check_internet():
    print("Connected to internet")
    wifiLED(1)

else:
    print("No internet connection")
    wifiLED(2)




while tick < 3:
    sleep(1)
    tick += 1
  


#0 is gone :(
        



sleep(10)
print("Done")
pixels.fill((0,0,0))
exit()