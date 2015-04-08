#!/usr/bin/env python3
import stepper
from math import sqrt
import urllib.request
import json
import logging
import os
import time


logger = logging.getLogger(__name__)
#logger.propagate = False

def load_config():
    """Method load configuration from configuration file
    """
    config = None
    try:
        config_file_path = os.path.join(os.path.dirname(__file__),'config.json')
        config_file = open(config_file_path)
        config = json.load(config_file)
        logger.debug('Parsed config file: ', config)
    except IOError: 
        logger.info("Parsing the JSON config file: %s", config_file.name)
    except ValueError:
        logger.error("Parsing of JSON config failed")
    else:
        validate_config(config)
    return config

def validate_config(config):
    """Method check if the required config params are present

    :param config:dicctionary containing configuration
    """
    try:
        config['plotter']["logging_level"]
        config['plotter']["steps_per_cm"]
        config['plotter']["width"]
        config['stepper1']['pins']
        config['stepper2']['pins']
    except KeyError as key:
        logger.error("Missing %s setting in config", key)
        raise

def setup_logger():
    """Function set up logger. At first it delete root handlers from stepper modules to override it from configuration file
    """
    logging.root.handlers = []
    logging.basicConfig(level=CONFIG['plotter']['logging_level'])

CONFIG = load_config()
setup_logger()

class Plotter:
    """Class controlling the plotter
    """
    stepper1_pins = CONFIG['stepper1']['pins']
    stepper2_pins = CONFIG['stepper2']['pins'] 
    stepper1 = None
    stepper2 = None
    steps_per_cm = CONFIG['plotter']['steps_per_cm']
    #l is plotter width from edge of one servo to other in centimeters
    l = CONFIG['plotter']['width']

    def __init__(self, x=0.0, y=0.0, l=52.0, debug=False):
        """Initialisation of plotter with physical parameters

        :param x: Initial X position of the pen in centimeters.
            Positive number from distance from left stepper to the pen tip.
        :param y: Initial Y position of the pen in centimeters.
            Positive number measuring distance from top of steppers to the pen tip
        :param l: Width of plotter measured from middle of one stepper to middle of second stepper.
        :param debug: Debug mode disables physical GPIO outputs. Useful for debugging and testing"""
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
        #b must be negative so the right stepper is rotating in reverse
        b = -int(b_cm * self.steps_per_cm)

        self.stepper1.step = a
        self.stepper2.step = b

        self.stepper1.connect()
        self.stepper2.connect()

    def gotoXY(self, x, y):
        """Move pen to position X,Y

        :param x: Horizontal destination. Positive number from distance from left stepper to the pen tip.
        :param y: Vertical destination. Positive number measuring distance from top of steppers to the pen tip
        """
        logger.info("New XY: {},{}".format(x, y))
        l = self.l

        a_cm = sqrt(x ** 2 + y ** 2)
        a = int(a_cm * self.steps_per_cm)
        d_a = a - self.stepper1.step

        b_cm = sqrt((l - x) ** 2 + y ** 2)
        #b must be negative so the right stepper is rotating in reverse
        b = -int(b_cm * self.steps_per_cm)
        d_b = b - self.stepper2.step

        logger.debug("New ab: {},{}".format(a, b))
        logger.debug("Delta ab: {},{}".format(d_a, d_b))

        #speed reduction of shorter position change
        if abs(d_a) > abs(d_b):
            self.stepper1.divider = 1.0
            try:
                self.stepper2.divider = abs(d_a / d_b)
            except ZeroDivisionError:
                self.stepper2.divider = float("inf")
        else:
            try:
                self.stepper1.divider = abs(d_b / d_a)
            except:
                self.stepper1.divider = float("inf")
            self.stepper2.divider = 1.0

        logger.debug("Dividers: {},{}".format(
            self.stepper1.divider,
            self.stepper2.divider))
        #synchronized movement of pen to new position
        self.stepper1.in_queue.put(int(a))
        self.stepper2.in_queue.put(int(b))
        self.stepper1.in_queue.join()
        self.stepper2.in_queue.join()

    def getXY(self):
        """ Function takes actual step positions of steppers and return orthogonal coordinates of the pen in centimeters.

        :return: Tuple with XY coordinates of the pen
        """
        return (self.getX(), self.getY())

    def getX(self):
        """ Function takes actual step positions of steppers and returns horizontal coordinate of the pen centimeters.

        :return: Horizontal coordinate of the pen
        """
        a = self.stepper1.step
        b = self.stepper2.step
        a_cm = a / self.steps_per_cm
        b_cm = b / self.steps_per_cm
        l = self.l
        x = (a_cm ** 2 - b_cm ** 2 + l ** 2) / (2 * l)
        return x

    def getY(self):
        """ Function takes actual step positions of steppers and returns vertical coordinate of the pen in centimeters.

        :return: Vertical coordinate of the pen
        """
        a = self.stepper1.step
        b = self.stepper2.step
        a_cm = a / self.steps_per_cm
        b_cm = b / self.steps_per_cm
        l = self.l
        y = sqrt(a_cm ** 2 - (a_cm ** 2 - b_cm ** 2 + l ** 2) ** 2 / (4 * l ** 2))
        return y

    def stop(self):
        """ Stop the stepper threads on destruction
        """ 
        logger.info("Clearing queues")
        with self.stepper1.in_queue.mutex:
            self.stepper1.in_queue.queue.clear()
        with self.stepper2.in_queue.mutex:
            self.stepper2.in_queue.queue.clear()
        logger.info("Putting Stop to both stepper queues")
        self.stepper1.in_queue.put('stop')
        self.stepper2.in_queue.put('stop')
        while self.stepper1.is_alive() or self.stepper2.is_alive():
            logger.info("Waiting for stepper threads to finish")
            time.sleep(0.1)

if __name__ == "__main__":
    #url = 'http://192.168.0.103:5000/json'
    url = 'http://web-droopy.rhcloud.com/json'
    response = urllib.request.urlopen(url)
    str_response = response.readall().decode('utf-8')
    image = json.loads(str_response)
    try:
        plotter = Plotter(x=11.0, y=30.0, l=54.0, debug=False)
        for x,y in image["analog_data"]:
            plotter.gotoXY(x, y)
        #for y in range(36)[::5]:
        #    for x in range(33):
        #        plotter.gotoXY(11 + x, 30 + y)
        plotter.gotoXY(11, 75)
        plotter.gotoXY(11, 30)
    except KeyboardInterrupt:
        logger.info("CTRL+C: Quitting")
    finally:
        plotter.stop()
    logger.info("Done")
