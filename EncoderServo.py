# This program demonstrates usage of the servos.
# Keep the robot in a safe location before running this program,
# as it will immediately begin moving.
# See https://learn.adafruit.com/adafruit-16-channel-pwm-servo-hat-for-raspberry-pi/ for more details.

import time
import Adafruit_PCA9685
import RPi.GPIO as GPIO
import signal
import math

rCount = 0   #current count for each wheel
lCount = 0   
prc = 0      #previous count
plc = 0

startTime = time.time()    #current timer

# This function is called when Ctrl+C is pressed.
# It's intended for properly exiting the program.
def ctrlC(signum, frame):
    print("Exiting")
    GPIO.cleanup()
    exit()

# Attach the Ctrl+C signal interrupt
signal.signal(signal.SIGINT, ctrlC)
    
# Set the pin numbering scheme to the numbering shown on the robot itself.
GPIO.setmode(GPIO.BCM)

# Prevent the program from exiting by adding a looping delay.
#while True:
    #time.sleep(1)
	
# The servo hat uses its own numbering scheme within the Adafruit library.
# 0 represents the first servo, 1 for the second, and so on.
LSERVO = 0
RSERVO = 1

# This function is called when Ctrl+C is pressed.
# It's intended for properly exiting the program.
def ctrlC(signum, frame):
    print("Exiting")
    
    # Stop the servos
    pwm.set_pwm(LSERVO, 0, 0);
    pwm.set_pwm(RSERVO, 0, 0);
    
    exit()

# Attach the Ctrl+C signal interrupt
signal.signal(signal.SIGINT, ctrlC)
    
# Initialize the servo hat library.
pwm = Adafruit_PCA9685.PCA9685()

# 50Hz is used for the frequency of the servos.
pwm.set_pwm_freq(50)

################ Encoder Functions #################

# Pins that the encoders are connected to
LENCODER = 17
RENCODER = 18

# This function is called when the left encoder detects a rising edge signal.
def onLeftEncode(pin):
    global lCount
    lCount = lCount + 1
    print(lCount)

# This function is called when the right encoder detects a rising edge signal.
def onRightEncode(pin):
    global rCount
    rCount = rCount + 1
    print(rCount)

# Resets tick counts to zero, store ticks before resetting
def resetCounts():
    global rCount
    global prc
    global lCount
    global plc
    global startTime
    prc = rCount
    plc = lCount
    rCount = 0
    lCount = 0
    
    #Reset time
    startTime = time.time()

# Returns the left and right tick counts since the last reset/start
# returns a tuple of left and right wheel speeds
def getCounts():
    global prc
    global plc
    return (plc, prc)

# Returns the instantaneous left and right wheel speeds as a tuple
# as revolutions per second;
def getSpeeds():
    global startTime
    currTime = time.time()
    global lcount
    global rcount
    if (lCount > 0):
        lSpeed = (currTime - startTime) / (lCount / 32)
    else:
        lSpeed = 0
    if (rCount > 0):
        rSpeed = (currTime - startTime) / (rCount / 32)
    else:
        rSpeed = 0
    return (lSpeed, rSpeed)

# Code necessary to initialize the encoders
def initEncoders():
    # Set encoder pins as input
    # Also enable pull-up resistors on the encoder pins
    # This ensures a clean 0V and 3.3V is always outputted from the encoders.
    GPIO.setup(LENCODER, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(RENCODER, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Attach a rising edge interrupt to the encoder pins
    GPIO.add_event_detect(LENCODER, GPIO.RISING, onLeftEncode)
    GPIO.add_event_detect(RENCODER, GPIO.RISING, onRightEncode)
    

################ Servo Functions ###################

# Write an initial value of 1.5, which keeps the servos stopped.
# Due to how servos work, and the design of the Adafruit library, 
# the value must be divided by 20 and multiplied by 4096.
pwm.set_pwm(LSERVO, 0, math.floor(1.5 / 20 * 4096));
pwm.set_pwm(RSERVO, 0, math.floor(1.5 / 20 * 4096));

startTime = time.time()

while True:
    # Write a maximum value of 1.7 for each servo.
    # Since the servos are oriented in opposite directions,
    # the robot will end up spinning in one direction.
    # Values between 1.3 and 1.7 should be used.
    
    onLeftEncode(LENCODER)
    onRightEncode(RENCODER)
    pwm.set_pwm(LSERVO, 0, math.floor(1.6 / 20 * 4096));
    pwm.set_pwm(RSERVO, 0, math.floor(1.6 / 20 * 4096));
    time.sleep(4)
    print ("Speed: ", getSpeeds())
    pwm.set_pwm(LSERVO, 0, math.floor(1.5 / 20 * 4096));
    pwm.set_pwm(RSERVO, 0, math.floor(1.5 / 20 * 4096));

    print("Current Counts: ", lCount, " ", rCount)
    resetCounts()
    print("Previous counts: ", getCounts())
    print("Current Counts: ", lCount, " ", rCount)
    print ("Speed: ", getSpeeds())
    
    # Write a minimum value of 1.4 for each servo.
    # The robot will end up spinning in the other direction.
    pwm.set_pwm(LSERVO, 0, math.floor(1.4 / 20 * 4096));
    pwm.set_pwm(RSERVO, 0, math.floor(1.4 / 20 * 4096));
    time.sleep(4)
    
    print ("Speed: ", getSpeeds())
    time.sleep(10)
    print("Current Counts: ", lCount, " ", rCount)
    resetCounts()
    prev = getCounts()
    print("Current Counts: ", lCount, " ", rCount)
    print("Previous counts: ", prev)
    
    time.sleep(10)