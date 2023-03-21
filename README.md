# nerf-turret

This repository contains code to actuate a nerf gun turret that uses an infrared camera to aim at a target. This software can be used as a basis for those creating their own infrared-aiming nerf blaster turret. This was created as part of a final project for an ME 405 class. 

The main program is designed such that the turret operates in the style of a duel, in which it starts facing away from a target before spinning 180 degrees and then shooting the target.

## Hardware Design

The software in this repository interfaces with a flywheel dart blaster mounted on a two-axis turret platform. The two axes are each driven by a brushed DC motor, both of which are driven by an H-bridge motor controller shield on a microcontroller. Both axes are belt-driven. The horizontal axis was constructed using a 12 inch diameter lazy susan, with the outer ring of the lazy susan being stationary. In order to rotate the inner ring, a GT2 timing belt was wrapped around the outer ring and around the 20T pulley of the horizontal drive motor. When the pulley turns, it moves along the belt and rotates the entire assembly. The vertical axis was constructed by placing two 3d-printed bearing blocks on top of two vertical pieces of wood, and then placing a wooden dowel into the bearing blocks. The blaster was fixed to the dowel using a 3d-printed mount. The vertical axis was actuated using standard GT2 20T pulley and a 3d printed 60T pulley.

The flywheels are enabled by an output pin on the microcontroller via a relay. The microcontroller output pin is connected to the base of an NPN bipolar junction transistor, whose collector is connected to the coil of the relay. When the output pin is set high, current flows through the coil and closes the switch, powering the flywheels. The relay is powered by a 5V buck converter that steps down the 12V from the power supply.

The trigger mechanism on the dart blaster is actuated by a small servo. The servo slides the blaster's trigger back and forth to move a plunger that moves a loaded dart into the flywheels. The servo is controlled by the microcontroller and is powered by the same 5V buck converter powering the relay. 

The blaster is aimed using an MLX90640 infrared camera. This camera is connected to the microcontroller using an I2C bus.

Below is a picture of the completed dart blaster.

![Completed blaster](/img/turret.jpg)

Below is the wiring diagram of the completed system.

![Turret wiring diagram](/img/405nt_wiring_diagram.png)

## Software Design

The software for this dueling blaster turret was implemented as a finite state machine. The states reflect the individual phases that the turret will enter during a duel. These states incude turning around, detecting a target, aiming for a target, and shooting. Although one of the design objectives for this project was to implement task-sharing, the disparity of the execution time between the tasks as well as their nature made it impractical to do any real task-sharing. The two-axis motor control is the only "simultaneous" task execution.

For more detail on the software, including tasks and states, please go to the documentation linked below:

https://artificialsalt.github.io/nerf-turret/

## Results

In the initial iteration (with the camera mounted directly on the blaster), the turret was fairly accurate up to 12 feet, with some success as far as 15 feet. Tests were performed by running the duel program and then standing in a spot in front of the turret at varying positions. To assist in analyzing the aiming algorithm, the camera image was printed into the terminal for use with an external python script to show what the camera saw and where the turret decided to aim. Below is a video of one such test in action.

https://user-images.githubusercontent.com/60730126/226225105-c88e973f-6a27-4022-9a65-f2677933cf0b.mov

The same general process was used in the second iteration, where the camera was moved to an external mount. With the positions calibrated, the turret was fairly accurate, hitting the duel target 2 out of 3 times. However, when the camera and turret were moved to an uncalibrated position, it missed both shots, but with a fairly consistent angle error. This suggests that, when calibrated or corrected, the accuracy of the turret should increase.

## Potential Improvements

The camera had difficulties detecting a target beyond 12 feet. As the nature of the project required shooting distances of at least 16 feet, the camera had to be located several feet away from the turret platform in order to be effective. This complicated the calculation of the angle required to move as well as necessitating accurate position control of the turret platform. This makes the turret more sensitive to variances in setup and requires calibration for each unique setup compared to a camera mounted directly on the blaster. To remedy this, a better camera could be used or a more stable camera platform can be created. The algorithm for calculating the angle was also extremely primitive and abstained from the use of any trigonometry to reduce the processing power needed. This algorithm can be replaced to make the caalculation more accurate.

The horizontal turret drive had excessive mechanical advantage. While this allowed it to be extremely precise when moving to a given setpoint, it made the turret relatlively slow to turn around. Changing the horizontal drive mechanism to have a smaller ratio should be considered if rotation speed becomes an important factor.

The vertical turret drive only had a usable range of about +/- 15 degrees from level. This was due to the blaster's center of mass not being placed perfectly on the axis of rotation. As a result, even with a 48:1 ratio, the motor was only powerful enough to hold the blaster's elevation, and could not counteract the weight of the blaster. Using more powerful motors or increasing the reduction would improve this issue.

In order to allow the dart plunger to be actuated by the servo, a spring used for returning the mechanism had to be removed. In doing so, this caused the plunger to never fully return to the original position due to some play between the trigger and the plunger. The servo was also not powerful enough to overcome the friction of multiple darts being pushed onto the chambered dart. Loading even a single dart required three cycles of the servo for the dart to be fully pushed into the flywheels. Any recreating this project should consider using a more powerful servo and/or using another blaster that has motorized loading of darts.
