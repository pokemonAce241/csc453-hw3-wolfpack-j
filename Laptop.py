from flask import Flask,redirect
from flask import renter_template
from flask import request
import os, json
import time
import ibmiotf.application
import uuid


client = None
deviceid = os.getenv("DEVICE_ID")
vcap = json.loads(os.getenv("VCAP_SERVICES"))

status = "Door Closed"
timeCommand = 0

def myCommandCallback(cmd):
	if cmd.event == "Door":
		payload = json.loads(cmd.payload)
		command = payload["DoorStatus"]
		print cmd.timestamp
		print command
		status = command
		timeCommand = cmd.timestamp
		
try:
	options = {
		"org": "5gt44o",
		"id": "TheRaspberryPi",
		"type": "standalone",
		"auth-method": "apikey",
		"auth-key": "a-5gt44o-8aw5vum4gz",
		"auth-token": "PliZTzoS8?8euK!oPq"
	}
	
	
	
	client = ibmiotf.application.Client(options)
	client.connect()
	
	client.deviceEventCallback = myCommandCallback
	client.subscribeToDeviceEvents(event="Door")
	
	#while(True):
	 # time.sleep(0.2);
	
except ibmiotf.ConnectionException as e:
	print e

app = Flask(__name__)
port = os.getenv('VCAP_APP_PORT','5000')


@app.route('/')
def hello():
	return '<!doctype html>\n
			<html>
				<head>
				<title>DoorStatus App</title>
				</head>
				<body>
					<h1>Python App</h1>
									
					<p> {{status}} </p>
					<p>time: {{timeCommand}} </p>
					

				</body>
			</html>'
				

#@app.route('/doorStatus',methods=['POST'])
#def door_route():	
	#return redirect("/",code=302)
		
	


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=int(port))
