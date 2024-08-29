import RPi.GPIO as GPIO
import time
from time import sleep
'''
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW) #replace 1 with pin number
freq = 1
deli = 1/(2*freq)

try:
    while True:
        GPIO.output(23, GPIO.HIGH)
        sleep(deli) #in seconds
        GPIO.output(23, GPIO.LOW)
        sleep(deli)
        
except KeyboardInterrupt:
    GPIO.cleanup()


import wiringpi
wiringpi.wiringPiSetup() #by physical board number
wiringpi.wiringPiSetupGpio() #by GPIO pin number
wiringpi.softToneCreate(23)
frequency = 10
wiringpi.softToneWrite(23, frequency)
#while true....
time.sleep(1000) #keep program running so code stays running
wiringpi.softToneWrite(23, 0) #shut off LED
'''
###########
import pigpio
pi = pigpio.pi() #sleect local pi for control
#pi = pigpio.pi('soft', 8888)
frequency = 1
pi.set_PWM_frequency(23, frequency)
dutyCycleValue = 127 #0 is always off, 255 is always on
pi.set_PWM_dutycycle(23, dutyCycleValue)
#while true....
time.sleep(20000) #keep program running so code stays running
pi.set_PWM_dutycycle(23, 0)
