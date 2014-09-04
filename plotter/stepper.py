#!/usr/bin/env python3
import time
import threading
import queue
import datetime


"""Optional load of GPIO"""
try:
    import RPi.GPIO as GPIO
except ImportError as e:
        if str(e) != "No module named 'RPi'":
            raise
        else:
            GPIO = False


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
        if not self.debug and GPIO:
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

    def __init__(self, pins=(7,11,12,3), step_delay=0.0015, debug=False):
        """Setup of GPIO pin mode, stepper pins and step delay

        :param pins: List of GPIO pins to initialize
        :param step_delay: Minimal delay between steps"""
        threading.Thread.__init__(self)
        self.daemon = True
        self.in_queue = queue.Queue()
        self.debug = debug
        if self.debug:
            self.pins = False
        else:
            if GPIO:
                GPIO.setmode(GPIO.BOARD)
            self.pins = pins
        self._step_delay = step_delay
        self._divider = 1.0

    def __del__(self):
        """Clean GPIO settings"""
        if GPIO:
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
            if not self.debug:
                time.sleep(self._step_delay - step_delta.microseconds // 1000000)


if __name__ == "__main__":
    stepper_pins1 = (7, 11, 12, 13)
    stepper_pins2 = (15, 16, 18, 22)

    stepper1 = Stepper(stepper_pins1)
    stepper2 = Stepper(stepper_pins2)

    stepper1.connect()
    stepper2.connect()

    stepper1.divider = 2.5
    stepper2.divider = 2.5
    stepper1.in_queue.put(-1000)
    stepper2.in_queue.put(1000)
    stepper1.in_queue.put(0)
    stepper2.in_queue.put(0)
    stepper1.in_queue.put('stop')
    stepper2.in_queue.put('stop')
    stepper1.in_queue.join()
    stepper2.in_queue.join()
