import stepper

stepper_pins1 = (7, 11, 12, 13)
stepper_pins2 = (15, 16, 18, 22)

stepper1 = stepper.Stepper(stepper_pins1)
stepper2 = stepper.Stepper(stepper_pins2)

stepper1.connect()
stepper2.connect()

#stepper2.divider = 5
stepper1.in_queue.put(-50000)
stepper2.in_queue.put(50000)
#stepper1.in_queue.put(0)
#stepper2.in_queue.put(0)
stepper1.in_queue.put('stop')
stepper2.in_queue.put('stop')
stepper1.in_queue.join()
stepper2.in_queue.join()
