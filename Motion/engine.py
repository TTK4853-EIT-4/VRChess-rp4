from typing import Any
from pinout import MOTOR_ENABLE, M1IN1, M1IN2, M1IN3, M1IN4, M2IN1, M2IN2, M2IN3, M2IN4
from pinout import END_DET1, END_DET2

from isrp4 import is_raspberrypi
if is_raspberrypi():
    from gpiozero import DigitalOutputDevice
else:
    import os
    os.environ['GPIOZERO_PIN_FACTORY'] = os.environ.get('GPIOZERO_PIN_FACTORY', 'mock')
    from gpiozero import DigitalOutputDevice, Button

from time import sleep

PINSET_LOWER = [M1IN1, M1IN2, M1IN3, M1IN4]
PINSET_TOP = [M2IN1, M2IN2, M2IN3, M2IN4]
    
# TODO: move() need to activate engine.
# TODO: somehow wait for move to finish, approximate time?
class EngineIO:
    def __init__(self) -> None:
        self.lower_engine = Engine(PINSET_LOWER, END_DET1)
        self.top_engine = Engine(PINSET_TOP, END_DET2)
        
        self.enable = DigitalOutputDevice(MOTOR_ENABLE, active_high=True, initial_value=False)
        
    
    def move_single(self, path: list[int]):
        """Send the amount of steps each engine should take. path[0] sets the steps for the lower engine, while path[1] sets the steps for the top engine. [0, 10] will make only the top engine do 10 steps.

        Args:
            path (list[int, int]): [steps_engine_lower, steps_engine_top]
        """
        self.lower_engine.move(path[0])
        self.top_engine.move(path[1])
        
    def move_path(self, path: list[list[int]]):
        for move in path:
            self.move_single(move)
            
    def enable(self):
        self.enable.on()
        
    def disable(self):
        self.disable.off()
        
    def reset(self):
        # no clue
        tick = 0  # if 3 minutes are used stop trying.
        while (not self.lower_engine._end_detected and not self.top_engine._end_detected) or tick < 1_800:
            if not self.lower_engine._end_detected:
                self.lower_engine.move(-10)
            if not self.top_engine._end_detected:
                self.top_engine.move(-10)
            sleep(0.1)
            tick += 1
                
        return


class Engine:
    
    def __init__(self, pinset: list, endstop: str) -> None:
        self._in1 = DigitalOutputDevice(pin=pinset[0], active_high=True, initial_value=False)
        self._in2 = DigitalOutputDevice(pin=pinset[1], active_high=True, initial_value=False)
        self._in3 = DigitalOutputDevice(pin=pinset[2], active_high=True, initial_value=False)
        self._in4 = DigitalOutputDevice(pin=pinset[3], active_high=True, initial_value=False)
        
        self._end_detected = False
        self._endstop_detection = Button(endstop)
        self._endstop_detection.when_activated = self._at_endstop
        self._endstop_detection.when_deactivated = self._not_at_endstop
    
    def move(self, steps: int):
        # set pins for direction or something..'
        print(f"Moved {steps} steps!")
        # give steps.
        return
    
    def stop(self):
        # set pins to some stop mode?
        return
    
    def _at_endstop(self):
        self.stop()
        self._end_detected = True
        
    def _not_at_endstop(self):
        self._end_detected = False
    
