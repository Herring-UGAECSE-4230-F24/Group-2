# Import necessary libraries for GPIO control and timing
import RPi.GPIO as GPIO
import time
import random

# Define GPIO pins for rotary encoder and other components
clk = 18  # Clock pin for rotary encoder
dt = 23   # Data pin for rotary encoder
sw = 24   # Switch pin for rotary encoder
ir = 12   # IR sensor pin
channel = 13 # Opto pin for motor control

# Configure GPIO settings
GPIO.setwarnings(False)  # Disable GPIO warnings
GPIO.setmode(GPIO.BCM)   # Use Broadcom pin-numbering scheme

# Set up pins as inputs with pull-up resistors, except channel which is output
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ir, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
GPIO.setup(channel, GPIO.OUT) 
GPIO.output(channel, GPIO.HIGH)  # Set initial output state to HIGH

# Initialize variables for measuring RPM and debouncing inputs
RPM = 25 # RPM of motor
frequency =  1 # RPM *3 /60
on = True # Motor on or off
rotary_encoder_pos = 1
motor_pwm = GPIO.PWM(channel, frequency)
doodoo_cycle = 0.5
motor_pwm.start(doodoo_cycle)
measured_rpm = 0
debounce = 0.002  # Debounce time in seconds to avoid false triggering
blade_counter = 0  # Counter for blades passing the IR sensor
blade_counter_window = time.time()  # Time window for counting blades
last_edge = 0  # Last time an edge was detected on the rotary encoder
lastClkState = GPIO.input(clk)  # Initial state of the clock pin
print_rpm_time = time.time()  # Time of last RPM printout
same_blade = False  # Flag to track if the same blade is detected

try:
    while True:
        current_time = time.time()  # Get current time

        clkState = GPIO.input(clk)  # Read current state of clock pin

        if (current_time - last_edge) >= debounce:  # Check debounce condition
            
            if GPIO.input(sw) == GPIO.LOW:  # Check if switch is pressed
                print("press")
                on = not on  # Toggle motor state
                
                if on:
                    motor_pwm.ChangeDutyCycle(doodoo_cycle)  # Resume motor operation
                else:
                    motor_pwm.ChangeDutyCycle(0)  # Stop motor operation
                
                time.sleep(0.2)  # Debounce delay for switch press

            elif (clkState == GPIO.LOW and lastClkState == GPIO.HIGH):  # Detect falling edge on clock pin
                
                if GPIO.input(dt) == GPIO.LOW:  
                    if rotary_encoder_pos >= 2:
                        rotary_encoder_pos -= 1  # Decrement position counter if counter-clockwise
                else:
                    rotary_encoder_pos += 1  # Increment position counter if clockwise
                
                RPM = 25 * rotary_encoder_pos  # Update RPM based on encoder position
                
                if RPM / 25 < 100:
                    doodoo_cycle = 0.5 * RPM / 25 # Set duty cycle based on desired RPM
                
                motor_pwm.ChangeDutyCycle(doodoo_cycle) # Change duty cycle 
                last_edge = current_time  # Keep track of edge time
                rotary_encoder_pos += 1 # Increment counter
                print("Duty Cycle")
                print(doodoo_cycle)
        
        if GPIO.input(ir) == GPIO.LOW:  # Read from IR sensor
            if same_blade: # Don't do anything if still reading high (still on the same blade)
                pass  
            else:
                same_blade = True  
                if current_time - blade_counter_window >= 2:  # Every two seconds calculate and print RPM
                    print(blade_counter)
                    print("Desired rpm = " + str(RPM))
                    measured_rpm = (blade_counter *200)/ (current_time - blade_counter_window) # Formula to calculate RPM
                    print("Measured rpm = " + str(measured_rpm))
                    print_rpm_time = current_time  
                    blade_counter = 0  # Reset the counter for number of blades
                    blade_counter_window = current_time  
                else: # Increment counter for number of blades
                    blade_counter += 1  
        else:
            same_blade = False  

        lastClkState = clkState  # Save the clk state
        time.sleep(0.035)  

except KeyboardInterrupt: # Cleanup GPIOs
    GPIO.cleanup()  
