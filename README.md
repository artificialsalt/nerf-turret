# nerf-turret

This repository contains code to actuate a nerf gun turret that uses an infrared camera to aim at a target.

The main program will be designed such that the turret operates in the style of a duel, in which it starts facing away from a target before spinning 180 degrees and then shooting the target.

## Hardware Design

The software in this repository interfaces with a flywheel dart blaster mounted on a two-axis turret platform. The two axes are each driven by a brushed DC motor, both of which are driven by an H-bridge motor controller shield on a microcontroller. 

The flywheels are enabled by an output pin on the microcontroller via a MOSFET located inside the dart blaster. The microcontroller output pin acts as the MOSFET gate drive, while the drain and source are connected to the dart blaster's batteries and the flywheels, respectively.

The trigger mechanism on the dart blaster is actuated by a small servo. The servo is controlled and powered directly from the microcontroller using PWM and the onboard +5V power pin.

## Software Design

link to doxygen mainpage

## Results

describe tests, describe test performance

## Potential Improvements
