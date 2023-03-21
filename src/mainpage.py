'''!
@mainpage nerf-turret

@author Jackie Chen, Richard Kwan, Chayton Ritter
@date 14-Mar-2023

@section soft_org Software Organization
@par
The following files are included in this software:\n\n
main.py: The main turret duel program\n
mlx_cam.py: A driver for the MLX90640 camera\n
mlx90640: A folder containing dependencies required to run the MLX90640 camera driver\n
motor_driver.py: A library containing a class for a motor driver\n
servo_driver.py: A library containing a class for a servo driver\n
encoder_reader.py: A library containing a class for an encoder reader\n
closedloopcontrol.py: A library containing a class for a proportional system controller



@section tasks Tasks
@par
The turret code can be summarized as a list of tasks:

@par
1. Adjusting the blaster horizontally\n
2. Adjusting the blaster vertically\n
3. Shooting a dart\n
4. Detecting a target (aiming)

@par
Although the intent of this project was to have these tasks run pseudo-simultaneously using a task-sharing algorithm, this was ommitted due to the almost mutually
exclusive nature of these tasks, which can be attributed to the following:

@par
- The original design having the camera mounted directly on the blaster. Due to refresh rate constraints, an image could not be taken until the blaster was stationary. 
The change to a camera mounted separate from the turret was done at the last minute, so the code was not changed to reflect the new ability to take an image while moving.\n
- The blaster not being able to move until the aiming point was calculated. Calculating the aiming point was a computationally expensive task, taking at least half a 
second to complete. There was no benefit to making this task a generator, as the motors would remain stationary until the new setpoints were calculated. If the code was 
updated to reflect the new ability to take an image while the turret was moving, then this calculation could still occur during a movement phase.\n

@par
As a result, the only tasks that can be considered "shared" at any given point are the vertical and horizontal adjustments.\n\n
The task diagram is shown below.

@image html 405_td.png



@section state_dia State Structure
@par
The main duel program is organized into six distinct states:

@par
S0_INIT: The turret initializes all necessary internal variables.\n
S1_TURN180: The turret turns 180 degrees. It stays in this state until 5 seconds have passed. This state consists of both move tasks.\n
S2_AIM: The turret takes a picture using the infrared camera, processes the image, and calculates the necessary movement to aim at the target. This state consists exclusively of the target detection task.\n
S3_ADJUST: The turret moves according to the calculations in the AIM state. The turret stays in this state for 500 milliseconds. This state consists of both move tasks.\n
S4_SHOOT: The turret spins up the flywheels, then actuates a servo to push a loaded dart into the flywheels. This state consists exclusively of the shoot task.\n
S5_SAFE: The turret powers down. All motors are disabled and the trigger mechanism is returned to the original position.

@par
The state diagram is shown below.

@image html 405_sd.png

'''