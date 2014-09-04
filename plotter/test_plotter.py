#!/usr/bin/env python3
import plotter
import unittest


class TestStepper(unittest.TestCase):

    def setUp(self):
        self.plotter = plotter.Plotter(debug=True)

#    def test_step_top_line(self):
#        self.plotter.gotoXY(self.plotter.l, 0)
#        self.assertEqual(self.plotter.getXY(), (self.plotter.l, 0))

    def test_step_left_line(self):
        self.plotter.gotoXY(0, self.plotter.l)
        self.assertEqual(self.plotter.getXY(), (0, self.plotter.l))

if __name__ == '__main__':
    unittest.main()
