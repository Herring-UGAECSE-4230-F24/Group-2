For the linux GPIO program, you will use the GPIO_ON and the GPIO_OFF folder.  The "On" turns on a GPIO.  The "Off" turns off a GPIO.

Deliverables:
THIS IS A GROUP PROJECT

Use an LED for a visual aid for your square wave project.

1) Run the GPIO On and the GPIO off separately to confirm that they work for you.
2) Change the GPIO On and the GPIO off to turn on/off a different GPIO. 
3) Now, combine the two programs into one program so that you can generate a square wave (remove all the redundancies).
Name the program Linux_asm_squarewave.  Have a commented and easily changed part of your program that selects the GPIO.  Select a different GPIO than in the program provided to you.
Your selected GPIO should generate a square wave approximately a 1 second blink rate (1/2 second off, 1/2 second on).  This will require a delay loop or two, of course.
Provide two variables at the top of your program that will set the on time and the off time. Name the two variables: On_time and Off_time. They cannot be in seconds.
They must be in nanoseconds.  So, a 1 second delay would be 1,000,000,000 as an entry.  You will not have to show a square wave with a value needing more time than this.
With the max value, you should be able to support a 2 second (50/50) square wave.  This will be the slowest.  You will find the fastest.
4) Show the code loop that uses your On_time and Off_time for time delay.  Describe how many instruction cycles are run in your loop for each "tick" on the delay value entry. Explain how you determined this.
5) Run your program showing 1 Hz: 1 second (50/50), 1 second (25 on / 75 off).
6) Run your program with 1Khz at (50/50 duty cycle).  You cannot see this on an LED.  You will need to look at Oscilloscope.  What are your two delay values for this?
7) What is the fastest that you can run a 50/50 square wave with your code assuming?  Provide the delay values and the Oscilloscope output.  Provide explanation for your result and what you observe.  What assumptions are you making to determine the "goodness" of the square wave to determine the fastest frequency?  You should think about what a digital/logic device requres as a clock.
8) Take data for your linux square wave generator.  What is the frequency range?  What is the dutycycle range?  You do not have to show rise/fall times.  Show this in data and graphs.
You programmed xxx and measured yyy.  In other words, characterize the square wave.  Be complete and thorough.
9) How does this compare to your **best results** from the Python square wave project?  Include pros and cons.  Which method would you use and for what situation?  Be complete and thorough.
10) Include all written responses on ELC and **treat it like a Phython project** for requirements in your writeup.
11) Make sure your final code in on Github and is named Linux_asm_squarewave_final.
