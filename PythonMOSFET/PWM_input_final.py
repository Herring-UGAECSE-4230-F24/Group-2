#First encoder part or PWM Minor Project
import RPi.GPIO as GPIO
import time

#setting the pins
clk = 18 
dt = 23 
sw = 24

#Setting up the gpios as pull-up or high
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(clk,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(sw,GPIO.IN,pull_up_down=GPIO.PUD_UP)

#counter and clk state
counter=0
lastClkState=GPIO.input(clk)
speed=0
  
lastchange = False
starttime = 0
turns = 0
  
#using the counter with the clk and dt
try:
    while True:
      
      clkState=GPIO.input(clk)
      dtState=GPIO.input(dt)

      if GPIO.input(sw) == GPIO.LOW:
        print("Press")
        time.sleep(.2)
        
      
      if clkState!=lastClkState:
        if not lastchange:
          starttime = time.time()
          lastchange = True
        if dtState!=clkState:
          counter+=1 # Number counter for CW
          #print("Clockwise,      " + str(counter))
        else:
          counter-=1 # Number counter for CCW
          #print("Counter Clockwise,      " + str(counter))

          lastClkState=clkState
        print(counter)
        turns += 1
      else:
        speed = turns / (time.time() - starttime)
        if speed != 0:
          print("Speed: " + str(speed))
        turns = 0
        lastchange = False
      time.sleep(0.04)

        
    
except KeyboardInterrupt:
  GPIO.cleanup()
    
  
    
