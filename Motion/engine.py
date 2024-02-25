from pinout import MOTOR_ENABLE, M1IN1, M1IN2, M1IN3, M1IN4, M2IN1, M2IN2, M2IN3, M2IN4
from pinout import END_DET1, END_DET2
from gpiozero import DigitalOutputDevice
from gpiozero import Button
from time import sleep

PINSET_LOWER = [M1IN1, M1IN2, M1IN3, M1IN4]
PINSET_TOP = [M2IN1, M2IN2, M2IN3, M2IN4]
    

class Engine:
    enable = DigitalOutputDevice(MOTOR_ENABLE)  # static?
    
    def __init__(self, pinset: list, endstop: str) -> None:
        self._in1 = DigitalOutputDevice(pin=pinset[0], active_high=True, initial_value=False)
        self._in2 = DigitalOutputDevice(pin=pinset[1], active_high=True, initial_value=False)
        self._in3 = DigitalOutputDevice(pin=pinset[2], active_high=True, initial_value=False)
        self._in4 = DigitalOutputDevice(pin=pinset[3], active_high=True, initial_value=False)
        
        self._endstop_detection = Button(endstop)
        pass
    
    def move(self, steps: int):
        # TODO: ensure start position -> do it in controller, engine only does work stuff?.
        
        self.start()
        # set pins for direction or something..'
        print(f"Moved {steps} steps!")
        # give steps.
        self.stop()
        return
    
    def stop(self):
        self.enable.off()
        
    def start(self):
        self.enable.on()
    
# subclass?

class LowerEngine:
    
    def __init__(self) -> None:

        pass
    
    
class TopEngine:
    
    def __init__(self) -> None:
        pass