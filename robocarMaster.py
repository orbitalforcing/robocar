# Robocar master control program
# v0.1 - keyboard steering logic for PWM motor control


import RPi.GPIO as GPIO # Import the GPIO Library
import time # Import the Time library
import sys, tty, termios, time

# Set the GPIO modes
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set variables for the GPIO motor pins
pinMotorAForwards = 10
pinMotorABackwards = 9
pinMotorBForwards = 8
pinMotorBBackwards = 7

# how many times to turn pin off each second
Frequency = 20
# how long pin stays on each cycle as a %
DutyCycleA = 30
DutyCycleB = 30
# setting duty cycle to 0 will stop motors
Stop = 0

# Set the GPIO Pin mode to be Output
GPIO.setup(pinMotorAForwards, GPIO.OUT)
GPIO.setup(pinMotorABackwards, GPIO.OUT)
GPIO.setup(pinMotorBForwards, GPIO.OUT)
GPIO.setup(pinMotorBBackwards, GPIO.OUT)

# The getch method can determine which key has been pressed
# by the user on the keyboard by accessing the system files
# It will then return the pressed key as a variable
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


# set the GPIO to software PWM at at frequency Hz
pwmMotorAForwards = GPIO.PWM(pinMotorAForwards, Frequency)
pwmMotorABackwards = GPIO.PWM(pinMotorABackwards, Frequency)
pwmMotorBForwards = GPIO.PWM(pinMotorBForwards, Frequency)
pwmMotorBBackwards = GPIO.PWM(pinMotorBBackwards, Frequency)

# start software PWM with duty cycle of 0 (not moving)
pwmMotorAForwards.start(Stop)
pwmMotorABackwards.start(Stop)
pwmMotorBForwards.start(Stop)
pwmMotorBBackwards.start(Stop)

# Turn all motors off
def StopMotors():
    pwmMotorAForwards.ChangeDutyCycle(Stop)
    pwmMotorABackwards.ChangeDutyCycle(Stop)
    pwmMotorBForwards.ChangeDutyCycle(Stop)
    pwmMotorBBackwards.ChangeDutyCycle(Stop)

# Turn both motors forwards
def Forwards():
    pwmMotorAForwards.ChangeDutyCycle(DutyCycleA)
    pwmMotorABackwards.ChangeDutyCycle(Stop)
    pwmMotorBForwards.ChangeDutyCycle(DutyCycleB)
    pwmMotorBBackwards.ChangeDutyCycle(Stop)

# Turn both motors backwards
def Backwards():
    pwmMotorAForwards.ChangeDutyCycle(Stop)
    pwmMotorABackwards.ChangeDutyCycle(DutyCycleA)
    pwmMotorBForwards.ChangeDutyCycle(Stop)
    pwmMotorBBackwards.ChangeDutyCycle(DutyCycleB)

# turn left
def Left():
    pwmMotorAForwards.ChangeDutyCycle(Stop)
    pwmMotorABackwards.ChangeDutyCycle(DutyCycleA)
    pwmMotorBForwards.ChangeDutyCycle(DutyCycleB)
    pwmMotorBBackwards.ChangeDutyCycle(Stop)

# turn right
def Right():
    pwmMotorAForwards.ChangeDutyCycle(DutyCycleA)
    pwmMotorABackwards.ChangeDutyCycle(Stop)
    pwmMotorBForwards.ChangeDutyCycle(Stop)
    pwmMotorBBackwards.ChangeDutyCycle(DutyCycleB)


# This method will toggle the direction of the steering
# motor. The method will determine whether the user wants
# to turn left or right depending on the key they press and
# then make the appropriate adjustment. It works as a toggle
# because the program cannot read multiple pressed keys at
# the same time. The possible positions of the wheels are
# "right", "centre" and "left". It will then update the
# status of the wheel to access next time it is called.

def toggleSteering(direction):

    global wheelStatus

    if(direction == "right"):
        if(wheelStatus == "centre"):
            wheelStatus = "right"
            Right()
        elif(wheelStatus == "left"):
            wheelStatus = "centre"
            Forwards()

    if(direction == "left"):
        if(wheelStatus == "centre"):
            wheelStatus = "left"
            Left()
        elif(wheelStatus == "right"):
            wheelStatus = "centre"
            Forwards()

# Global variables for the status of the steering
wheelStatus = "centre"

# Instructions for when the user has an interface
print("w/s: acceleration")
print("a/d: steering")
print("x: exit")

# Infinite loop that will not end until the user presses the
# exit key
while True:
    # Keyboard character retrieval method is called and saved
    # into variable
    char = getch()

    # The car will drive forward when the "w" key is pressed
    if(char == "w"):
        Forwards()
        
    # The car will reverse when the "s" key is pressed
    if(char == "s"):
        Backwards()
        
    # The "a" key will toggle the steering left
    if(char == "a"):
        toggleSteering("left")

    # The "d" key will toggle the steering right
    if(char == "d"):
        toggleSteering("right")

    # The "x" key will break the loop and exit the program
    if(char == "x"):
        print("Program Ended")
        break

    # The keyboard character variable will be set to blank, ready
    # to save the next key that is pressed
    char = ""

#Forwards()
#time.sleep(5)

#Left()
#time.sleep(5)

#Forwards()
#time.sleep(1)

#Right()
#time.sleep(5)

# Backwards()
# time.sleep(5)


StopMotors()

GPIO.cleanup()
