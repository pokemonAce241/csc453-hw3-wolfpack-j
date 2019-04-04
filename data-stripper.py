# This program will parse out the data that we need from the open and close samples
# Run this directly in the data directory

import os
import random


def stripDataClose(input):
    allLines = input.readlines()
    # get all of the gyroY values
    allGyroYValues = []

    for line in allLines:
        values = line.split(",")
        allGyroYValues.append(values[4])

    # find the first value that goes above the threshold
    array = []
    for y in allGyroYValues:
        if float(y) < closeThreshold:
            array.append(float(y))
    while len(array) > 10:
        index = random.randint(0, len(array) - 2)
        array[index] = (array[index] + array[index + 1]) / 2
        del array[index + 1]
    # for y in array:
    #     output.write(str(y) + ",")
    return array


def stripDataOpen(input):
    allLines = input.readlines()
    # get all of the gyroY values
    allGyroYValues = []

    for line in allLines:
        values = line.split(",")
        allGyroYValues.append(values[4])

    # find the first value that goes above the threshold
    array = []
    for y in allGyroYValues:
        if float(y) > openThreshold:
            array.append(float(y))
    while len(array) > 10:
        index = random.randint(0, len(array) - 2)
        array[index] = (array[index] + array[index + 1]) / 2
        del array[index + 1]
    # for y in array:
    #     output.write(str(y) + ",")
    return array


def print2DArray(file, array):
    for row in array:
        line = ",".join(map(str, row))
        file.write(line + "\n")

directory = os.fsencode("./data/")

openThreshold = 8
closeThreshold = -5
isCloseData = False

combinedOpenFile = open("./combinedData/open_samples.csv", "w")
combinedCloseFile = open("./combinedData/close_samples.csv", "w")

open_rows_samples = []
close_rows_samples = []

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    print("opening file: " + filename)
    originalFile = open("./data/" + filename)
    if filename.endswith("_open_sample.csv"):
        array = stripDataOpen(originalFile)
        print(array)
        open_rows_samples.append(array)
    elif filename.endswith("_close_sample.csv"):
        array = stripDataClose(originalFile)
        print(array)
        close_rows_samples.append(array)

print2DArray(combinedOpenFile, open_rows_samples)
print2DArray(combinedCloseFile, close_rows_samples)
