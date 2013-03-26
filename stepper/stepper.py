import RPi.GPIO as GPIO
import time
import threading
import Queue
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
    divider = 1.0
    step = 0
    connected = False

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
        #TODO: Implement divider
        while self.step != destination:
            step_start = datetime.datetime.now()
            if self.step > destination:
                self.step_backward()
            if self.step < destination:
                self.step_forward()
            step_stop = datetime.datetime.now()
            time.sleep(self._step_delay - (step_stop - step_start).microseconds / 1000000)


            #for i in range(self.delay_multiplicator):
            #    if i == 0:
            #        if self.step > destination:
            #            self.step_backward()
            #        if self.step < destination:
            #            self.step_forward()
            #    else:
            #        self.step_same()
            #    time.sleep(self._step_delay)
