import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
channel = 26
frequency = 100
desiredFrequency = 200
GPIO.setup(channel, GPIO.OUT)
pwm=GPIO.PWM(channel, frequency)
pwm.ChangeFrequecy(desiredFrequency)

try:
    while True:
        pwm.start()
except KeyboardInterrupt:
    GPIO.cleanup()
    pwm.stop()