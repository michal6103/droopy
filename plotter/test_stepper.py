#!/usr/bin/env python3
import stepper
import unittest


class TestStepper(unittest.TestCase):

    def setUp(self):
        self.stepper_pins = False
        self.stepper = stepper.Stepper(self.stepper_pins, debug=True)
        self.stepper.connected = True

    def test_steps_forward(self):
        #Test all forward movement states
        self.stepper.step_forward()
        self.assertEqual(self.stepper._step_outputs, self.stepper.STEPS[1])
        self.stepper.step_forward()
        self.assertEqual(self.stepper._step_outputs, self.stepper.STEPS[2])
        self.stepper.step_forward()
        self.assertEqual(self.stepper._step_outputs, self.stepper.STEPS[3])
        self.stepper.step_forward()
        self.assertEqual(self.stepper._step_outputs, self.stepper.STEPS[4])
        self.stepper.step_forward()
        self.assertEqual(self.stepper._step_outputs, self.stepper.STEPS[5])
        self.stepper.step_forward()
        self.assertEqual(self.stepper._step_outputs, self.stepper.STEPS[6])
        self.stepper.step_forward()
        self.assertEqual(self.stepper._step_outputs, self.stepper.STEPS[7])
        self.stepper.step_forward()
        self.assertEqual(self.stepper._step_outputs, self.stepper.STEPS[0])

    def test_steps_backward(self):
        #Test all backward movement states
        self.stepper.step_backward()
        self.assertEqual(self.stepper._step_outputs, self.stepper.STEPS[7])
        self.stepper.step_backward()
        self.assertEqual(self.stepper._step_outputs, self.stepper.STEPS[6])
        self.stepper.step_backward()
        self.assertEqual(self.stepper._step_outputs, self.stepper.STEPS[5])
        self.stepper.step_backward()
        self.assertEqual(self.stepper._step_outputs, self.stepper.STEPS[4])
        self.stepper.step_backward()
        self.assertEqual(self.stepper._step_outputs, self.stepper.STEPS[3])
        self.stepper.step_backward()
        self.assertEqual(self.stepper._step_outputs, self.stepper.STEPS[2])
        self.stepper.step_backward()
        self.assertEqual(self.stepper._step_outputs, self.stepper.STEPS[1])
        self.stepper.step_backward()
        self.assertEqual(self.stepper._step_outputs, self.stepper.STEPS[0])

    def test_step_to(self):
        #Test step_to function
        self.stepper.step_to(1.1)
        self.assertEqual(self.stepper.step, 1)
        self.stepper.step_to(0)
        self.assertEqual(self.stepper.step, 0)
        self.stepper.step_to(100)
        self.assertEqual(self.stepper.step, 100)
        self.stepper.step_to(-100)
        self.assertEqual(self.stepper.step, -100)
        self.stepper.step_to(0)
        self.assertEqual(self.stepper.step, 0)
        self.stepper.step_to(23400.0)
        self.assertEqual(self.stepper.step, 23400)

    def test_step_divider_range(self):
        with self.assertRaises(ValueError):
            self.stepper.divider = 0.33
        with self.assertRaises(ValueError):
            self.stepper.divider = -5.0
        with self.assertRaises(ValueError):
            self.stepper.divider = 0.0

    def test_step_divider_2(self):
        self.stepper.step_to(0.0)
        self.stepper.divider = 2.0
        self.stepper.step_forward()
        self.assertEqual(self.stepper.step, 0.5)
        self.stepper.step_forward()
        self.assertEqual(self.stepper.step, 1.0)
        self.stepper.step_backward()
        self.assertEqual(self.stepper.step, 0.5)
        self.stepper.step_backward()
        self.assertEqual(self.stepper.step, 0.0)
        self.stepper.step_backward()
        self.assertEqual(self.stepper.step, -0.5)
        self.stepper.step_backward()
        self.assertEqual(self.stepper.step, -1.0)

    def test_stepper_non_divisible_destination_by_divider(self):
        self.stepper.step_to(0.0)
        self.stepper.divider = 7
        self.stepper.step_to(1.0)
        self.assertEqual(self.stepper.step, 1.0)
        self.stepper.step_to(-1.0)
        self.assertEqual(self.stepper.step, -1.0)

if __name__ == '__main__':
    unittest.main()
