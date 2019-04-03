# This program will parse out the data that we need from the open and close samples
# Run this directly in the data directory

import os


def stripData(input, output):
    allLines = input.readlines()
    # get all of the gyroY values
    allGyroYValues = []

    for line in allLines:
        values = line.split(",")
        allGyroYValues.append(values[4])

    # find the first value that goes above the threshold
    startIndex = -1
    endIndex = -1
    for y in allGyroYValues:
        # if the data is door closed data, then we make sure the y value is below the close threshold
        if isCloseData and float(y) < closeThreshold:
            print(y)
            output.write(y + ",")
        # if the data is door open data, then we make sure the y value is above the door open threshold    
        elif not isCloseData and float(y) > openThreshold:
            print(y)
            output.write(y + ",")


directory = os.fsencode("./data/")

openThreshold = 8
closeThreshold = -5
global startIndex, endIndex
isCloseData = False

for file in os.listdir(directory):
     filename = os.fsdecode(file)
     if filename.endswith("_open_sample.csv") or filename.endswith("_close_sample.csv"):
        if ( filename.endswith("_close_sample.csv") ):
            isCloseData = True
        print("opening file: " + filename)
        originalFile = open("./data/" + filename)
        strippedFile = open("./strippedData/" + filename + ".stripped.csv", "w")
        stripData(originalFile, strippedFile)
