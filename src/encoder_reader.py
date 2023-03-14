'''!
@file encoder_reader.py
This file contains a class that allows the user to instantiate a motor encoder.

@author Chayton Ritter, Richard Kwan, Jackie Chen
@date 24-Jan-2023
'''

# Import pyboard module
import pyb 

class EncoderReader:
    '''!
    This class implements an encoder reader for an ME 405 kit.
    '''

    def __init__(self, pin1:str, pin2:str, timer:int, ch1:int, ch2:int):
        '''!
        Creates an encoder reader and configures the appropriate pins, timers, and timer channels.
        @param pin1 String containing the pin label for the first encoder channel (e.g. 'A10' for pin A10)
        @param pin2 String containing the pin label for the second encoder channel
        @param timer Number of the timer to configure, given as integer (e.g. 5 for TIM5)
        @param ch1 The channel number of the first encoder channel, given as integer (e.g. 1 for TIMx CH1)
        @param ch2 The channel number of the second encoder channel, given as integer
        '''

        # Pin, timer, and channel configuration
        ## Pin object for pin 1
        self.pin1 = pyb.Pin(pin1, pyb.Pin.OUT_PP)                               
        ## Pin object for pin 2
        self.pin2 = pyb.Pin(pin2, pyb.Pin.OUT_PP)                               
        ## Timer object for the encoder
        self.timer = pyb.Timer(timer, prescaler=0, period=0xFFFF)               
        ## Channel object for channel 1 
        self.ch1 = self.timer.channel(ch1, pyb.Timer.ENC_AB, pin=self.pin1)    
        ## Channel object for channel 2 
        self.ch2 = self.timer.channel(ch2, pyb.Timer.ENC_AB, pin=self.pin2)    

        # Initialize encoder position to zero
        ## Current position of the motor
        self.position = 0   
        ## Reference count value for measuring difference between readings
        self.prev_cnt = 0   

    def zero(self):
        '''!
        Sets the current position of the encoder to zero (does not modify the timer count).
        '''
        self.prev_cnt = self.timer.counter()
        self.position = 0
    
    def read(self):
        '''!
        Reads the current position of the encoder.
        @returns self.position Current position of the encoder
        '''
        # Calculate difference in position
        current_cnt = self.timer.counter()
        diff = current_cnt - self.prev_cnt 

        # Handle overflow and underflow 
        if diff < -(65536/2):       # Overflow adjustment
            diff += 65536
        elif diff > (65536/2):      # Underflow adjustment
            diff -= 65536

        # Set previous count value to current count value
        self.prev_cnt = current_cnt

        # Add distance to position measurement
        self.position += diff

        return self.position
