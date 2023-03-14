'''!
@file closedloopcontrol.py
This file contains a class that allows the user to instantiate a proportional controller for a motor.

@author Jackie Chen, Richard Kwan, Chayton Ritter
@date 31-Jan-2023
'''

import utime

class cl_loop:
    '''!
    This class implements a proportional controller for an ME 405 kit.
    '''

    def __init__(self, gain, setpoint):
        '''!
        Creates a proportional controller with a gain and setpoint.
        @param gain Float variable representing the gain coefficient of the proportional control (Kp)
        @param setpoint Integer representing the desired motor position in encoder ticks
        '''
        
        # Class variables necessary for control
        ## Kp of the system
        self.gain = gain
        ## Desired position (in encoder ticks)
        self.setpoint = setpoint
        # Class variables used for data plotting
        ## Single list for both position and data (alternating positions)
        self.pos_data = []                          
        ## Reference time to calculate time elapsed between encoder readings
        self.prev_time = utime.ticks_ms()           
        ## Time elapsed since beginning of step response test
        self.time = 0                               

    def run(self, output):
        '''!
        Evaluates the difference between motor position and setpoint, and returns a pwm percentage

        @param output Integer representing current motor position in encoder ticks
        '''

        pwm = self.gain*(self.setpoint - output)                        # Generate pwm percentage

        # Collect time and position data for plotting
        interval = utime.ticks_diff(utime.ticks_ms(), self.prev_time)   # Calculate time interval
        self.time += interval                                           # Add to current time
        self.prev_time = utime.ticks_ms()                               # Set reference time for next run call
        self.pos_data.append(self.time)                                 # Append time and data for transmission back to PC
        self.pos_data.append(output)
        return pwm

    def set_setpoint(self, setpoint):
        '''!
        Sets the setpoint of the controller

        @param setpoint Integer representing desired final motor position in encoder ticks
        '''
        self.setpoint = setpoint

    def set_kp(self, gain):
        '''!
        Sets the gain of the controller

        @param gain Float representing the gain of the controller
        '''

        self.gain = gain

    def get_pos_data(self):
        '''!
        Returns the list of time and data (all in one list to make UART transmission easier)
        '''

        return self.pos_data