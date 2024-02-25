from pinout import EM_ENABLE
from gpiozero import DigitalOutputDevice
from time import sleep


# TODO: Will probably need some tiny break to discharge electromagnet.
class ElectroMagnet:
    def __init__(self) -> None:
        self._output = DigitalOutputDevice(pin=EM_ENABLE, active_high=True, initial_value=False)
        self.discharge_time = 0
        pass
    
    def activate(self):
        # enable pins
        self._output.on()
        return
    
    def deactivate(self):
        # disable pins
        self._output.off()
        sleep(self.discharge_time)
        return
    
    