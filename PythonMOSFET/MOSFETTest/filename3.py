import RPi.GPIO as GPIO
import time

# GPIO pin setup
CLK = 18
DT = 23
SW = 24

# Initialize variables
counter = 0
clkLastState = 0
rotation_start_time = 0
last_rotation_time = 0
speed = 0

# Setup GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(DT,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW,GPIO.IN,pull_up_down=GPIO.PUD_UP)

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
        if GPIO.input(SW) == GPIO.LOW:
            print("Press")
            time.sleep(0.2)

        elif (clkState == GPIO.LOW and clkLastState == GPIO.HIGH):
            calculate_speed()
            if dtState == GPIO.HIGH:
                print("CW")
                counter += 1
            else:
                print("CCW")
                counter -= 1
            print(f"Speed: {speed:.2f} turns/second")
            print(counter)
            
        clkLastState = clkState
        time.sleep(0.01)  # Small delay for debouncing

except KeyboardInterrupts:
    GPIO.cleanup()