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
          
        elif (clkState == GPIO.LOW and lastclkState == GPIO.HIGH):
          current_time = time.time()
          if rot_start_time == 0:
              rot_start_time = current_time
          else:
              time_diff = current_time - last_time
              if time_diff > 0:
                speed = (1 / time_diff) / 140  # turns per second
          last_time = current_time

          if dtState == GPIO.HIGH:
              print("CW")
              counter += 1
          else:
              print("CCW")
              counter -= 1
          print(counter)
          print(f"Speed: {speed:.2f} turns/second")
          

        lastclkState = clkState
        last_edge = current_time

        time.sleep(0.05)
    
except KeyboardInterrupt:
  GPIO.cleanup()
    
  
    
