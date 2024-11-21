# Import necessary libraries
import RPi.GPIO as GPIO
import pigpio
import time
import random

# Define GPIO pins for rotary encoder
clk = 18  # Clock pin
dt = 23   # Data pin
sw = 24   # Switch pin
ir = 12   # IR sensor pin
channel = 13 #Opto pin

# Configure GPIO settings
GPIO.setwarnings(False)  # Disable GPIO warnings
GPIO.setmode(GPIO.BCM)   # Use Broadcom pin-numbering scheme
# Set up pins as inputs with pull-up resistors
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ir, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
GPIO.setup(channel, GPIO.OUT) 
GPIO.output(channel, GPIO.HIGH)
"""
RPM = 25 # RPM of motor
frequency =  1 #RPM *3 /60
on = True # Motor on or off
rotary_encoder_pos = 1
motor_pwm = GPIO.PWM(channel, frequency)
doodoo_cycle = 100
motor_pwm.start(doodoo_cycle)
measured_rpm = 0
debounce = 0.002 
blade_counter = 0
blade_counter_window = time.time()
last_edge = 0
lastClkState = GPIO.input(clk)
print_rpm_time = time.time()
same_blade = False"""

try:
    while True:
        pass
except KeyboardInterrupt:
    GPIO.cleanup()