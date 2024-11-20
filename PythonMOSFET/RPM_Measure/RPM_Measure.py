# Import necessary libraries
import RPi.GPIO as GPIO
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

RPM = 25 # RPM of motor
frequency =  1 #RPM *3 /60
on = True # Motor on or off
rotary_encoder_pos = 1
motor_pwm = GPIO.PWM(channel, frequency)
doodoo_cycle = 1
motor_pwm.start(doodoo_cycle)
measured_rpm = 0
debounce = 0.002 
blade_counter = 0
blade_counter_window = time.time()
last_edge = 0
lastClkState = GPIO.input(clk)
print_rpm_time = time.time()
same_blade = False
try:
    while True:
        current_time = time.time()  # Get current
        # Check if enough time has passed since the last edge (debounce)
        clkState = GPIO.input(clk)

        if (current_time - last_edge) >= debounce:
            
            if GPIO.input(sw) == GPIO.LOW:
                print("press")
                on = not on
                if on:
                    motor_pwm.ChangeDutyCycle(doodoo_cycle)
                else:
                    motor_pwm.ChangeDutyCycle(0)
                time.sleep(0.2)

            elif (clkState == GPIO.LOW and lastClkState == GPIO.HIGH):

                # Determine rotation direction
                if GPIO.input(dt) == GPIO.LOW:
                    if rotary_encoder_pos >= 2:
                        rotary_encoder_pos -= 1 # Decrement counter
                else:
                    rotary_encoder_pos += 1 # Increment counter
                RPM = 25 * rotary_encoder_pos
                #frequency = RPM * 3/60
                if 1 * RPM/25  < 100:
                    doodoo_cycle = 1 * RPM/25 
                    #doodoo_cycle += 1
                #motor_pwm.ChangeFrequency(frequency)
                motor_pwm.ChangeDutyCycle(doodoo_cycle)
                last_edge = current_time
                print("Duty Cycle")
                print(doodoo_cycle)
        
        if GPIO.input(ir) == GPIO.LOW:
            
            if same_blade:
                pass
            else:
                #print("High")
                same_blade = True
                if current_time - blade_counter_window >= 2:                  
                    print(blade_counter)
                    print("Desired rpm = " + str(RPM))
                    measured_rpm = (blade_counter *200)/ (current_time - blade_counter_window)
                    print("Measured rpm = " + str(measured_rpm))
                    print_rpm_time = current_time
                    blade_counter = 0
                    blade_counter_window = current_time
                else: 
                    blade_counter += 1
        else:
            same_blade = False

        lastClkState = clkState
        time.sleep(0.035)
except KeyboardInterrupt:
    # Clean up GPIO on keyboard interrupt
    GPIO.cleanup()