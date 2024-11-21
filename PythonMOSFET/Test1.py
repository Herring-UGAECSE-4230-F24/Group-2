"""import RPi.GPIO as GPIO
import time
from time import sleep

# Initialize GPIO 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

channel = 13 #GPIO Number
frequency = 1# Frequency sent to the motor that can be changed

# Setup GPIO
GPIO.setup(channel, GPIO.OUT)
GPIO.output(channel, GPIO.HIGH)
pwm=GPIO.PWM(channel, frequency) # Setup GPIO pin for PWM output

try:
    while True: # Loop to continuously run motor
        pwm.start(40) # Start PWM output and set duty Cycle

except KeyboardInterrupt:
    GPIO.cleanup() # Clean up GPIO
    pwm.stop() # Stop PWM"""


import pigpio

pi = pigpio.pi()
clk = 18  # Clock pin
dt = 23   # Data pin
sw = 24   # Switch pin
ir = 12   # IR sensor pin
channel = 13 # Opto pin

clkpi = pi.set_mode(clk, pigpio.INPUT)
dtpi = pi.set_mode(dt, pigpio.INPUT)
swpi = pi.set_mode(sw, pigpio.INPUT)
irpi = pi.set_mode(ir, pigpio.INPUT)
channelpi = pi.set_mode(channel, pigpio.OUTPUT)



