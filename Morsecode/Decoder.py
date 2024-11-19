import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#GPIO Pins
OutputPin = 20
Telegraph = 5
GPIO.setup(OutputPin, GPIO.OUT)
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
dashLength = 0
halfLength = 0

def telegraphInput(): #Function that monitors GPIO pin and returns duration of press
  if GPIO.input(Telegraph) == GPIO.HIGH:
    start = time.time() #Begin the clock time
    p = GPIO.PWM(OutputPin, 500)
    p.start(50)
    time.sleep(0.01)
    while GPIO.input(Telegraph) == GPIO.HIGH:
      pass #pass if the output is still high
    end = time.time()
    p.stop()
    length = end - start #get the time difference of the HIGH state
    if length >= halfLength:
      return '-'
    elif length < halfLength:
      return '.'
  else: #returns how long a space is if nothing is pressed
    #print('else')
    start = time.time()
    time.sleep(0.01)
    temp = start
    while GPIO.input(Telegraph) == GPIO.LOW:
      if time.time() - temp > 3*dotLength:
        print("3 DOT")
        temp = time.time()
    end = time.time()
    length = end - start
    if length >= 3 * dotLength and length < 7 * dotLength:
      return 'letter break'
    elif length >= 7 * dotLength:
      return 'word break'
    else:
      return -1

def attentionIn():    
  if GPIO.input(Telegraph) == GPIO.HIGH:
    start = time.time() #Begin the clock time
    p = GPIO.PWM(OutputPin, 500)
    p.start(50)
    time.sleep(0.01)
    while GPIO.input(Telegraph) == GPIO.HIGH:
      pass #pass if the output is still high
    end = time.time()
    p.stop()
    length = end - start
    return length
  else:
    return -1

try:
  output_file = "output.txt" # Location of output file
  open(output_file, "w").close() # Clears the file

  with open(output_file, 'w') as file:
    print("Sign Attention : ")
    sum = 0
    for i in range(5): # attention is -.-.- so i just loop through 5 characters
      #print(i)
      while True: # keep looping until it reads a high
        a = attentionIn()
        time.sleep(0.01)
        if a != -1:
          sum += a # add the length of the character
          break #break out of while loop to get to next i in for loop
    dotLength = sum / 11 #find lengthof dot based on length of total attention length
    print(dotLength)
    dashLength = 3 * dotLength #dash length is 3* dot length
    halfLength = (dashLength + dotLength)/2.0#halfway point is found in order have leeway between dot and dash
    letters = []
    temp = ''
    file.write('-.-.- | attention \n')
    
    while True: #loop code will go through until out or keyboard exception
      mcChar = telegraphInput() #call telegraphInput function to read high or low on GPIO
      print(mcChar)
      if mcChar == -1: #no breaks, keep going
        continue
      if mcChar == 'letter break': #start of a new letter
        file.write(" ")
        letters.append(temp) #add the mc to letter array
        temp = ''

      elif mcChar == 'word break': # end of wrod
        letters.append(temp) #still add mc to letter array
        temp = ''
        if letters != ['']: #make sure array not empty
          file.write(" | ") 
          for l in letters: #check if mc letter in dictionary
            if l in MC_TO_LETTER_DICT: #if it is, print it out
                file.write(MC_TO_LETTER_DICT[l])
            else: #if not, write a ?
              file.write('?')
          file.write("\n")
        letters = [] #clear the array
      else:
        temp = temp + mcChar #temp is mc of letter and each dot or dash is added to temp
        file.write(mcChar) #write each code character to file
        if temp == ".-.-.": #check for out code
          file.write(" | out")
          break #exit if out
      
      time.sleep(0.01) #small time delay to debouncy
except:
  GPIO.cleanup()



