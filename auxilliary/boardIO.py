from pinout import LEDSTRIP_ALT, LEDSTRIP, BTN_JOIN, BTN_EXTRA
from auxilliary.isrp4 import is_raspberrypi
if is_raspberrypi():
    from gpiozero import DigitalOutputDevice, Button
else:
    import os
    os.environ['GPIOZERO_PIN_FACTORY'] = os.environ.get('GPIOZERO_PIN_FACTORY', 'mock')
    from gpiozero import DigitalOutputDevice, Button
from time import sleep
from neopixel import NeoPixel
from strobe import boot_led, wifiLED


class LED_LOCATION:
    DONT_USE = 0
    WIFI = 8

class COLOR:
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    BLUE = (0, 0, 255)


class BoardIO:
    def __init__(self) -> None:
        self._started = False
        self._extra = False
        
        self.btn_start = Button(BTN_JOIN)
        self.btn_start.when_activated(self._at_start_press)
        
        self.btn_extra = Button(BTN_EXTRA)
        self.btn_extra.when_activated(self._at_extra_press)
    
        self.led_strip = NeoPixel(LEDSTRIP_ALT, 10)
        boot_led(self.led_strip)
        
        
    def wifi_status_led(self, wifi_status):
        wifi_led = LED_LOCATION.WIFI
        if wifi_status == 1:
            self.led_strip[wifi_led] = COLOR.GREEN
        if wifi_status == 2:
            self.led_strip[wifi_led] = COLOR.RED
        if wifi_status == 0:
            self.led_strip[wifi_led] = COLOR.BLACK
            
    
    def _at_start_press(self):
        self._started = not self._started
        return
    
    def _at_extra_press(self):
        self._extra = not self._extra
        return
    
    def started(self):
        return self._started
    
    def extraed(self):
        return self._extra
    
    def reset(self):
        self._started = False
        self._extra = False
  