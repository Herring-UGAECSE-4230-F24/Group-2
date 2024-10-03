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
# Clock pulse to update the display. Clock has orange wire.
# Maybe use the top left of chip for the high/low turn on/off seven segment
Q1 = 25
Q2 = 12
Q3 = 16
Q4 = 20
Q5 = 24
Q6 = 23
Q7 = 18
Q8 = 14
Clock1 = 21
Clock2 = 1 #change
Clock3 = 1 #change
Clock4 = 1 #change
LEDpin = 1 #change
DisPower = 15

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
GPIO.setup(LEDpin, GPIO.OUT)
GPIO.setup(DisPower, GPIO.OUT)
GPIO.output(DisPower, GPIO.LOW)

#Wire labels
#A - 2
#B - 1
#C - 7
#D - 6
#E - 5
#F - 3
#G - 4 

# Variable for on/off function
on = False

# Remember last variable
last = None

#Dictionary to reference what segment of the SSD to light up to display each number/character
display_dict = {"0": ["A", "B", "C", "D", "E", "F"], 
                "1": ["B", "C"], 
                "2": ["A", "B", "G", "E", "D"], 
                "3": ["A", "B", "G", "C", "D"], 
                "4": ["F", "G", "B", "C"], 
                "5": ["A", "F", "G", "C", "D"], 
                "6": ["A", "F", "G", "C", "D", "E"], 
                "7": ["A", "B", "C"], 
                "8": ["A", "B", "C", "D", "E", "F", "G"], 
                "9": ["A", "B", "C", "D", "F", "G"],
                "D": ["B", "C", "D", "E", "G"],
                "*": ["."]}

#Dictionary to reference which pin each SSD segment is connected to 
letters_dict = {"A": Q2, "B": Q1, "C": Q7, "D": Q6, "E": Q5, "F": Q3, "G": Q4, ".": Q8}

# Function to read rows and columns.
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

"""This function sets the necessary GPIO pins HIGH for what input character is to be displayed 
    and by checking the c"""

def display_SSD(char):
    letters = display_dict[char]
    for l in letters_dict:
        if l in letters:
            GPIO.output(letters_dict[l], GPIO.HIGH)
        else:
            GPIO.output(letters_dict[l], GPIO.LOW)

try:
    while True:
        for x, row in [(X1, ["1","2","3","A"]), (X2, ["4","5","6","B"]), (X3, ["7","8","9","C"]), (X4, ["*","0","#","D"])]:
            key = readKeypad(x, row)
            if key != None:
                print(key)
                break
        if on == True and key in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "D", "*"]:
            display_SSD(key)
            GPIO.output(Clock, GPIO.HIGH)
            GPIO.output(Clock, GPIO.LOW)
            last = key

        if key == "#":
            on = not on
            if on == True:
                GPIO.output(DisPower, GPIO.HIGH)
                if last != None:
                    display_SSD(last)
                    GPIO.output(Clock, GPIO.HIGH)
                    GPIO.output(Clock, GPIO.LOW)
            else:
                GPIO.output(DisPower, GPIO.LOW)
                GPIO.output(Q1, GPIO.LOW)
                GPIO.output(Q2, GPIO.LOW)
                GPIO.output(Q3, GPIO.LOW)
                GPIO.output(Q4, GPIO.LOW)
                GPIO.output(Q5, GPIO.LOW)
                GPIO.output(Q6, GPIO.LOW)
                GPIO.output(Q7, GPIO.LOW)
                GPIO.output(Q8, GPIO.LOW)

        time.sleep(0.15)

except KeyboardInterrupt:
    GPIO.cleanup()
