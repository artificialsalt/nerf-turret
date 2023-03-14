'''!
@file closedloopcontrol.py
This file contains a class that allows the user to instantiate a proportional controller for a motor.

@author Jackie Chen, Richard Kwan, Chayton Ritter
@date 31-Jan-2023
'''

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

    def run(self, output):
        '''!
        Evaluates the difference between motor position and setpoint, and returns a pwm percentage

        @param output Integer representing current motor position in encoder ticks
        '''

        pwm = self.gain*(self.setpoint - output)                        # Generate pwm percentage
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