#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import sys

OUTPUTPIN = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(OUTPUTPIN, GPIO.OUT, initial = GPIO.HIGH)

try:
    if(len(sys.argv) != 2):
        print("usage: prime.py \"num\" ; where \"num\" is an integer")
        sys.exit()
    else:
        waitTime = 0    
        try:
            waitTime = int(sys.argv[1])
        except:
            print("Pass in an integer next time")
            sys.exit()
        GPIO.output(OUTPUTPIN, GPIO.LOW)
        time.sleep(waitTime)
finally:
    GPIO.cleanup()
            
