import RPi.GPIO as GPIO
import time
import threading
import Queue


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
    _step_delay = 0.001
    delay_multiplicator = 1
    step = 0
    connected = False

    def connect(self):
        """Set GPIO pins as outputs"""
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
        self.connected = True
        self.start()

    def run(self):
        while self.connected is True:
            step = self.in_queue.get()
            if step != 'stop':
                self.step_to(step)
                self.in_queue.task_done()
            else:
                self.in_queue.task_done()
                self.connected = False

    def __init__(self, pins, step_delay=0.001):
        """Setup of GPIO pin mode, stepper pins and step delay

        :param pins: List of GPIO pins to initialize
        :param step_delay: Minimal delay between steps"""
        threading.Thread.__init__(self)
        self.daemon = True
        self.in_queue = Queue.Queue()
        GPIO.setmode(GPIO.BOARD)
        self.pins = pins
        self._step_delay = step_delay

    def __del__(self):
        """Clen GPIO settings"""
        GPIO.cleanup()

    def _set_step(self, step):
        """Set GPIO outputs for certain step

        :param step: Index of step"""
        if self.connected:
            step_outputs = self.STEPS[step]
            for index, pin in enumerate(self.pins):
                GPIO.output(pin, step_outputs[index])
        else:
            print "Not connected to GPIO pins"

    def step_forward(self):
        """Increment step and set it to GPIO"""
        self.step += 1
        self._set_step(self.step % 8)

    def step_backward(self):
        """Decrement step and set it to GPIO"""
        self.step -= 1
        self._set_step(self.step % 8)

    def step_same(self):
        """Do not change step and set it on GPIO.
        Function just for synchronisation purposes"""
        self.step += 0
        self._set_step(self.step % 8)

    def step_to(self, destination):
        while self.step != destination:
            for i in range(self.delay_multiplicator):
                if i == 0:
                    if self.step > destination:
                        self.step_backward()
                    if self.step < destination:
                        self.step_forward()
                else:
                    self.step_same()
                time.sleep(self._step_delay)
