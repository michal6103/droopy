#!/usr/bin/env python3
import stepper
from math import sqrt


class Plotter:
    stepper1_pins = (15, 16, 18, 22)
    stepper2_pins = (7, 11, 12, 13)
    stepper1 = None
    stepper2 = None
    steps_per_cm = 450
    #l is plotter width from edge of one servo to other in centimeters
    l = 52

    def __init__(self, x=0.0, y=0.0, l=52.0, debug=False):
        #Initiation of physical parameters
        self.l = l
        if debug:
            self.stepper1 = stepper.Stepper(debug=debug)
            self.stepper2 = stepper.Stepper(debug=debug)
        else:
            self.stepper1 = stepper.Stepper(self.stepper1_pins)
            self.stepper2 = stepper.Stepper(self.stepper2_pins)

        self.stepper1.step = int(sqrt(x ** 2 + y ** 2) * self.steps_per_cm)
        self.stepper2.step = int(sqrt(y ** 2 + (self.l - x) ** 2) * self.steps_per_cm)

        self.stepper1.connect()
        self.stepper2.connect()

    def gotoXY(self, x, y):
        #print("New XY: {},{}".format(x, y))
        a = sqrt(x ** 2 + y ** 2) * self.steps_per_cm
        d_a = a - self.stepper1.step
        b = sqrt(y ** 2 + (self.l - x) ** 2) * self.steps_per_cm
        d_b = b - self.stepper2.step
        #print("New ab: {},{}".format(a, b))
        #print("Delta ab: {},{}".format(d_a, d_b))
        #print("Dividers: {},{}".format(
        #    self.stepper1.divider,
        #    self.stepper2.divider))

        #speed reduction of shorter position change
        if abs(d_a) == abs(d_b):
            self.stepper1.divider = 1.0
            self.stepper2.divider = 1.0
        else:
            if abs(d_a) > abs(d_b):
                self.stepper1.divider = abs(d_a / d_b)
                self.stepper2.divider = 1.0
            else:
                self.stepper1.divider = 1.0
                self.stepper2.divider = abs(d_b / d_a)

        #synchronized movement of pen to new position
        self.stepper1.in_queue.put(int(a))
        self.stepper2.in_queue.put(int(b))
        self.stepper1.in_queue.join()
        self.stepper2.in_queue.join()

    def getXY(self):
        return (self.getX(), self.getY())

    def getX(self):
        a = self.stepper1.step
        b = self.stepper2.step
        a_cm = a / self.steps_per_cm
        b_cm = b / self.steps_per_cm
        l = self.l
        x = (a_cm**2 - b_cm**2 + l**2) / (2 * l)
        return x

    def getY(self):
        a = self.stepper1.step
        b = self.stepper2.step
        a_cm = a / self.steps_per_cm
        b_cm = b / self.steps_per_cm
        l = self.l
        y = sqrt(a_cm**2 - (a_cm**2 - b_cm**2 + l**2)**2/(4 * l**2))
        return y

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
