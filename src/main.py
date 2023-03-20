'''!
@file main.py
This file contains code to perform a nerf turret duel. 

@author Jackie Chen, Richard Kwan, Chayton Ritter
@date 14-Mar-2023
'''

# Motion-related imports
import servo_driver
import motor_driver
import encoder_reader
import closedloopcontrol
# Hardware imports
import mlx_cam
from pyb import Pin
from machine import I2C
# Utility imports
import time
from array import array

# -----------------------------------
# CONFIGURATION/TUNING
# -----------------------------------
# MEC1 (horizontal aiming axis)
MEC1_tickratio = (194000/180)           # Horizontal axis ticks to degrees ratio
MEC1_gain = 0.7                         # Horizontal axis gain
# MEC2 (vertical aiming axis)
MEC2_tickratio = (2300/100)             # Vertical axis ticks to degrees ratio
MEC2_gain = 0.7                         # Vertical axis gain
# MLX Camera
horiz_correction = 0                    # Angle correction for horizontal axis
vert_correction = 15                    # Angle correction for vertical axis
x_fov = 55                              # Camera FOV in x direction
y_fov = 35                              # Camera FOV in y direction
mask_threshold = 75                     # Minimum "heat" value to be seen as target pixel
width = 32                              # Camera resolution width
length = 24                             # Camera resolution length
angle_prescale = 0.5                    # Ratio of the angle to target from camera and angle to target from turret

# -----------------------------------
# INITIALIZATION
# The turret initializes all necessary hardware and peripherals.
# -----------------------------------

# FIRING MECHANISM
# Trigger servo
servo = servo_driver.ServoDriver('D13', 2, 1)
# Flywheel relay control pin
trigger_pin = Pin('D12', Pin.OUT_PP)

# MOTOR AXES
# Initialize motor/encoder/controller 1
M1 = motor_driver.MotorDriver('A10', 'B4', 'B5', 3, 1, 2)
E1 = encoder_reader.EncoderReader('C6', 'C7', 8, 1, 2)
C1 = closedloopcontrol.cl_loop(MEC1_gain, 0)
M1.enable_motor()

# Initialize motor/encoder/controller 2
M2 = motor_driver.MotorDriver('C1', 'A0', 'A1', 5, 1, 2)
E2 = encoder_reader.EncoderReader('B6', 'B7', 4, 1, 2)
C2 = closedloopcontrol.cl_loop(MEC2_gain, 0)
M2.enable_motor()

# MLX IR CAMERA
# Configure I2C bus
i2c_bus = I2C(1)
i2c_address = 0x33
# Create the camera object and set it up in default mode
camera = mlx_cam.MLX_Cam(i2c_bus)
# Set refresh rate to 64 Hz
ctrl_reg_val = 0b0001101110000001
i2c_bus.writeto_mem(i2c_address, 0x800D, ctrl_reg_val.to_bytes(16, 'big'))

# TURRET SAFE
servo.set_position(20)
trigger_pin.low()


# -----------------------------------
# TASK DEFINITIONS
# All the things the turret needs to do
# -----------------------------------

# Run the motor to the desired setpoint
def run_motor(motor, encoder, controller):
    motor_pwm = controller.run(encoder.read())
    motor.set_duty_cycle(motor_pwm)
    return
        
