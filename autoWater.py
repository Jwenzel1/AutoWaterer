#!/usr/bin/python3
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.")

import os.path as fileChecker
import datetime
import time

DATAFILE = ".wateringInfo"
TIMEFILE = ".lastWatered"
OUTPUTPIN = 12

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(OUTPUTPIN, GPIO.OUT, initial = GPIO.HIGH)
    
def waterThosePlants(secondsToWater):
    GPIO.output(OUTPUTPIN, GPIO.LOW)
    t = time.time() + secondsToWater
    print("Watering those plants baby!")
    time.sleep(secondsToWater)
    GPIO.output(OUTPUTPIN, GPIO.HIGH)

def getLastWatered():
    if not fileChecker.exists(TIMEFILE):
        f = open(TIMEFILE , 'w')
        f.write("1 1 1 1 1 1 1\n")
        f.close()

    f = open(TIMEFILE , 'r')
    values = [int(i) for i in f.readline().strip().split(" ")]
    f.close()
    return datetime.datetime(values[0], values[1], values[2], values[3],values[4], values[5], values[6])
   

def writeLastWatered(datetimeToWrite):
    f = open(TIMEFILE , 'w')
    f.write("%d %d %d %d %d %d %d\n" %(datetimeToWrite.year,
                                       datetimeToWrite.month,
                                       datetimeToWrite.day,
                                       datetimeToWrite.hour,
                                       datetimeToWrite.minute,
                                       datetimeToWrite.second,
                                       datetimeToWrite.microsecond))
    f.close()

def getSecondsHoursDays():
    f = open(DATAFILE, 'r')
    values = []
    for line in f:
        values.append(int(line.strip().split("=")[1]))
    return values
    
def main():
    while(True):
        secondsToWater, hoursToWait, daysToWait = getSecondsHoursDays()
        wateringInterval = datetime.timedelta(days = daysToWait,
                                              hours = hoursToWait)
        timeToWater = getLastWatered() + wateringInterval
        currentTime = datetime.datetime.now()
        if currentTime >= timeToWater:
            waterThosePlants(secondsToWater)
            writeLastWatered(currentTime)
        time.sleep(5)

try:
    main()
except:
    GPIO.cleanup()
