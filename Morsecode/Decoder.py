import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#GPIO Pins
LED = #add pin
Speaker = #pin
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
                    '-.-.':'c', '-..''d', '.':'e',
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
dashLength = 0

def telegraphInput(): #Function that monitors GPIO pin and returns duration of press
  while GPIO.input(Telegraph) == GPIO.HIGH:
    start = time.time() #Begin the clock time
    while GPIO.input(Telegraph) == GPIO.HIGH:
      pass #pass if the output is still high
    end = time.time()
    length = end - start #get the time difference of the HIGH state
    if length == (dashLength+1) or length == (dashLength-1):
      return '-'
    elif length == (dotLength+1) or length == (dotLength-1):
      return '.'
    else
      return ' '




