import RPi.GPIO as GPIO
import time
from time import sleep

# Initialize GPIO 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

channel = 26 #GPIO Number
frequency = 1 # Frequency sent to the motor that can be changed

# Setup GPIO
GPIO.setup(channel, GPIO.OUT)
GPIO.output(channel, GPIO.HIGH)
pwm=GPIO.PWM(channel, frequency) # Setup GPIO pin for PWM output

try:
    while True: # Loop to continuously run motor
        pwm.start(50) # Start PWM output and set duty Cycle

except KeyboardInterrupt:
    GPIO.cleanup() # Clean up GPIO
    pwm.stop() # Stop PWM