def aim(camera):
    # Get raw image
    image = camera.get_image()

    # Get pixel heat as a number from 0 to 99
    pixels = array('I')
    for line in camera.get_csv(image, limits=(0, 99)):
        #print(line)
        pixel_row = array('I', [int(str_val) for str_val in line.split(',')])
        pixels += pixel_row
     
    # Mask the pixels, discard 4 pixels on the left and right sides due to noise
    for pixel in range(length*width):
        if pixels[pixel] > mask_threshold:
            pixels[pixel] = 1
        else:
            pixels[pixel] = 0

    # Discard outlier pixels
    for pixel in range(length*width):
        if pixels[pixel] == 1:
            neighbors = []
            try:
                nb1 = pixels[pixel-width-1]
                neighbors.append(nb1)
            except IndexError:
                pass
            try:
                nb2 = pixels[pixel-width]
                neighbors.append(nb2)
            except IndexError:
                pass
            try:
                nb3 = pixels[pixel-width+1]
                neighbors.append(nb3)
            except IndexError:
                pass
            try:
                nb4 = pixels[pixel-1]
                neighbors.append(nb4)
            except IndexError:
                pass
            try:
                nb6 = pixels[pixel+1]
                neighbors.append(nb6)
            except IndexError:
                pass
            try:
                nb7 = pixels[pixel+width-1]
                neighbors.append(nb7)
            except IndexError:
                pass
            try:
                nb8 = pixels[pixel+width]
                neighbors.append(nb8)
            except IndexError:
                pass
            try:
                nb9 = pixels[pixel+width+1]
                neighbors.append(nb9)
            except IndexError:
                pass
            if 1 not in neighbors:
                pixels[pixel] = 0

    # Compute center of mass (aimpoint)
    # Y coordinate
    mask_sum_y = 0
    wtd_sum_y = 0
    for row in range(length):
        mask_sum = sum(pixels[row*width : (row+1)*width-1])
        mask_sum_y += mask_sum
        wtd_sum_y += mask_sum * (row + 0.5)
    try:
        com_y = wtd_sum_y / mask_sum_y
    except ZeroDivisionError:
        com_y = 11.5

    # X coordinate
    mask_sum_x = 0
    wtd_sum_x = 0
    for col in range(width):
        mask_sum = 0
        for row in range(length):
            mask_sum += pixels[row * width + col]
        mask_sum_x += mask_sum 
        wtd_sum_x += mask_sum * (col + 0.5)
    try:
        com_x = wtd_sum_x / mask_sum_x
    except ZeroDivisionError:
        com_x = 15.5

    # Defining the range of degrees from center
    x_min = -(x_fov/2)
    x_max = (x_fov/2)
    y_min = -(y_fov/2)
    y_max = (y_fov/2)

    # Mapping the COM to the FOV
    x_adj = (com_x) * (x_max - x_min) / (width) + x_min
    y_adj = (com_y) * (y_max - y_min) / (length) + y_min

    # Create setpoints
    x_adj += horiz_correction
    y_adj += vert_correction
    new_setpoint_x = E1.read() - (x_adj * MEC1_tickratio * angle_prescale)
    new_setpoint_y = E2.read() - (y_adj * MEC2_tickratio)
    return new_setpoint_x, new_setpoint_y


# ------------------------------------
# STATE DEFINITIONS
# All the states the turret will be in
# ------------------------------------       

S0_INIT = 0
S1_TURN180 = 1
S2_AIM = 2
S3_ADJUST = 3
S4_SHOOT = 4
S5_SAFE = 5
S6_AIM2 = 6
S7_ADJUST2 = 7

# ------------------------------------
# ACTUAL PROGRAM
# Pew pew
# ------------------------------------

if __name__ == '__main__':
    
    state = S0_INIT
    #time.sleep(5)

    while True:
        try:
            if state == S0_INIT:
                # Start the turret, begin a 5 second timer
                time_start180 = time.ticks_ms()
                state = S1_TURN180
                
            elif state == S1_TURN180:
                # Turn the turret 180 degrees
                C1.set_setpoint(180 * MEC1_tickratio)
                if time.ticks_diff(time.ticks_ms(), time_start180) > 5000:
                    state = S2_AIM
                
            elif state == S2_AIM:
                # Allow camera to refresh
                time.sleep(1/32)
                x_target_stpt, y_target_stpt = aim(camera)
                state = S3_ADJUST
                adjust_time = time.ticks_ms()
            
            elif state == S3_ADJUST:
                # Change setpoints to aim turret at target                
                C1.set_setpoint(x_target_stpt)
                C2.set_setpoint(y_target_stpt)
                if time.ticks_diff(time.ticks_ms(), adjust_time) > 500:
                    state = S4_SHOOT
                
            elif state == S4_SHOOT:
                
                # Spin up the flywheels, wait for them to get to speed
                trigger_pin.high()
                time.sleep(2)
                
                # Shoot once (sometimes the dart needs extra encouragement so the plunger pushes twice)
                servo.set_position(-100)
                time.sleep(0.2)
                servo.set_position(20)
                time.sleep(0.2)
                servo.set_position(-100)
                time.sleep(0.2)
                servo.set_position(20)
                time.sleep(0.2)
                servo.set_position(-100)
                time.sleep(0.2)
                
                state = S5_SAFE
            else:
                # Disable everything
                servo.set_position(20)
                trigger_pin.low()
                M1.disable_motor()
                M2.disable_motor()

            # Run motors
            run_motor(M1, E1, C1)
            #run_motor(M2, E2, C2)
            time.sleep_ms(5)
        except KeyboardInterrupt:
            # Disable everything
            servo.set_position(20)
            trigger_pin.low()
            M1.disable_motor()
            M2.disable_motor()
            break
        
