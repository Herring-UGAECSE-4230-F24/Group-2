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
# GPIOS being used 5, 6, 13, 16, 17, 22, 26, 27 for keypad 
# GPIOS for the flip flop will be set up as outputs
# Clock1 pulse to update the display. Clock1 has orange wire.
# Maybe use the top left of chip for the high/low turn on/off seven segment
Q1 = 25
Q2 = 12
Q3 = 16
Q4 = 20
Q5 = 24
Q6 = 23
Q7 = 18
Q8 = 14

# global Clock1, Clock2, Clock3, Clock4
Clock1 = 11
Clock2 = 9
Clock3 = 10
Clock4 = 21
#DisPower = 15
LED = 4 # Invalid Entry LED GPIO

GPIO.setup(Q1, GPIO.OUT)
GPIO.setup(Q2, GPIO.OUT)
GPIO.setup(Q3, GPIO.OUT)
GPIO.setup(Q4, GPIO.OUT)
GPIO.setup(Q5, GPIO.OUT)
GPIO.setup(Q6, GPIO.OUT)
GPIO.setup(Q7, GPIO.OUT)
GPIO.setup(Q8, GPIO.OUT)
GPIO.setup(Clock1, GPIO.OUT)
GPIO.setup(Clock2, GPIO.OUT)
GPIO.setup(Clock3, GPIO.OUT)
GPIO.setup(Clock4, GPIO.OUT)
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, GPIO.LOW)
#GPIO.setup(DisPower, GPIO.OUT)
#GPIO.output(DisPower, GPIO.LOW)

#Wire labels
# A - 2
# B - 1
# C - 7
# D - 6
# E - 5
# F - 3
# G - 4 

# Variable for on/off function
on = True

# Remember last1 variable
last1 = None
last2 = None
last3 = None
last4 = None

# Keep track of display
dispCount = 0

display_dict = {"0": ["A", "B", "C", "D", "E", "F"], # To display each number
                "1": ["B", "C"], 
                "2": ["A", "B", "G", "E", "D"], 
                "3": ["A", "B", "G", "C", "D"], 
                "4": ["F", "G", "B", "C"], 
                "5": ["A", "F", "G", "C", "D"], 
                "6": ["A", "F", "G", "C", "D", "E"], 
                "7": ["A", "B", "C"], 
                "8": ["A", "B", "C", "D", "E", "F", "G"], 
                "9": ["A", "B", "C", "D", "F", "G"],
                "*": ["."]}

letters_dict = {"A": Q2, "B": Q1, "C": Q7, "D": Q6, "E": Q5, "F": Q3, "G": Q4, ".": Q8}

# Function to read rows and columns
def readKeypad(rowNum, char):
    curVal = None
    GPIO.output(rowNum, GPIO.LOW)
    if GPIO.input(Y1)==GPIO.LOW: # If button pressed, input is LOW
        curVal=char[0]
    elif GPIO.input(Y2)==GPIO.LOW:
        curVal=char[1]
    elif GPIO.input(Y3)==GPIO.LOW:
        curVal=char[2]
    elif GPIO.input(Y4)==GPIO.LOW:
        curVal=char[3]
    GPIO.output(rowNum,GPIO.HIGH)
    return curVal

# Function to display characters
def display_SSD(char):
    letters = display_dict[char]
    for l in letters_dict:
        if l in letters:
            GPIO.output(letters_dict[l], GPIO.HIGH)
        else:
            GPIO.output(letters_dict[l], GPIO.LOW)

def display_PM(char):
    letters = display_dict[char]
    letters.append("*")
    for l in letters_dict:
        if l in letters:
            GPIO.output(letters_dict[l], GPIO.HIGH)
        else:
            GPIO.output(letters_dict[l], GPIO.LOW)

