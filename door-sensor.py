from mpu6050 import mpu6050
import time
import json
import ibmiotf.application

# for handling CTRL+C
import signal

# for getting command line arguments
import sys, getopt

client = None
data_file = None
sensor = None

def main():
    global client, data_file, sensor
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
    
    data_file = open("data/" + str(int(time.time())) + "_" + status + "_sample.csv", "a+")

    sensor = mpu6050(0x68)
    
    #try:
    #    options = ibmiotf.application.ParseConfigFile("./device.cfg")

#        client = ibmiotf.application.Client(options)
 #       client.connect()
  #      client.deviceEventCallback = myCommandCallback
   #     client.subscribeToDeviceEvents(event="light")

    #except ibmiotf.ConnectionException  as e:
     #   print(e)
    print("starting the loop")
    loop()
    

def loop():
    global sensor, data_file
    while True:
        a = sensor.get_accel_data() # get the acceleration data
        g = sensor.get_gyro_data() # get the gyro data
        data_file.write("{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f}\n".format(a['x'], a['y'], a['z'], g['x'], g['y'], g['z']))
        time.sleep(0.1)
        #myData = {'buttonPushed' : True}
        # client.publishEvent("RaspberryPi", "b827eb4fa1e2", "buttonPress", "json", myData)
    

    

def myCommandCallback(cmd):
    print("You got a command.")
    print(cmd)

def clean_up():
    global data_file, client
    print("cleaning up")
    if data_file:
        data_file.close()
    if client:
        client.disconnect()

# handle CTRL+C
def signal_handler(sig, frame):
    print("ending")
    clean_up()
    sys.exit(0)

if __name__ == "__main__":
    main()

