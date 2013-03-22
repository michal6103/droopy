import RPi.GPIO as GPIO
import time


class Stepper:
    """Class for set up of GPIO pins for use of stepper motor"""
    pins = []
    steps = ((1, 0, 0, 0),
            (1, 1, 0, 0),
            (0, 1, 0, 0),
            (0, 1, 1, 0),
            (0, 0, 1, 0),
            (0, 0, 1, 1),
            (0, 0, 0, 1),
            (1, 0, 0, 1))
    step_delay = 0.001
    step = 0
    connected = False

    def connect(self):
        """Set GPIO pins as outputs"""
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
        self.connected = True

    def __init__(self, pins, step_delay=0.001):
        """Setup of GPIO pin mode, servo pins and step delay

        :param pins: List of GPIO pins to initialize
        :param step_delay: Minimal delay between steps"""
        GPIO.setmode(GPIO.BOARD)
        self.pins = pins
        self.step_delay = step_delay

    def __del__(self):
        """Clen GPIO settings"""
        GPIO.cleanup()

    def _set_step(self, step):
        """Set GPIO outputs for certain step

        :param step: Index of step"""
        if self.connected:
            step_outputs = self.steps[step]
            for index, pin in enumerate(self.pins):
                GPIO.output(pin, step_outputs[index])
        else:
            print "Not connected to GPIO pins"

    def step_forward(self):
        """Increment step and set it to GPIO"""
        self.step += 1
        self._set_step(self.step % 8)
        time.sleep(self.step_delay)
