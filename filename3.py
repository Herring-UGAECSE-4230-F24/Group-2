import RPi.GPIO as GPIO
import time

# GPIO pin setup
CLK = 17
DT = 18
SW = 27

# Initialize variables
counter = 0
clkLastState = 0
rotation_start_time = 0
last_rotation_time = 0
speed = 0

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def calculate_speed():
    global rotation_start_time, last_rotation_time, speed
    current_time = time.time()
    if rotation_start_time == 0:
        rotation_start_time = current_time
    else:
        time_diff = current_time - last_rotation_time
        if time_diff > 0:
            speed = 1 / time_diff  # turns per second
    last_rotation_time = current_time

try:
    while True:
        clkState = GPIO.input(CLK)
        dtState = GPIO.input(DT)
        
        if clkState != clkLastState:
            calculate_speed()
            if dtState != clkState:
                counter += 1
            else:
                counter -= 1
            print(f"Counter: {counter}, Speed: {speed:.2f} turns/second")
        
        clkLastState = clkState
        time.sleep(0.01)  # Small delay to reduce CPU usage

finally:
    GPIO.cleanup()