import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#GPIO Number
channel = 26

#Changeable
frequency = 5

GPIO.setup(channel, GPIO.OUT)
GPIO.output(channel, GPIO.HIGH)
pwm=GPIO.PWM(channel, frequency)


try:
    while True:
        #Duty Cycle
        pwm.start(50)
except KeyboardInterrupt:
    GPIO.cleanup()
    pwm.stop()