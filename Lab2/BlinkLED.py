import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(1, GPIO.OUT, initial=GPIO.LOW) #replace 1 with pin number
while True:
    GPIO.output(1, GPIO.HIGH)
    sleep(0.5) #in seconds
    GPIO.output(1, GPIO.LOW)

###########
import wiringpi
#wiringpi.wiringPiSetup() #by physical board number
#wiringpi.wiringPiSetupGpio() #by GPIO pin number
wiringpi.softToneCreate(1)
frequency = 1000
wiringpi.softToneWrite(1, frequency)
#while true....
time.sleep(20) #keep program running so code stays running
wiringpi.softToneWrite(1, 0) #shut off LED

###########
import pigpio
pi = pigpio.pi() #sleect local pi for control
frequency = 1000
pi.set_PWM_frequency(1, frequency)
dutyCycleValue = 255 #0 is always off, 255 is always on
pi.set_PWM_dutycycle(1, dutyCycleValue)
#while true....
time.sleep(20) #keep program running so code stays running
pi.set_PWM_dutycycle(1, 0)