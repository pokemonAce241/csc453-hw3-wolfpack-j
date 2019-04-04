import time
import json
import ibmiotf.application

import datetime

# for handling CTRL+C
import signal

# for getting command line arguments
import sys, getopt

client = None

def main():
    global client
    # register the signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        options = {
            "org": "sat52l",
            "id": "therpi",
            "auth-method": "apikey",
            "auth-key": "a-sat52l-fdaspx5lja",
            "auth-token": "dC8TO5j?ol8jUgVlJe"
        }

        client = ibmiotf.application.Client(options)
        client.connect()
        client.deviceEventCallback = deviceEventCallback
        client.subscribeToDeviceEvents(event="doorStatus")
        print("Connected to IBM Cloud!!")

    except ibmiotf.ConnectionException  as e:
        print(e)
    print("starting the loop")
    loop()
    

def deviceEventCallback(event):
    if event.event == "doorStatus":
        payload = json.loads(event.payload)
        status = payload["status"]
        print(str(datetime.datetime.now()) + " STATUS: " + status)

def loop():
        time.sleep(0.5)

def clean_up():
    global client
    print("cleaning up")
    if client:
        client.disconnect()

# handle CTRL+C
def signal_handler(sig, frame):
    print("ending")
    clean_up()
    sys.exit(0)

if __name__ == "__main__":
    main()

