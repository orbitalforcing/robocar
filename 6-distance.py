# CamJam EduKit 3 - Robotics
# Worksheet 6 measuring distance

import RPi.GPIO as GPIO # Import the GPIO Library
import time # Import the Time library

# Set the GPIO modes
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set variables for the GPIO pins
pinTrigger = 17
pinEcho = 18

print("Ultrasonic measurement")

# Set pins as input and output
GPIO.setup(pinTrigger, GPIO.OUT)
GPIO.setup(pinEcho, GPIO.IN)

try:
    # repeat forever
    while True:
        # set trigger to false (low)
        GPIO.output(pinTrigger, False)

        # allow module to settle
        time.sleep(0.5)

        # send 10us pulse to trigger
        GPIO.output(pinTrigger, True)
        time.sleep(0.00001)
        GPIO.output(pinTrigger, False)

        # start the timer
        StartTime = time.time()

        # the start time is reset until echo pin is high (==1)
        while GPIO.input(pinEcho)==0:
            StartTime = time.time()

        # stop timer when echo pin no longer high
        while GPIO.input(pinEcho)==1:
            StopTime = time.time()
            # detect if sensor too close to object
            if StopTime - StartTime >= 0.04:
                print("Stop! Too close to see.")
                StopTime = StartTime
                break

        # calculate pulse length
        ElapsedTime = StopTime - StartTime

        # pulse travel round trip distance is time x speed of sound (cm/s)
        Distance = ElapsedTime * 34326

        # distance to object is half that
        Distance = Distance / 2

        print("Distance: %.1f cm" % Distance)

        time.sleep(0.5)

# if ctrl-C pressed then cleanup and stop
except KeyboardInterrupt:
    GPIO.cleanup()
