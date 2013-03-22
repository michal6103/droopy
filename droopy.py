import stepper

stepper_pins1 = (7, 11, 12, 13)
stepper_pins2 = (15, 16, 18, 22)

stepper1 = stepper.Stepper(stepper_pins1)
stepper2 = stepper.Stepper(stepper_pins2)

stepper1.connect()
stepper2.connect()
while 1:
    stepper1.step_forward()
    stepper2.step_forward()
