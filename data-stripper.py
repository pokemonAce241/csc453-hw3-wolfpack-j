# This program will parse out the data that we need from the open and close samples
# Run this directly in the data directory

import os

directory = os.fsencode(".")

openThreshold = 8
closeThreshold = -5



for file in os.listdir(directory):
     filename = os.fsdecode(file)
     if filename.endswith("open_sample.csv") or filename.endswith("close_sample.csv"):
        originalFile = open(filename)
        strippedFile = open(filename + ".stripped.csv", w)
        stripData(originalFile, strippedFile)

def stripData(input, output):
    allLines = input.readlines()
    # get all of the gyroY values
    allGyroYValues = []

    for line in allLines:
        values = line.split(",")
        allGyroYValues.append(values[4])

    # find the first value that goes above the threshold
    for y in allGyroYValues:


    # find the last value that is above the threshold

    # print out all of the values in between these two to the output file
