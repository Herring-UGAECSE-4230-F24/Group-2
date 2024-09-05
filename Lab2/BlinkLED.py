
import RPi.GPIO as GPIO
import time
from time import sleep
#----------RPI.GPIO------------
# Initialize GPIOS
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT, initial=GPIO.LOW) #replace 1 with pin number
freq = 1 # Measured frequency in Hz
deli = 1/(2*freq) # Calculate delay from frequency value

try:
    while True:
        GPIO.output(24, GPIO.HIGH)
        sleep(deli) # delay in seconds
        GPIO.output(24, GPIO.LOW)
        sleep(deli)
        
except KeyboardInterrupt:
    GPIO.cleanup()

'''
#----------WIRINGPI------------
import wiringpi
wiringpi.wiringPiSetup() #Initialize by physical board number
wiringpi.wiringPiSetupGpio() #Initialize by by GPIO pin number
wiringpi.softToneCreate(24)
frequency = 10 # set frequency
try:
    wiringpi.softToneWrite(24, frequency)
    while True:
        time.sleep(100) # How long program will run
except KeyboardInterrupt:
    wiringpi.softToneWrite(24, 0) # Stop program
    wiringpi.softToneStop(24) # Clean up

#----------PIGPIO------------
import pigpio
pi = pigpio.pi() #sleect local pi for control
#pi = pigpio.pi('soft', 8888)
frequency = 10 # Set frequency
try:
    pi.set_PWM_frequency(24, frequency) # Set frequency to pin
    dutyCycleValue = 127 #0 is always off, 255 is always on
    pi.set_PWM_dutycycle(24, dutyCycleValue) # Set duty cycle
    while True:
        time.sleep(200) # Keep program running
except KeyboardInterrupt:
    pi.set_PWM_dutycycle(24, 0) # Stop program
'''
