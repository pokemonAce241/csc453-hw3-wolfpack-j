# This program will parse out the data that we need from the open and close samples
# Run this directly in the data directory

import os
import random


def stripDataClose(input, output):
    allLines = input.readlines()
    # get all of the gyroY values
    allGyroYValues = []

    for line in allLines:
        values = line.split(",")
        allGyroYValues.append(values[4])

    # find the first value that goes above the threshold
    startIndex = -1
    endIndex = -1
    array = []
    for y in allGyroYValues:
        if float(y) < closeThreshold:
            array.append(float(y))
    while len(array) > 10:
        index = random.randint(0, len(array) - 2)
        array[index] = (array[index] + array[index + 1]) / 2
        del array[index + 1]
    for y in array:
        output.write(str(y) + ",")


def stripDataOpen(input, output):
    allLines = input.readlines()
    # get all of the gyroY values
    allGyroYValues = []

    for line in allLines:
        values = line.split(",")
        allGyroYValues.append(values[4])

    # find the first value that goes above the threshold
    startIndex = -1
    endIndex = -1
    array = []
    for y in allGyroYValues:
        if float(y) > openThreshold:
            array.append(float(y))
    while len(array) > 10:
        index = random.randint(0, len(array) - 2)
        array[index] = (array[index] + array[index + 1]) / 2
        del array[index + 1]
    for y in array:
        output.write(str(y) + ",")

directory = os.fsencode("./data/")

openThreshold = 8
closeThreshold = -5
global startIndex, endIndex
isCloseData = False

for file in os.listdir(directory):
     filename = os.fsdecode(file)
     if filename.endswith("_open_sample.csv") or filename.endswith("_close_sample.csv"):
        print("opening file: " + filename)
        originalFile = open("./data/" + filename)
        strippedFile = open("./strippedData/" + filename + ".stripped.csv", "w")
        if ( filename.endswith("_close_sample.csv") ):
            stripDataClose(originalFile, strippedFile)
        else:
            stripDataOpen(originalFile, strippedFile)
