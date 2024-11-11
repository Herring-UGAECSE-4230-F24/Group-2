import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#GPIO Pins
LED = #add pin
Speaker = #pin
OutputPin = LED
Telegraph = #pin
GPIO.setup(LED, GPIO.OUT)
GPIO.setup(Speaker, GPIO.OUT)
GPIO.setup(Telegraph, GPIO.IN)

#Dictionary from Encoder.py - stores MC translations
LETTER_TO_MC_DICT = { 'a':'.-', 'b':'-...',
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

MC_TO_LETTER_DICT = { '.-':'a', '-...':'b',
                    '-.-.':'c', '-..':'d', '.':'e',
                    '..-.':'f', '--.':'g', '....':'h',
                    '..':'i', '.---':'j', '-.-':'k',
                    '.-..':'l', '--':'m', '-.':'n',
                    '---':'o', '.--.':'p', '--.-':'q',
                    '.-.':'r', '...':'s', '-':'t',
                    '..-':'u', '...-':'v', '.--':'w',
                    '-..-':'x', '-.--':'y', '--..':'z',
                    '.----':'1', '..---':'2', '...--':'3',
                    '....-':'4', '.....':'5', '-....':'6',
                    '--...':'7', '---..':'8', '----.':'9',
                    '-----':'0'}

#Variable declaration

dotLength = 0
while dotLength == 0 or dotLength > 2 or dotLength < 0.001:
    print("Length of dot (must be between 0.001 and 2): ")
    dotLength = float(input()) 

dashLength = 2 * dotLength

def telegraphInput(): #Function that monitors GPIO pin and returns duration of press
  if GPIO.input(Telegraph) == GPIO.HIGH:
    start = time.time() #Begin the clock time
    p = GPIO.PWM(LED, 500)
    p.start(50)
    GPIO.output(OutputPin, GPIO.HIGH)
    while GPIO.input(Telegraph) == GPIO.HIGH:
      pass #pass if the output is still high
    end = time.time()
    p.stop()
    length = end - start #get the time difference of the HIGH state
    if length > dashLength:
      return '-'
    elif length <= 2 * dotLength:
      return '.'
    else:
      return ' '

output_file = "output.txt" # Location of output file
open(output_file, "w").close() # Clears the file

with open(output_file, 'w') as file:
  while True:
    mcChar = telegraphInput()
    file.write(mcChar)



