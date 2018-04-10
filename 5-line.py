# CamJam EduKit 3 - Robotics
# Worksheet 5 – Line detection

import RPi.GPIO as GPIO # Import the GPIO Library
import time # Import the Time library

# Set the GPIO modes
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set variables for the GPIO pins
pinLineFollower = 25

# Set pin 25 as input so it can be read
GPIO.setup(pinLineFollower, GPIO.IN)

try:
    # repeat forever
    while True:
        # if sensor low (=0), it's above black
        if GPIO.input(pinLineFollower)==0:
            print('Sensor is seeing a black surface')
        else:
            print('Sensor is seeing a white surface')
        time.sleep(0.2)

# if ctrl-C pressed then cleanup and stop
except KeyboardInterrupt:
    GPIO.cleanup()
