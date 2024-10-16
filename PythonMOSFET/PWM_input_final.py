#First encoder part or PWM Minor Project
import RPi.GPIO as GPIO
import time

# Setting the pins
clk = 18 
dt = 23 
sw = 24

# Setting up the gpios as pull-up or high
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(clk,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(sw,GPIO.IN,pull_up_down=GPIO.PUD_UP)

# Counter and clk state
counter = 0
lastClkState=GPIO.input(clk)

last_edge = 0
speed = 0
last_time = 0
starttime = 0
debounce = 0.001
rot_start_time = 0
lastclkState=GPIO.input(clk)
  
# Using the counter with the clk and dt
try:
    while True:
      current_time = time.time()

      clkState=GPIO.input(clk)
      dtState=GPIO.input(dt)

      if (current_time - last_edge) >= debounce:

        if GPIO.input(sw) == GPIO.LOW:
          print("Press")
          time.sleep(.2)
          
        if (clkState == GPIO.LOW and lastclkState == GPIO.HIGH):
          if rot_start_time == 0:
              rot_start_time = current_time
          else:
              time_diff = current_time - last_time
              if time_diff > 0:
                speed = (1 / time_diff) / 140  # turns per second
          last_time = current_time

          if dtState!=clkState:
            counter+=1 # Number counter for CW
            print("Clockwise")
          else:
            counter-=1 # Number counter for CCW
            print("Counter Clockwise")
            

          print(f"Counter: {counter}")
          print(f"Speed: {speed}")


        lastClkState = clkState
        last_edge = current_time

        time.sleep(0.04)

        
    
except KeyboardInterrupt:
  GPIO.cleanup()
    
  
    
