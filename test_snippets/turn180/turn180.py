import motor_driver
import encoder_reader
import closedloopcontrol
import utime

# Initialize motor/encoder/controller 1
M1 = motor_driver.MotorDriver('A10', 'B4', 'B5', 3, 1, 2)
E1 = encoder_reader.EncoderReader('C6', 'C7', 8, 1, 2)
C1 = closedloopcontrol.cl_loop(0.75, 0)
M1.enable_motor()

# Initialize motor/encoder/controller 2
M2 = motor_driver.MotorDriver('C1', 'A0', 'A1', 5, 1, 2)
E2 = encoder_reader.EncoderReader('B6', 'B7', 4, 1, 2)
C2 = closedloopcontrol.cl_loop(0.5, -1000)
M2.enable_motor()

while True:
    try:
        #vert_duty = C2.run(E2.read())
        #M2.set_duty_cycle(vert_duty)
        horiz_duty = C1.run(E1.read())
        M1.set_duty_cycle(horiz_duty)
        utime.sleep_ms(5)
    except KeyboardInterrupt:
        print("Stopping turret...")
        M1.set_duty_cycle(0)
        M1.disable_motor()
        M2.set_duty_cycle(0)
        M2.disable_motor()
        break

