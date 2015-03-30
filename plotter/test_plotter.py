#!/usr/bin/env python3
import plotter
import unittest


class TestPlotter(unittest.TestCase):

    def setUp(self):
        #Debug must be true so plotter will not send  steps over GPIO
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

    def test_vertical_line(self):
        #Initialisation into the middle of the plotter
        x = self.plotter.l // 2
        y = 0
        self.plotter.gotoXY(x, y)

        #Vertical move
        x = self.plotter.l // 2
        y = self.plotter.l
        self.plotter.gotoXY(x, y)
        self.assertTrue(abs(self.plotter.getX() - x) < self.tolerance)
        self.assertTrue(abs(self.plotter.getY() - y) < self.tolerance)

    def test_move_to_same_position(self):
        x = 10
        y = 10
        self.plotter.gotoXY(x, y)
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
