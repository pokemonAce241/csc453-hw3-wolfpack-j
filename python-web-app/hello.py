from flask import Flask, render_template, request, jsonify
import atexit
import os
import json

# IBM IoT connection
import ibmiotf.application

# import random

import datetime

from joblib import load

ml_model = load('./trained_model.joblib') # load the file from the root project directory (NOT THIS DIRECTORY)

app = Flask(__name__, static_url_path='')

client = None
lastReceivedData = {
    "gyroY": 0,
    "time": str(datetime.datetime.now())
}

array = []
tracking = "none"

OPEN_THRESHOLD = 8
CLOSE_THRESHOLD = -5

door_status = {
    "status": "CLOSED",
    "time": str(datetime.datetime.now())
}

def myEventCallback(event):
    global lastReceivedData
    if event.event == "doorSensorData":
        payload = json.loads(event.payload)
        gyroY = payload["gyroY"]

        lastReceivedData = {
            "gyroY": gyroY,
            "time": str(datetime.datetime.now())
        }

        # run the logic for determining the start and end points of data
        saveValuesLogic(gyroY)

def saveValuesLogic(value):
    global array, tracking, ml_model, client, door_status
    if (tracking == "open"):
        if (value > OPEN_THRESHOLD):
            array.append(value)
        else:
            if (len(array) > 10):
                # reduce the data to 10 values
                # while len(array) > 10:
                #     index = random.randint(0, len(array) - 2)
                #     array[index] = (array[index] + array[index + 1]) / 2
                #     del array[index + 1]
                array = array[:10]
                # ask model what happened
                prediction = str(ml_model.predict([array]))
                if (prediction == '[0]'):
                    door_status['status'] = 'CLOSED'
                else:
                    door_status['status'] = 'OPEN'
                door_status['time'] = str(datetime.datetime.now())
                # publish the response from the model
                client.publishEvent("MLModel", "123abc", "doorStatus", "json", door_status, 2)
            if (value < CLOSE_THRESHOLD):
                tracking = "close"
                array = [] # clear the array
                array.append(value)
            else:
                tracking = "none"
                array = [] # clear the array
    elif (tracking == "close"):
        if (value < CLOSE_THRESHOLD):
            array.append(value)
        else:
            if (len(array) > 10):
                # reduce the data to 10 values
                # while len(array) > 10:
                #     index = random.randint(0, len(array) - 2)
                #     array[index] = (array[index] + array[index + 1]) / 2
                #     del array[index + 1]
                array = array[:10]
                # ask model what happened
                prediction = str(ml_model.predict([array]))
                if (prediction == '[0]'):
                    door_status['status'] = 'CLOSED'
                else:
                    door_status['status'] = 'OPEN'
                door_status['time'] = str(datetime.datetime.now())
                # publish the response from the model
                client.publishEvent("MLModel", "123abc", "doorStatus", "json", door_status, 2)
            if (value > OPEN_THRESHOLD):
                tracking = "open"
                array = [] # clear the array
                array.append(value)
            else:
                tracking = "none"
                array = [] # clear the array
    else: # tracking is none
        array = []
        if (value > OPEN_THRESHOLD):
            tracking = "open"
            array.append(value)
        elif (value < CLOSE_THRESHOLD):
            tracking = "close"
            array.append(value)

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

@app.route('/')
def root():
    return app.send_static_file('door-status.html')

@app.route('/door-status')
def get_door_status():
    global door_status
    return jsonify(door_status)

@app.route("/ibmiot-status")
def getIbmIotConnectionStatus():
    """connection status route"""
    state = {"ibmIotConnStatus": "DISCONNECTED"}
    if (client):
        state = {"ibmIotConnStatus": "CONNECTED"}
    return jsonify(state)

@app.route("/last-received-data")
def getLastReceivedData():
    """last received data route"""
    global lastReceivedData
    return jsonify(lastReceivedData)

@app.route('/test-ml-model', methods=['POST'])
def testMlModel():
    global ml_model
    json = request.get_json(force=True)
    values = json['values']
    prediction = {'prediction': str(ml_model.predict([values]))}
    return jsonify(prediction)

@atexit.register
def shutdown():
    if client:
        client.disconnect()

if __name__ == '__main__':
    try:
        options = {
            "org": "sat52l",
            "id": "web-app",
            "auth-method": "apikey",
            "auth-key": "a-sat52l-fdaspx5lja",
            "auth-token": "dC8TO5j?ol8jUgVlJe"
        }
        client = ibmiotf.application.Client(options)
        client.connect()
        client.deviceEventCallback = myEventCallback
        client.subscribeToDeviceEvents(event="doorSensorData")
    except ibmiotf.ConnectionException as e:
        print(e)
    app.run(host='0.0.0.0', port=port, debug=True)
