class DummyGPIO:
    """ Dummy GPIO library used for debugging on non-rPi platforms
    """

    OUT = "Output"
    IN = "Input"

    BOARD = "Board"
    BCM = "BCM"

    def setup(pin, mode):
        """Simulates initialisation of input or outpu mode of GPIO pin
        """
        pass

    def setmode(mode):
        """Simulates setup of pin numbers as BCM or BOARD
        """
        pass

    def cleanup():
        """Simulates cleanup of GPIO
        """
        pass

    def output(pin, value):
        """Simulates setting the value to pin
        """
        pass
