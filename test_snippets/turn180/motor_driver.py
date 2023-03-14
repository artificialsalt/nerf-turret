'''!
@file motor_driver.py
This file contains a class that allows the user to instantiate a motor driver.

@author Chayton Ritter, Richard Kwan, Jackie Chen
@date 24-Jan-2023
'''

# Import pyboard module
import pyb

class MotorDriver:
    '''!
    This class implements a motor driver for an ME 405 kit.
    '''

    def __init__(self, en_pin:str, in1pin:str, in2pin:str, timer:int, ch1:int, ch2:int):
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
        ## Pin object for the enable pin
        self.en_pin = pyb.Pin(en_pin, pyb.Pin.OUT_PP)           
        ## Pin object for pin 1
        self.in1pin = pyb.Pin(in1pin, pyb.Pin.OUT_PP)           
        ## Pin object for pin 2
        self.in2pin = pyb.Pin(in2pin, pyb.Pin.OUT_PP)           
        ## Timer object for the motor driver
        self.timer = pyb.Timer(timer, freq=20000)               

        # Disables motor pin for safety
        self.en_pin.low()

        # Configures pins and their appropriate timer channels to PWM mode
        ## Channel object for PWM channel 1
        self.pwm1 = self.timer.channel(ch1, pyb.Timer.PWM, pin=self.in1pin)    
        ## Channel object for PWM channel 2 
        self.pwm2 = self.timer.channel(ch2, pyb.Timer.PWM, pin=self.in2pin)    

    def enable_motor(self):
        '''!
        Enables the motor by driving the enable pin high.
        '''
        self.en_pin.high()

    def disable_motor(self):
        '''!
        Disables the motor by driving the enable pin low.
        '''
        self.en_pin.low()

    def set_duty_cycle (self, level:int):
        '''!
        Drives the motor at a given duty cycle.
        @param level PWM duty cycle to drive the motor at. Given as integer from -100 to 100 (inclusive). The sign affects the direction the motor will be driven.
        '''
        if level >= 0:
            if level > 100:
                level = 100
            self.pwm1.pulse_width_percent(level)
            self.pwm2.pulse_width_percent(0)
        else:
            if level < -100:
                level = -100
            self.pwm1.pulse_width_percent(0)
            self.pwm2.pulse_width_percent(-(level))
