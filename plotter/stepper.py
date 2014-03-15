import RPi.GPIO as GPIO
import time
import threading
import queue
import datetime


class Stepper(threading.Thread):
    """Class for set up of GPIO pins for use of stepper motor"""
    STEPS = ((1, 0, 0, 0),
            (1, 1, 0, 0),
            (0, 1, 0, 0),
            (0, 1, 1, 0),
            (0, 0, 1, 0),
            (0, 0, 1, 1),
            (0, 0, 0, 1),
            (1, 0, 0, 1))
    pins = []
    _step_delay = 0.0
    step = 0
    connected = False
    _step_outputs = (1, 0, 0, 0)

    def get_divider(self):
        return self._divider

    def set_divider(self, value):
        if value < 1.0:
            raise ValueError('Divider must be at least 1.0')
        else:
            self._divider = value

    divider = property(get_divider, set_divider)

    def connect(self):
        """Set GPIO pins as outputs"""
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
        self.connected = True
        self.start()

    def run(self):
        """Function is tarted when thread is started. Getting position
        from queue and rotating the stepper to destination"""
        while self.connected is True:
            destination = self.in_queue.get()
            if destination != 'stop':
                self.step_to(destination)
                self.in_queue.task_done()
            else:
                self.in_queue.task_done()
                self.connected = False

    def __init__(self, pins, step_delay=0.0015):
        """Setup of GPIO pin mode, stepper pins and step delay

        :param pins: List of GPIO pins to initialize
        :param step_delay: Minimal delay between steps"""
        threading.Thread.__init__(self)
        self.daemon = True
        self.in_queue = queue.Queue()
        GPIO.setmode(GPIO.BOARD)
        self.pins = pins
        self._step_delay = step_delay
        self._divider = 1.0

    def __del__(self):
        """Clean GPIO settings"""
        GPIO.cleanup()

    def _set_step(self, step):
        """Set GPIO outputs for certain step

        :param step: Index of step"""
        if self.connected:
            self._step_outputs = self.STEPS[step]
            #for testing purposes
            if self.pins:
                for index, pin in enumerate(self.pins):
                    GPIO.output(pin, self._step_outputs[index])
        else:
            print("Not connected to GPIO pins")

    def step_forward(self):
        """Increment step and set it to GPIO"""
        self.step += 1.0 / self.divider
        self._set_step(int(self.step) % 8)

    def step_backward(self):
        """Decrement step and set it to GPIO"""
        self.step -= 1.0 / self.divider
        self._set_step(int(self.step) % 8)

    def step_to(self, destination):
        while int(self.step) != int(destination):
            step_start = datetime.datetime.now()
            if self.step > destination:
                self.step_backward()
            else:
                self.step_forward()
            step_stop = datetime.datetime.now()
            step_delta = step_stop - step_start
            time.sleep(self._step_delay - step_delta.microseconds // 1000000)
