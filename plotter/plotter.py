#!/usr/bin/env python3
import stepper
from math import sqrt


class Plotter:
    stepper1_pins = (15, 16, 18, 22)
    stepper2_pins = (7, 11, 12, 13)
    stepper1 = None
    stepper2 = None
    steps_pre_cm = 450
    #l is plotter width from edge of one servo to other in centimeters
    l = 52

    def __init__(self, x=0.0, y=0.0, l=52.0):
        #Initiation of physical parameters
        self.l = l

        self.stepper1 = stepper.Stepper(self.stepper1_pins)
        self.stepper2 = stepper.Stepper(self.stepper2_pins)

        self.stepper1.step = int(sqrt(x ** 2 + y ** 2) * self.steps_pre_cm)
        print("Step1: {}".format(self.stepper1.step))
        self.stepper2.step = int(sqrt(x ** 2 + (self.l - y) ** 2) * self.steps_pre_cm)
        print("Step2: {}".format(self.stepper2.step))

        self.stepper1.connect()
        self.stepper2.connect()

    def gotoXY(self, x, y):
        a = sqrt(x ** 2 + y ** 2) * self.steps_pre_cm
        d_a = a - self.stepper1.step
        b = sqrt(x ** 2 + (self.l - y) ** 2) * self.steps_pre_cm
        d_b = b - self.stepper2.step

        #speed reduction of shorter position change
        if abs(d_a) > abs(d_b):
            self.stepper1.divider = abs(d_a / d_b)
            self.stepper2.divider = 1.0
        else:
            self.stepper1.divider = 1.0
            self.stepper2.divider = abs(d_b / d_a)
        print("New position: {},{}".format(a, b))
        print("Delta position: {},{}".format(d_a, d_b))
        print("Dividers: {},{}".format(
            self.stepper1.divider,
            self.stepper2.divider))

        #synchronized movement of pen to new position
        self.stepper1.in_queue.put(int(a))
        self.stepper2.in_queue.put(int(b))
        self.stepper1.in_queue.join()
        self.stepper2.in_queue.join()

    def __del__(self):
        self.stepper1.in_queue.put('stop')
        self.stepper2.in_queue.put('stop')
        self.stepper1.in_queue.join()
        self.stepper2.in_queue.join()


if __name__ == "__main__":
    plotter = Plotter(x=27.0, y=47.0, l=54.0)
    plotter.gotoXY(27.0, 48.0)
    plotter.gotoXY(28.0, 48.0)
    plotter.gotoXY(27.0, 48.0)
    plotter.gotoXY(27.0, 47.0)
