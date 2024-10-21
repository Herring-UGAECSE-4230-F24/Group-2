import time
import RPi.GPIO as GPIO

output_pin = 0
dot_length = 0

GPIO.setwarnings(False)  # Disable GPIO warnings
GPIO.setmode(GPIO.BCM) 
# Dictionary storing all of the MC translations for the characters/numbers
MORSE_CODE_DICT = { 'a':'.-', 'b':'-...',
                    'c':'-.-.', 'd':'-..', 'e':'.',
                    'f':'..-.', 'g':'--.', 'h':'....',
                    'i':'..', 'j':'.---', 'k':'-.-',
                    'l':'.-..', 'm':'--', 'n':'-.',
                    'o':'---', 'p':'.--.', 'q':'--.-',
                    'r':'.-.', 's':'...', 't':'-',
                    'u':'..-', 'v':'...-', 'w':'.--',
                    'x':'-..-', 'y':'-.--', 'z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----'}

with open("file.txt") as file: # Open the file we want to translate
    lines=[line for line in file.readlines()] # Make array with each element being one line in the file

while dot_length == 0 or dot_length > 2 or dot_length < 0.001:
    print("Length of dot: ")
    dot_length = int(input()) # Asks user to input length of dot in terminal *doesn't do anything rn

print("GPIO pin for output: ")
output_pin = int(input()) # Asks user for pin to output to speaker or led 
GPIO.setup(output_pin, GPIO.OUT)


output_file = "output.txt" # Location of output file
open(output_file, "w").close() # Clears the file
# Convert message to morse code
first_word = True # Don't add spaces if we are on the first word of the message (each line)
with open(output_file, "w") as output: # Open the output file with write permissions
    output.write("-.-.- | attention \n") # Start by writing attention in MC
    for line in lines: # Loop through each line of the array made above
        words = line.lower().strip() # Removes any extra spacing in the line, so we only have the lines
        for word in words.split(" "): # Split the line into array of words to loop through
            chars = [*word] # Breaks the word into list of characters
            if first_word: # If it is the first word in the message, don't do anything and set it to false
                first_word = False
            else: # If it is not the first word, add the 7 spaces in front of the MC translation
                output.write("       ")
            for c in chars: # Loop through all of the characters
                output.write(MORSE_CODE_DICT[c] + " ") # Get the MC translation for each character and write to output
            output.write(" | " + word + "\n") # Add the english translation and start new line
        first_word = True # Reset first_word to true since we move to the next message now
        output.write(".-.-. | out \n") # Write the MC for out 


# Output morsecode
with open(output_file, "r") as output:
    for line in lines:
        print(line)
        print(line.index("|")- 1)
        mc_by_letter = line[0: line.index("|")- 1].split(" ")
        print(mc_by_letter)
        for letter in mc_by_letter:
            for char in letter:
                if char == "-":
                    GPIO.output(output_pin, GPIO.HIGH)
                    print("dash...")
                    time.sleep(dot_length * 3)
                    GPIO.output(output_pin, GPIO.LOW)
                else:
                    GPIO.output(output_pin, GPIO.HIGH)
                    print("dot.")
                    time.sleep(dot_length)
                    GPIO.output(output_pin, GPIO.LOW)
            print("wait...")
            time.sleep(dot_length * 3)
        print("wait.......")
        time.sleep(dot_length * 7)
        