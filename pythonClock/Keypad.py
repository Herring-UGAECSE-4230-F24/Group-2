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
Y3 = 16
Y4 = 26

# Set up GPIOS for keypad
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

# GPIOS for the flip flop

# Function to read rows and columns
def readKeypad(rowNum, char):
    curVal = None
    GPIO.output(rowNum, GPIO.LOW)
    if GPIO.input(Y1)==GPIO.LOW: # If button pressed, input is HIGH
        curVal=char[0]
    elif GPIO.input(Y2)==GPIO.LOW:
        curVal=char[1]
    elif GPIO.input(Y3)==GPIO.LOW:
        curVal=char[2]
    elif GPIO.input(Y4)==GPIO.LOW:
        curVal=char[3]
    GPIO.output(rowNum,GPIO.HIGH)
    return curVal

try:
    while True:
        for x, row in [(X1, ["1","2","3","A"]), (X2, ["4","5","6","B"]), (X3, ["7","8","9","C"]), (X4, ["*","0","#","D"])]:
            key = readKeypad(x, row)
            if key != None:
                print(key)
                break

        time.sleep(0.2)
        
    # GPIOS being used 5, 6, 13, 16, 17, 22, 26, 27 for keypad 
    # GPIOS for the flip flog will be set up as outputs
    # clock pulse to update the display. Cloc has orange wire.
    # Maybe use the top left of chip for the high/low turn on/off seven segment
except KeyboardInterrupt:
    GPIO.cleanup()
