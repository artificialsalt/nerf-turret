import mlx_cam
import servo_driver
import motor_driver
import encoder_reader
import closedloopcontrol
import time
from pyb import Pin
from machine import I2C
from array import array

# Configure I2C bus
i2c_bus = I2C(1)

# Select MLX90640 camera I2C address, normally 0x33, and check the bus
i2c_address = 0x33
scanhex = [f"0x{addr:X}" for addr in i2c_bus.scan()]
print(f"I2C Scan: {scanhex}")

# Create the camera object and set it up in default mode
camera = mlx_cam.MLX_Cam(i2c_bus)

servo = servo_driver.ServoDriver('D13', 2, 1)
trigger_pin = Pin('D12', Pin.OUT_PP)

# Initialize motor/encoder/controller 1
M1 = motor_driver.MotorDriver('A10', 'B4', 'B5', 3, 1, 2)
E1 = encoder_reader.EncoderReader('C6', 'C7', 8, 1, 2)
C1 = closedloopcontrol.cl_loop(0.5, 0)
M1.enable_motor()

# Initialize motor/encoder/controller 2
M2 = motor_driver.MotorDriver('C1', 'A0', 'A1', 5, 1, 2)
E2 = encoder_reader.EncoderReader('B6', 'B7', 4, 1, 2)
C2 = closedloopcontrol.cl_loop(0.5, 0)
M2.enable_motor()

# Set trigger closed
servo.set_position(20)
trigger_pin.low()

time.sleep(3)

while True:
    try:
        # Get and image and see how long it takes to grab that image
        print("Click.", end='')
        image = camera.get_image()

        # Can show image.v_ir, image.alpha, or image.buf; image.v_ir best?
        # Display pixellated grayscale or numbers in CSV format; the CSV
        # could also be written to a file. Spreadsheets, Matlab(tm), or
        # CPython can read CSV and make a decent false-color heat plot.
        pixels = array('I')
        for line in camera.get_csv(image, limits=(0, 99)):
            pixel_row = array('I', [int(str_val) for str_val in line.split(',')])
            pixels += pixel_row
             
        #print(pixels)
        print('Image received, calculating position...')
        
        mask_threshold = 70
        width = 32
        length = 24
         
        # Mask the pixels
        for pixel in range(length*width):
            if pixels[pixel] < mask_threshold:
                pixels[pixel] = 0
            else:
                pixels[pixel] = 1

        # Compute center of mass (aimpoint)
        # Y coordinate
        mask_sum_y = 0
        wtd_sum_y = 0
        for row in range(length):
            mask_sum = sum(pixels[row*width : (row+1)*width-1])
            mask_sum_y += mask_sum
            wtd_sum_y += mask_sum * row
        try:
            com_y = wtd_sum_y / mask_sum_y
        except ZeroDivisionError:
            com_y = height/2

        # X coordinate
        mask_sum_x = 0
        wtd_sum_x = 0
        for col in range(width):
            mask_sum = 0
            for row in range(length):
                mask_sum += pixels[row * width + col]
            mask_sum_x += mask_sum 
            wtd_sum_x += mask_sum * col
        try:
            com_x = wtd_sum_x / mask_sum_x
        except ZeroDivisionError:
            com_x = width/2
           
        #print(f'COM: x: {com_x}, y: {com_y}')
       
        # Camera FOV characteristics
        x_fov = 55
        y_fov = 35

        # Defining the range of degrees from center
        x_min = -(x_fov/2)
        x_max = (x_fov/2)
        y_min = -(y_fov/2)
        y_max = (y_fov/2)

        # Mapping the COM to the FOV
        x_adj = (com_x) * (x_max - x_min) / (width) + x_min
        y_adj = (com_y) * (y_max - y_min) / (length) + y_min

        x_set = x_adj * (194000/180)
        C1.set_setpoint(E1.read()- x_set) # The camera is mirrored for some dumbass reason
        print(f'Moving turret {x_set} counts')
        
        while True:
            try:
                if abs(E1.read() - C1.setpoint) < 1000:
                    break
                #print(E1.read(), E1.read() - x_set)
                horiz_duty = C1.run(E1.read())
                M1.set_duty_cycle(horiz_duty)
                time.sleep_ms(5)
            except KeyboardInterrupt:
                print("Stopping turret...")
                M1.set_duty_cycle(0)
                M1.disable_motor()
                M2.set_duty_cycle(0)
                M2.disable_motor()
                break

        print('Move complete')
        M1.set_duty_cycle(0)
        M2.set_duty_cycle(0)
        time.sleep(1)
        
    except KeyboardInterrupt:
        break
    
