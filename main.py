# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       student                                                      #
# 	Created:      5/6/2025, 3:49:42 PM                                         #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *
import math

# Brain should be defined by default
brain = Brain()

conveyor = Motor(Ports.PORT10) # Conveyor (motor at port 10)

# Left and right wheels (ports 11 and 20)
wheelR = Motor(Ports.PORT11)
wheelL = Motor(Ports.PORT20)

# Function to spin the conveyor forward and carry the wheel
def spin_forward():
    conveyor.spin(FORWARD, 100) # Spin the conveyor forward at a velocity of 100

# Function to spin the conveyor reverse and drop the wheel
def spin_backward():
    conveyor.spin(REVERSE, 100) # Spin the conveyor in reverse at a velocity of 100

# Function to stop spinning the conveyor
def stop_spin():
    conveyor.stop() # Stop the conveyor

controller = Controller() # Initialize the controller for use

# CONTROLLER JOYSTICKS
leftStickX = controller.axis4 # Left joystick left-right
leftStickY = controller.axis3 # Right joystick up-down
rightStickX = controller.axis1 # Right joystick left-right
rightStickY = controller.axis2 # Right joystick up-down

buttons = [leftStickX, leftStickY, rightStickX, rightStickY] # Array of the joysticks (in case we want to run for loops)

left_position_y = 0 # Variable for storing the up-down position of the left joystick
left_position_x = 0 # Variable for storing the left-right position of the left joystick

right_position_y = 0 # Variable for storing the up-down position of the right joystick
right_position_x = 0 # Variable for storing the left-right position of the right joystick


# Function to update the position variable
def update_position():

    # Define which variables are globally scoped so we can update them 
    global left_position_y
    global left_position_x
    global right_position_y
    global right_position_x

    # Update all of the variables to be the position of the joystick
    left_position_y = leftStickY.position()
    left_position_x = leftStickX.position()
    right_position_y = rightStickY.position()
    right_position_x = rightStickX.position()

# Function to check for turns based on direction
def check_turns(direction):
        
        # If the direction is forward
        if direction == FORWARD:
                
            # If the right stick is turned to the right
            if (right_position_x > 0):

                # The left wheel slightly pushes against the right wheel so the turns aren't as erratic
                wheelR.spin(FORWARD, 50) # Spin the left wheel forward at a velocity of 25 
                wheelL.spin(FORWARD, 75) # Spin the right wheel in reverse (our forwards)
                    
            # If the right stick is turned to the left
            elif (right_position_x < 0):

                # The right wheel slightly pushes against the left wheel so the turns aren't as erratic
                wheelR.spin(REVERSE, 50) # Spin the right wheel forward (our reverse) at a velocity of 25
                wheelL.spin(REVERSE, 75) # Spin the left wheel forward at a velocity of 75
            else:

                # Both wheels spin in the same direction
                wheelL.spin(FORWARD, math.sin(math.pi/200 * left_position_y) * 100) # Spin the left wheel forward at a velocity of 100
                wheelR.spin(REVERSE, math.sin(math.pi/200 * left_position_y) * 100) # Spin the right wheel reverse (our forwards) at a velocity of 100

        # If else (direction is REVERSE)
        else:

            # If the right stick is turned to the right
            if (right_position_x > 0):

                # The left wheel slightly pushes against the right wheel so the turns aren't as erratic
                wheelR.spin(REVERSE, 75) # Spin the right wheel in reverse (our forwards)
                wheelL.spin(REVERSE, 50) # Spin the left wheel forwards

            # If the right stick is turned to the left
            elif (right_position_x < 0):

                # The right wheel slightly pushes against the left wheel so the turns aren't as erratic
                wheelL.spin(FORWARD, 75) # Spin the left wheel forwards
                wheelR.spin(FORWARD, 50)  # Spin the right wheel forwards (our reverse)

            # If else (right stick is 0)
            else:
                wheelL.spin(REVERSE, (math.sin(math.pi/200 * left_position_y) * 100) * -1) # Spin the left wheel in reverse at a velocity of 100
                wheelR.spin(FORWARD, (math.sin(math.pi/200 * left_position_y) * 100) * -1) # Spin the right wheel forwards (our reverse) at a velocity of 100
    

# The L1 and R1 buttons on the controller
L1 = controller.buttonL1
R1 = controller.buttonR1

def check_conveyor():

    # If L1 is being pressed
    if L1.pressing():
        spin_backward() # Spin the conveyor backwards

    # If R1 is being pressed
    elif R1.pressing():
        spin_forward() # Spin the conveyor forwards

    # If else (none or both)
    else:
        stop_spin() # Stop spinning the conveyor

# Run forever
while True:
    update_position() # Constantly update the position

    # If the position of the left stick is up
    if left_position_y > 0:
        check_turns(FORWARD) # Check turns when the robot is driving forward
        check_conveyor() # Check if the conveyor is spinning

    # If the position of the left stick is down
    elif left_position_y < 0:
        check_turns(REVERSE)  # Check turns when the robot is driving in reverse
        check_conveyor() # Check if the conveyor is spinning

    # If the position of the left stick is right
    elif right_position_x > 0:

        # When the wheels alternate the robot turns, so this makes it turn
        wheelL.spin(FORWARD, 50) # Spin the left wheel forward at a velocity of 50
        wheelR.spin(FORWARD, 50) # Spin the right wheel backward at a velocity of 50
        check_conveyor() # Check if the conveyor is spinning

    # If the position of the right stick is left
    elif right_position_x < 0:

        # When the wheels alternate the robot turns, so this makes it turn
        wheelL.spin(REVERSE, 50) # Spin the left wheel forward at a velocity of 50
        wheelR.spin(REVERSE, 50) # Spin the right wheel backward at a velocity of 50
        check_conveyor() # Check if the conveyor is spinning

    # When the position of the right stick is 0
    else:
        wheelL.stop() # Stop the left wheel
        wheelR.stop() # Stop the right wheel 
        check_conveyor() # Check if the conveyor is spinning
