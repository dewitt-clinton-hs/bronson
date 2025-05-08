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

# Brain should be defined by default
brain = Brain()

conveyor = Motor(Ports.PORT10) # Conveyor (motor at port 10)

# Left and right wheels (ports 11 and 20)
wheelR = Motor(Ports.PORT11)
wheelL = Motor(Ports.PORT20)

wheels = [wheelR, wheelL] # Array holding the wheels (in case we want to run for loops)

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

L1 = controller.buttonL1 # The L1 button on the controller
R1 = controller.buttonR1 # The L2 button on the controller

# When L1 is pressed invoke spin(), when it's released invoke stop_spin()
L1.pressed(spin_forward)
R1.pressed(spin_backward)

top_1 = [L1, R1] # An array containing the top buttons of 1

# For each left button, where an individual button is represented as i
for i in top_1:
    i.released(stop_spin) # When the button is released, invoke stop_spin()

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

# Function for printing the axis of the joysticks
def printAxis():

    # Print rightStickX
    brain.screen.print("Right stick X: ")
    brain.screen.print(rightStickX.position())
    brain.screen.new_line()

    # Print rightStickY
    brain.screen.print("Right stick Y: ")
    brain.screen.print(rightStickY.position())
    brain.screen.new_line()

    # Print leftStickX
    brain.screen.print("Left stick X: ")
    brain.screen.print(leftStickX.position())
    brain.screen.new_line()

    # Print leftStickY
    brain.screen.print("Left stick Y: ")
    brain.screen.print(leftStickY.position())
    brain.screen.new_line()

brain.screen.pressed(printAxis) # When the brain's screen is pressed, invoke printAxis()

# Run forever
while True:
    update_position() # Constantly update the position

    # If the position of the left stick is up
    if left_position_y > 0:

        # If the right stick is turned to the right
        if (right_position_x > 0):
            wheelR.spin(FORWARD, 85) # Spin the right wheel in reverse (our forwards)

        # If the right stick is turned to the left
        elif (right_position_x < 0):
            wheelL.spin(REVERSE, 85) # Spin the wheel forwards (our reverse)
        else:
            wheelL.spin(FORWARD, 100) # Spin the left wheel forward at a velocity of 50
            wheelR.spin(REVERSE, 100) # Spin the right wheel forward at a velocity of 50

    # If the position of the left stick is down
    elif left_position_y < 0:

        # If the right stick is turned to the right
        if (right_position_x > 0):
            wheelR.spin(FORWARD, 85) # Spin the right wheel in reverse (our forwards)

        # If the right stick is turned to the left
        elif (right_position_x < 0):
            wheelL.spin(REVERSE, 85) # Spin the wheel forwards (our reverse)
        else:
            wheelL.spin(REVERSE, 100) # Spin the left wheel back at a velocity of 50
            wheelR.spin(FORWARD, 100) # Spin the right wheel back at a velocity of 50

    # If the position of the left stick is right
    elif right_position_x > 0:

        # When the wheels alternate the robot turns, so this makes it turn
        wheelL.spin(FORWARD, 50) # Spin the left wheel forward at a velocity of 50
        wheelR.spin(FORWARD, 50) # Spin the right wheel backward at a velocity of 50

    # If the position of the right stick is left
    elif right_position_x < 0:

        # When the wheels alternate the robot turns, so this makes it turn
        wheelL.spin(REVERSE, 50) # Spin the left wheel forward at a velocity of 50
        wheelR.spin(REVERSE, 50) # Spin the right wheel backward at a velocity of 50

    # When the position of the right stick is 0
    else:
        wheelL.stop() # Stop the left wheel
        wheelR.stop() # Stop the right wheel
