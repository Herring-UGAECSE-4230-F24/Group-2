# Import necessary libraries
import RPi.GPIO as GPIO
import time

# Define GPIO pins for rotary encoder
clk = 18  # Clock pin
dt = 23   # Data pin
sw = 24   # Switch pin

# Configure GPIO settings
GPIO.setwarnings(False)  # Disable GPIO warnings
GPIO.setmode(GPIO.BCM)   # Use Broadcom pin-numbering scheme
# Set up pins as inputs with pull-up resistors
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize variables
counter = 0          # Counter for rotation (accounts for direction)
turns = 0            # Counter for turns (does not account for direction)
lastClkState = GPIO.input(clk)  # Last state of the clock pin
speed = 0            # Rotation speed
rot_start_time = 0   # Start time for rotation measurement
last_time = 0        # Last time a state change was detected
debounce = 0.002     # Debounce time in seconds
last_edge = 0        # Time of the last edge detection

try:
    while True:
        current_time = time.time()  # Get current time
        clkState = GPIO.input(clk)  # Read current clock state

        # Check if enough time has passed since the last edge (debounce)
        if (current_time - last_edge) >= debounce:

            # Check if switch is pressed
            if GPIO.input(sw) == GPIO.LOW:
                print("Press")
            
            # Check for a falling edge on clock pin
            elif(clkState == GPIO.LOW and lastClkState == GPIO.HIGH):
                turns += 1  # Increment turn counter which doesn't take into account direction
                
                # Calculate rotation speed
                if rot_start_time == 0: # Check if the encoder has rotated yet
                    rot_start_time = current_time # Set the first rotation time as current time defined above
                else:
                    time_diff = current_time - rot_start_time # Get the change in time from the current rotation
                    if time_diff > 0:
                        speed = turns / time_diff  # Calculate turns per second

                # Determine rotation direction
                if GPIO.input(dt) == GPIO.LOW:
                    counter -= 1 # Decrement counter 
                    print("CCW")  # Counter-clockwise
                else:
                    counter += 1 # Increment counter
                    print("CW")   # Clockwise
                
                # Print current count and speed
                print(counter)
                print(f"Speed: {speed:.2f} turns/sec")
                    
        # Update last clock state
        lastClkState = clkState

except KeyboardInterrupt:
    # Clean up GPIO on keyboard interrupt
    GPIO.cleanup()
