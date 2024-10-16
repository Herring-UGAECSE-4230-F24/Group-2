import RPi.GPIO as GPIO
import time
clk = 18
dt = 23
sw = 24

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(clk,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(sw,GPIO.IN,pull_up_down=GPIO.PUD_UP)

# Counter and Clk states
counter = 0
lastClkState = GPIO.input(clk)
speed = 0
rot_start_time = 0
last_time = 0
debounce = 0.001
last_edge = 0
try:
    while True:
        current_time = time.time()
        clkState = GPIO.input(clk)

        if (current_time - last_edge) >= debounce:

            if GPIO.input(sw) == GPIO.LOW:
                print("Press")
                time.sleep(0.2)
            
            elif(clkState == GPIO.LOW and lastClkState == GPIO.HIGH):
                if rot_start_time == 0:
                    rot_start_time = current_time
                else:
                    time_diff = current_time - last_time
                    if time_diff > 0:
                        speed = (1 / time_diff) / 140  # turns per second
                last_time = current_time

                if GPIO.input(dt) == GPIO.LOW:
                    counter -= 1
                    print("CCW")
                else:
                    counter += 1
                    print("CW")
                print(counter)
                print(f"Speed: {speed:.2f} turns/sec")
                    

        lastClkState = clkState

except KeyboardInterrupt:
    GPIO.cleanup()