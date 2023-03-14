import servo_driver
import utime

# Initializes servo object
servo = servo_driver.ServoDriver('D13', 2, 1)

# Actuates servo twice (needs two pushes to push the dart all the way)
servo.set_position(-100)
utime.sleep_ms(250)
servo.set_position(20)
utime.sleep_ms(250)