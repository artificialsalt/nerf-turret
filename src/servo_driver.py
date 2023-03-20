'''!
@file servo_driver.py
This file contains a class that allows the user to instantiate a servo driver.

@author Chayton Ritter, Richard Kwan, Jackie Chen
@date 9-Mar-2023
'''

# Import pyboard module
import pyb

class ServoDriver:
    '''!
    This class implements a servo driver for a position-controlled servo.
    '''

    def __init__(self, pwm_pin:str, timer:int, ch: int):
        '''!
        Creates a servo driver and configures the appropriate pins, timers, and timer channels.
        @param pwm_pin String containing the pin label of the PWM pin (e.g. 'A10' for pin A10)
        @param timer Number of the timer to configure, given as integer (e.g. 5 for TIM5)
        @param ch The channel number of the PWM pin, given as integer
        '''
        
        # Pin and timer configurations       
        ## Pin object for PWM pin
        self.pwm_pin = pyb.Pin(pwm_pin, pyb.Pin.OUT_PP)

        ## Timer object for the servo driver
        self.timer = pyb.Timer(timer, freq=50)               

        # Configures pins and their appropriate timer channels to PWM mode
        ## Channel object for PWM channel
        self.pwm = self.timer.channel(ch, pyb.Timer.PWM, pin=self.pwm_pin)  

    def return_to_zero(self):
        self.set_position(0)

    def set_position (self, position:int):
        '''!
        Sets the servo position based on the PWM level.
        @param level PWM duty cycle to move the servo. Given as integer from -90 to 90 (inclusive). Overall range may vary depending on servo model.
        '''

        duty = (position - (-90)) * (10 - 5) / (90 - (-90)) + 5

        self.pwm.pulse_width_percent(duty)
