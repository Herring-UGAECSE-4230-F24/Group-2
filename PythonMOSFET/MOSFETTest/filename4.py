import RPi.GPIO as GPIO
import time

# GPIO pin setup
CLK = 18
DT = 23
SW = 24

# Initialize variables
counter = 0
clkLastState = 0
dtLastState = 0
rotation_start_time = 0
last_rotation_time = 0
speed = 0
last_edge_time = 0
debounce_time = 0.001  # 1ms debounce time

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def calculate_speed():
    global rotation_start_time, last_rotation_time, speed
    current_time = time.time()
    if rotation_start_time == 0:
        rotation_start_time = current_time
    else:
        time_diff = current_time - last_rotation_time
        if time_diff > 0:
            speed = (1 / time_diff) / 140  # turns per second
    last_rotation_time = current_time

def encoder_callback(channel):
    global counter, clkLastState, dtLastState, last_edge_time
    
    current_time = time.time()
    #if (current_time - last_edge_time) < debounce_time:
        return
    
    last_edge_time = current_time
    
    clkState = GPIO.input(CLK)
    dtState = GPIO.input(DT)

    if GPIO.input(SW) == GPIO.LOW:
            print("Press")
            
            time.sleep(0.2)

    elif(clkState == GPIO.LOW and clkLastState == GPIO.HIGH):
        calculate_speed()
        if dtState != clkState:
            counter += 1
            print("CW")
        else:
            counter -= 1
            print("CCW")
        print(counter)
        print(f"Speed: {speed:.2f} turns/second")
    
    clkLastState = clkState
    dtLastState = dtState

try:
    GPIO.add_event_detect(CLK, GPIO.BOTH, callback=encoder_callback)
    GPIO.add_event_detect(DT, GPIO.BOTH, callback=encoder_callback)
    
    while True:
        time.sleep(0.1)  # Main loop can sleep longer, as we're using interrupts

finally:
    GPIO.cleanup()