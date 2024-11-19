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

with open("file.txt") as file: 
    lines=[line for line in file.readlines()] # Make array with each element being one line in the file

while dot_length == 0 or dot_length > 2 or dot_length < 0.001:
    print("Length of dot (must be between 0.001 and 2): ")
    dot_length = float(input()) # Asks user to input length of dot in terminal *doesn't do anything rn

while True:
    print("GPIO pin for output (must be between 1 and 26 *choose 20 for checkpoint): ")
    output_pin = input() # Asks user for pin to output to speaker or led 
    try: 
        output_pin = int(output_pin)
        if output_pin < 26 or output_pin > 1:
            break
    except:
        pass


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
try:
    with open(output_file, "r") as output:
        lines=[line for line in output.readlines()] 
        for line in lines:
            print(line)
            #print(line.index("|")- 1)
            mc_by_letter = line[0: line.index("|")- 1].strip().split(" ")
            print(mc_by_letter)
            for letter in mc_by_letter:
                for char in letter:
                    if char == "-":
                        p = GPIO.PWM(output_pin, 500)
                        p.start(50)
                        print("dash...")
                        time.sleep(dot_length * 3)
                        p.stop()
                    else:
                        p = GPIO.PWM(output_pin, 500)
                        p.start(50)
                        print("dot.")
                        time.sleep(dot_length)
                        p.stop()
                    time.sleep(dot_length/4)
                print("wait...")
                #GPIO.output(output_pin, GPIO.LOW)
                time.sleep(dot_length * 3)
            #GPIO.output(output_pin, GPIO.LOW)
            print("wait.......")
            time.sleep(dot_length * 7)

except KeyboardInterrupt:
    GPIO.cleanup()
        