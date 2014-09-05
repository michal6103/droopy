#!/usr/bin/env python3
import plotter
import unittest


class TestStepper(unittest.TestCase):

    def setUp(self):
        self.plotter = plotter.Plotter(debug=True)
        self.tolerance = self.plotter.steps_per_cm

    def test_step_top_line(self):
        self.plotter.gotoXY(self.plotter.l, 0)
        self.assertEqual(self.plotter.getXY(), (self.plotter.l, 0))

    def test_left_line(self):
        x = 0
        y = self.plotter.l
        self.plotter.gotoXY(x, y)
        self.assertTrue(abs(self.plotter.getX() - x) < self.tolerance)
        self.assertTrue(abs(self.plotter.getY() - y) < self.tolerance)

    def test_every_cm_in_lxl(self):
        l = int(self.plotter.l)
        for x in range(l):
            for y in range(l):
                self.plotter.gotoXY(x, y)
                self.assertTrue(abs(self.plotter.getX() - x) < self.tolerance)
                self.assertTrue(abs(self.plotter.getY() - y) < self.tolerance)

if __name__ == '__main__':
    unittest.main()
