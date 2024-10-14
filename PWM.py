#First encoder part or PWM Minor Project
import RPi.GPIO as GPIO
import time

#I don't know these pins
clk = 19 
dt = 12 
sd = 13

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(clk,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(sd,GPIO.IN,pull_up_down=GPIO.PUD_UP)

counter=0
lastClkState=GPIO.input(clk)

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
    
