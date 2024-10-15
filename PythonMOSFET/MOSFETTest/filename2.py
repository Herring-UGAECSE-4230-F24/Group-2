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
statement = ""
try:
    while True:
        clkState = GPIO.input(clk)
        if GPIO.input(sw) == GPIO.LOW:
            print("Press")
            statement = "not"
            time.sleep(0.2)
        
        elif(clkState == GPIO.LOW and lastClkState == GPIO.HIGH):
            if GPIO.input(dt) == GPIO.LOW:
                counter -= 1
                print("CCW")
            else:
                counter += 1
                print("CW")
            print(counter)
            statement = "not"
        else:
            if(statement != "None"):
                statement = "None"
                print(statement)
                

        lastClkState = clkState

except KeyboardInterrupt:
    GPIO.cleanup()