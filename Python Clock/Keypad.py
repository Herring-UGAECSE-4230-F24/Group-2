import RPi.GPIO as GPIO
import time
from time import sleep

# Row GPIOS
X1 = 17
X2 = 27
X3 = 22
X4 = 5

# Column GPIOS
Y1 = 6
Y2 = 13
Y3 = 19
Y4 = 26

# Set up GPIOS
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(X1, GPIO.OUT)
GPIO.setup(X2, GPIO.OUT)
GPIO.setup(X3, GPIO.OUT)
GPIO.setup(X4, GPIO.OUT)
GPIO.setup(Y1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Y2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Y3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Y4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to read rows and columns
def readKeypad(rowNum, char):
    GPIO.output(rowNum, GPIO.HIGH)
    curVal = None
    if GPIO.input(Y1)==0: # If button pressed, input is LOW
        curVal=char[0]
    if GPIO.input(Y2)==0:
        curVal=char[1]
    if GPIO.input(Y3)==0:
        curVal=char[2]
    if GPIO.input(Y4)==0:
        curVal=char[3]
    GPIO.output(rowNum,GPIO.LOW)
    return curVal

try:
    while True:
        key = None # Variable to store the key value to print
        key = readKeypad(X1, ["1","2","3","A"]) or key
        key = readKeypad(X2, ["4","5","6","B"]) or key
        key = readKeypad(X3, ["7","8","9","C"]) or key
        key = readKeypad(X4, ["*","0","#","D"]) or key
        if key:
            print("Key pressed: " + key + "\n") # Print the key value
        sleep(0.2)
except KeyboardInterrupt:
    GPIO.cleanup()