# Function for blink numbers
def blinkDisp():
    global last4, last3, last2, last1, dispCount, Clock1, Clock2, Clock3, Clock4
    key = None
    clock = Clock1
    while(dispCount < 4):
        print(key)
        while(key == None):
            display_SSD("8")
            onDisp(clock)
            time.sleep(0.2)
            offDisp(clock)
            time.sleep(0.2)
            key = readKey()
        print(key)   
        if dispCount == 0 and key in ["0", "1", "2"]:
            GPIO.output(LED, GPIO.LOW)
            display_SSD(key)
            GPIO.output(Clock1, GPIO.HIGH)
            GPIO.output(Clock1, GPIO.LOW)
            last1 = key
            dispCount += 1
            clock = Clock2
            key = None
        elif dispCount == 1 and key in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            GPIO.output(LED, GPIO.LOW)
            temp = int (last1 + key)
            '''if temp > 12:
                temp -= 12
                H1 = str(temp[0])
                H2 = str(temp[1])
                display_SSD(H1) # Update the 24 hour clock to display pm times
                GPIO.output(Clock1, GPIO.HIGH)
                GPIO.output(Clock1, GPIO.LOW)
                display_PM(H2)
                GPIO.output(Clock2, GPIO.HIGH)
                GPIO.output(Clock1, GPIO.LOW)
                last1 = H1
                last2 = H2
            else:'''
            display_SSD(key)
            GPIO.output(Clock2, GPIO.HIGH)
            GPIO.output(Clock2, GPIO.LOW)
            last2 = key
            dispCount += 1
            clock = Clock3
            key = None
        elif dispCount == 2 and key in ["0", "1", "2", "3", "4", "5", "9"]:
            GPIO.output(LED, GPIO.LOW)
            display_SSD(key)
            GPIO.output(Clock3, GPIO.HIGH)
            GPIO.output(Clock3, GPIO.LOW)
            last3 = key
            dispCount += 1
            clock = Clock4
            key = None
        elif dispCount == 3 and key in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            GPIO.output(LED, GPIO.LOW)
            display_SSD(key)
            GPIO.output(Clock4, GPIO.HIGH)
            GPIO.output(Clock4, GPIO.LOW)
            last4 = key
            dispCount += 1
        else:
            GPIO.output(LED, GPIO.HIGH)
            key = None

# Turn off Displays
def offDisp(clk):
    print("in offdisp")
    GPIO.output(Q1, GPIO.LOW)
    GPIO.output(Q2, GPIO.LOW)
    GPIO.output(Q3, GPIO.LOW)
    GPIO.output(Q4, GPIO.LOW)
    GPIO.output(Q5, GPIO.LOW)
    GPIO.output(Q6, GPIO.LOW)
    GPIO.output(Q7, GPIO.LOW)
    GPIO.output(Q8, GPIO.LOW)
    GPIO.output(clk, GPIO.HIGH)
    GPIO.output(clk, GPIO.LOW)

# Function for turning on displays
def onDisp(clk):
    GPIO.output(clk, GPIO.HIGH)
    GPIO.output(clk, GPIO.LOW)

def allOffDisp():
    GPIO.output(Q1, GPIO.LOW)
    GPIO.output(Q2, GPIO.LOW)
    GPIO.output(Q3, GPIO.LOW)
    GPIO.output(Q4, GPIO.LOW)
    GPIO.output(Q5, GPIO.LOW)
    GPIO.output(Q6, GPIO.LOW)
    GPIO.output(Q7, GPIO.LOW)
    GPIO.output(Q8, GPIO.LOW)
    GPIO.output(Clock1, GPIO.HIGH)
    GPIO.output(Clock1, GPIO.LOW)
    GPIO.output(Clock2, GPIO.HIGH)
    GPIO.output(Clock2, GPIO.LOW)
    GPIO.output(Clock3, GPIO.HIGH)
    GPIO.output(Clock3, GPIO.LOW)
    GPIO.output(Clock4, GPIO.HIGH)
    GPIO.output(Clock4, GPIO.LOW)

# Detect reading from keypad
def readKey():
    for x, row in [(X1, ["1","2","3","A"]), (X2, ["4","5","6","B"]), (X3, ["7","8","9","C"]), (X4, ["*","0","#","D"])]:
        key = readKeypad(x, row)
        if key != None:
            return key
    return None
    
try:
    while True:
        key = readKey()
        print(key)
        # First Input
        if on == True: 
            if dispCount == 0:
                blinkDisp()

        if key == "#":
            on = not on
            if on == True:
                if last1 != None:
                    display_SSD(last1)
                    GPIO.output(Clock1, GPIO.HIGH)
                    GPIO.output(Clock1, GPIO.LOW)
                if last2 != None:
                    display_SSD(last2)
                    GPIO.output(Clock2, GPIO.HIGH)
                    GPIO.output(Clock2, GPIO.LOW)
                if last3 != None:
                    display_SSD(last3)
                    GPIO.output(Clock3, GPIO.HIGH)
                    GPIO.output(Clock3, GPIO.LOW)
                if last4 != None:
                    display_SSD(last4)
                    GPIO.output(Clock4, GPIO.HIGH)
                    GPIO.output(Clock4, GPIO.LOW)
            else:
                allOffDisp()
                
        time.sleep(0.15)

except KeyboardInterrupt:
    allOffDisp()
    GPIO.cleanup()

