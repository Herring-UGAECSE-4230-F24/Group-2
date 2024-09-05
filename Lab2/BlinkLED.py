import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT, initial=GPIO.LOW) #replace 1 with pin number
freq = 1
deli = 1/(2*freq)

try:
    while True:
        GPIO.output(24, GPIO.HIGH)
        sleep(deli) #in seconds
        GPIO.output(24, GPIO.LOW)
        sleep(deli)
        
except KeyboardInterrupt:
    GPIO.cleanup()

'''

import wiringpi
wiringpi.wiringPiSetup() #by physical board number
wiringpi.wiringPiSetupGpio() #by GPIO pin number
wiringpi.softToneCreate(24)
frequency = 10
try:
    wiringpi.softToneWrite(24, frequency)
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    wiringpi.softToneWrite(24, 0)
    wiringpi.softToneStop(24)

###########

import pigpio
pi = pigpio.pi() #sleect local pi for control
#pi = pigpio.pi('soft', 8888)
frequency = 10
try:
    pi.set_PWM_frequency(24, frequency)
    dutyCycleValue = 127 #0 is always off, 255 is always on
    pi.set_PWM_dutycycle(24, dutyCycleValue)
    while True:
        time.sleep(200) #keep program running so code stays running
except KeyboardInterrupt:
    pi.set_PWM_dutycycle(24, 0)
    '''
