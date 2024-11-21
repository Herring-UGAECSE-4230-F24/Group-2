import time
import pigpio #needed for rpm class
from time import sleep
import RPi.GPIO as GPIO
from Rotary import Rotary #pigpio rotary encoder import
from Test2 import reader #pigpio rpm import
import csv


pi = pigpio.pi() #initializes pigpio

clk = 18 #encoder pins
dt = 23
sw = 24

ir = 12 #infrared sensor pin
motor = 13
counter = 0 #counts falling edge from fan
pressed = 1 #bool for on / off of fan

rpm_desired = 0 #variable for user setting 
duty = 0.41 #duty cycle 

GPIO.setmode(GPIO.BCM)
GPIO.setup([clk,dt,sw], GPIO.IN)
GPIO.setup(ir, GPIO.IN)
GPIO.setup(motor, GPIO.OUT)
 
pwm = GPIO.PWM(motor, 1)

def cw(self): #turning clock wise in the encoder
    global rpm_desired, duty, pressed
    rpm_desired += 25 #expected value
    if rpm_desired > 0:
        if duty <= 96.5: #changes duty cycle since frequency does not affect it
            duty += 0.61
        pwm.start(duty) #starts at new duty cycle
        pressed = 1
    if rpm_desired > 6000: 
        rpm_desired = 6000 #max rpm value 
    
def acw(self): #anti clock wise very similar to other function
    global rpm_desired, duty, pressed
    rpm_desired -= 250
    if duty >= 0.82: #limits duty cycle from being negative
        duty -= 0.41
    pwm.start(duty)
    pressed = 1 #ensures pressed state is correct with motor
    if rpm_desired <= 0:
        pwm.stop()
        pressed = 0 #likewise to line 48
        rpm_desired = 0
   
def switch(): #switch function for encoder
    global pressed, duty 
    if pressed == 1: #if running stops running
        pwm.stop()
        pressed = 0
    
    else: #if NOT running then starts running
        pwm.start(duty)
        pressed = 1
    print("Pressed: ", pressed)
    
#sets up pins from rotary
my_rotary = Rotary(clk_gpio=18,dt_gpio=23,sw_gpio=24) 

#sets up rotary callbacks, and debounces based on rotary class
my_rotary.setup_rotary(debounce=200, up_callback=acw, down_callback=cw)
my_rotary.setup_switch(debounce=200,long_press=False,sw_short_callback=switch)

#finds the RPM from the read_RPM pigpio file, does heavy lifting since none of our methods were accurate
rotations = reader(pi, gpio = ir, pulses_per_rev = 3)


data = [['Expected', 'Measured']]
try:
    #adds stability for starting motor
    if rpm_desired > 0 and pressed == 1:
        pwm.start(duty)
    
    else:
        pwm.stop()
    
    open('test.csv', "w").close()
    while True: #prints speed
        speed = rotations.RPM() #calls RPM function
        data.append([rpm_desired, speed])
        print(rpm_desired, speed) 
        sleep(.5)

except:
    
    with open('test.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
    pwm.stop()
    GPIO.cleanup()