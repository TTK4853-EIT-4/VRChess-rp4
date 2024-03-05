from pinout import EM_ENABLE
from auxilliary.isrp4 import is_raspberrypi
if is_raspberrypi():
    from gpiozero import DigitalOutputDevice
else:
    import os
    os.environ['GPIOZERO_PIN_FACTORY'] = os.environ.get('GPIOZERO_PIN_FACTORY', 'mock')
    from gpiozero import DigitalOutputDevice
from time import sleep


# TODO: Will probably need some tiny break to discharge electromagnet.
class ElectroMagnet:
    def __init__(self) -> None:
        self._output = DigitalOutputDevice(pin=EM_ENABLE, active_high=True, initial_value=False)
        pass
    
    def activate(self):
        # enable pins
        self._output.on()
        return
    
    def deactivate(self, wait=0):
        # disable pins
        self._output.off()
        sleep(wait)
        return
    
    