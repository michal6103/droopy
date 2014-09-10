#!/usr/bin/env python3
import stepper
from math import sqrt


class Plotter:
    stepper1_pins = (7, 11, 12, 13)
    stepper2_pins = (15, 16, 18, 22)
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

        a_cm = sqrt(x**2 + y**2)
        a = int(a_cm * self.steps_per_cm)
        b_cm = sqrt((l-x)**2 + y**2)
        b = int(b_cm * self.steps_per_cm)

        self.stepper1.step = a
        self.stepper2.step = b

        self.stepper1.connect()
        self.stepper2.connect()

    def gotoXY(self, x, y):
        #print("New XY: {},{}".format(x, y))
        l = self.l

        a_cm = sqrt(x**2 + y**2)
        a = int(a_cm * self.steps_per_cm)
        d_a = a - self.stepper1.step

        b_cm = sqrt((l - x)**2 + y**2)
        b = int(b_cm * self.steps_per_cm)
        d_b = b - self.stepper2.step

        print("New ab: {},{}".format(a, b))
        print("Delta ab: {},{}".format(d_a, d_b))
        print("Dividers: {},{}".format(
            self.stepper1.divider,
            self.stepper2.divider))

        #speed reduction of shorter position change
        if abs(d_a) == abs(d_b):
            self.stepper1.divider = 1.0
            self.stepper2.divider = 1.0
        else:
            if abs(d_a) > abs(d_b):
                self.stepper1.divider = 1.0
                self.stepper2.divider = abs(d_a / d_b)
            else:
                self.stepper1.divider = abs(d_b / d_a)
                self.stepper2.divider = 1.0

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
    try:
        plotter = Plotter(x=32.0, y=41.5, l=54.0)
        #plotter.gotoXY(20.0, 40.0)
        #plotter.gotoXY(34.0, 40.0)
        #plotter.gotoXY(34.0, 54.0)
        #plotter.gotoXY(20.0, 54.0)
        #plotter.gotoXY(20.0, 40.0)
        for i in range(100):
            plotter.gotoXY(32, 41.5)
            plotter.gotoXY(33, 40.25)
            plotter.gotoXY(34, 40)
            plotter.gotoXY(35, 40.25)
            plotter.gotoXY(36, 40.8)
            plotter.gotoXY(36.5, 42.5)
            plotter.gotoXY(36, 44)
            plotter.gotoXY(35, 46)
            plotter.gotoXY(34, 47)
            plotter.gotoXY(33, 48.5)
            plotter.gotoXY(32, 50)
            plotter.gotoXY(31, 48.5)
            plotter.gotoXY(30, 47)
            plotter.gotoXY(29, 46)
            plotter.gotoXY(28, 44)
            plotter.gotoXY(27.5, 42.5)
            plotter.gotoXY(28, 40.8)
            plotter.gotoXY(29, 40.25)
            plotter.gotoXY(30, 40)
            plotter.gotoXY(31, 40.25)
            plotter.gotoXY(32, 41.5)



    except KeyboardInterrupt:
        print('Quitting!')

    finally:
        plotter.stepper1.in_queue.put('stop')
        plotter.stepper2.in_queue.put('stop')
        plotter.stepper1.in_queue.join()
        plotter.stepper2.in_queue.join()
