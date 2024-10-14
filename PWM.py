#First encoder part or PWM Minor Project
import RPi.GPIO as GPIO
import time

#I don't know these pins
clk = 19 
dt = 12 
sw = 13

#Setting up the gpios as pull-up or high
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(clk,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(sw,GPIO.IN,pull_up_down=GPIO.PUD_UP)

#counter and clk state
counter=0
lastClkState=GPIO.input(clk)
 
#when the input of the encoder goes low because press. It prints press
while True:
  if GPIO.input(sw) == GPIO.LOW:
    print("Press")
  else:
    break
  
encoder_direction = None
turns_second = None

#using the counter with the clk and dt
while True:
  
    clkState=GPIO.input(clk)
    dtState=GPIO.input(dt)

    if clkState!=lastClkState:
        if dtState!=clkState:
            counter+=1
        else:
            counter-=1
        lastClkState=clkState
        print(counter)


    #prints the direction and turns per second of the encoder
    print(f"Direction {encoder_direction}")
    print(f"Turns per second {turns_second}")
    
