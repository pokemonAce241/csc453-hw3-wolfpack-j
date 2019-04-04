from mpu6050 import mpu6050
import time
import json
import ibmiotf.application

# for handling CTRL+C
import signal

# for getting command line arguments
import sys, getopt

client = None
sensor = None

def main():
    global client, sensor
    # register the signal handler
    signal.signal(signal.SIGINT, signal_handler)
    status = "default"
    # parse the command line arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:")
    except getopt.GetoptError:
        print('GET OPT ERROR')
    for opt, arg in opts:
        if opt == '-i':
            status = arg

    sensor = mpu6050(0x68)
    
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
        print("Connected to IBM Cloud!!")

    except ibmiotf.ConnectionException  as e:
        print(e)
    print("starting the loop")
    loop()
    

def loop():
    global sensor
    while True:
        # a = sensor.get_accel_data() # get the acceleration data
        g = sensor.get_gyro_data() # get the gyro data
        myData = {'gyroY' : g['y']}
        client.publishEvent("RaspberryPi", "therpi", "doorSensorData", "json", myData, 2)
        time.sleep(0.1)

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

