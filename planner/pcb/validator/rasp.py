import atexit

import RPi.GPIO as GPIO

RESERVED_PINS = set([0, 1])

class PiPin:
    def __init__(self, pin: int):
        assert pin not in RESERVED_PINS
        assert pin in list(range(28))
        self.pin = pin

class PiOut(PiPin):
    def __init__(self, *args):
        super().__init__(*args)
        GPIO.setup(self.pin, GPIO.OUT)

    def set(self, high: bool):
        GPIO.output(self.pin, GPIO.HIGH if high else GPIO.LOW)

class PiInput(PiPin):
    def __init__(self, *args):
        super().__init__(*args)
        GPIO.setup(self.pin, GPIO.IN)

    def is_high(self):
        return GPIO.input(self.pin) == GPIO.HIGH


class PiController:
    def __init__(self):
        self.pins = [None]*28  # pytype: List[PiPin | None]
        self.setup()

    def setup(self):
        def cleanup():
            GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup
        atexit.register(cleanup)

    def assign_out(self, index: int):
        assert self.pins[index] is None
        out = PiOut(index)
        self.pins[index] = out
        return out

    def assign_in(self, index: int):
        assert index not in self.reserved_pins
        assert self.pins[index] is None
        input = PiInput(index)
        self.pins[index] = input
        return input
