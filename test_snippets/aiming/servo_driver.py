'''!
@file motor_driver.py
This file contains a class that allows the user to instantiate a motor driver.

@author Chayton Ritter, Richard Kwan, Jackie Chen
@date 24-Jan-2023
'''

# Import pyboard module
import pyb

class ServoDriver:
    '''!
    This class implements a motor driver for an ME 405 kit.
    '''

    def __init__(self, pwm_pin:str, timer:int, ch: int):
        '''!
        Creates a motor driver and configures the appropriate pins, timers, and timer channels.
        @param en_pin String containing the pin label of the enable pin (e.g. 'A10' for pin A10)
        @param in1pin String containing the pin label of the first PWM channel
        @param in2pin String containing the pin label of the second PWM channel
        @param timer Number of the timer to configure, given as integer (e.g. 5 for TIM5)
        @param ch1 The channel number of the first PWM channel, given as integer (e.g. 1 for TIMx CH1)
        @param ch2 The channel number of the second PWM channel, given as integer
        '''
        
        # Pin and timer configurations       
        ## Pin object for pin 1
        self.pwm_pin = pyb.Pin(pwm_pin, pyb.Pin.OUT_PP)

        ## Timer object for the motor driver
        self.timer = pyb.Timer(timer, freq=50)               

        # Configures pins and their appropriate timer channels to PWM mode
        ## Channel object for PWM channel 1
        self.pwm = self.timer.channel(ch, pyb.Timer.PWM, pin=self.pwm_pin)  

    def return_to_zero(self):
        self.set_position(0)

    def set_position (self, position:int):
        '''!
        Drives the motor at a given duty cycle.
        @param level PWM duty cycle to drive the motor at. Given as integer from -100 to 100 (inclusive). The sign affects the direction the motor will be driven.
        '''

        #90 -> 10
        #-90 -> 5
        duty = (position - (-90)) * (10 - 5) / (90 - (-90)) + 5

        self.pwm.pulse_width_percent(duty)
