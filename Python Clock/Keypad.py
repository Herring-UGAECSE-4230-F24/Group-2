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
    If GPIO.input(Y1)==1:
    curVal=char[0]
    If GPIO.input(Y2)==1:
    curVal=char[1]
If GPIO.input(Y3)==1:
    curVal=char[2]
If GPIO.input(Y4)==1:
    curVal=char[3]
GPIO.output(rowNum,GPIO.LOW)
return curVal

try:
    while True:
        readKeypad(X1, ["1","2","3","A"])
        readKeypad(X2, ["4","5","6","B"])
        readKeypad(X3, ["7","8","9","C"])
        readKeypad(X4, ["*","0","#","D"])
        sleep(0.2)
except KeyboardInterrupt:
    GPIO.cleanup()
