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

startTime = 0

try:
    while True:
        
        if GPIO.input(sw) == GPIO.LOW:
            print("Press")
            time.sleep(0.2)

        clkState = GPIO.input(clk)
        if(clkState == GPIO.LOW and lastClkState == GPIO.HIGH):
            if GPIO.input(dt) == GPIO.LOW:
                counter += 1
            else:
                counter -= 1
            print(counter)
        lastClkState = clkState

except KeyboardInterrupt:
    GPIO.cleanup()