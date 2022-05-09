import RPi.GPIO as GPIO
import datetime
from flask import *
from time import sleep
import _thread

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define actuators GPIOs
relay  = 18	#GPIO 18 (pin 12 on RPI) to IN port on Relay
btn = 23 #Closing indicator to GPIO 23 (pin 16 on RPI)
led = 24 #LED to GPIO 24 (pin 18 on RPI)

# Initialize GPIO status variables
lockSts = 0

# Define led pins as output
GPIO.setup(relay, GPIO.OUT)
GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(led, GPIO.OUT)

# Turn lock ON
GPIO.output(relay, GPIO.HIGH)

@app.route("/")
def index():
	# Read Sensors Status
	now = datetime.datetime.now()
	timeString = now.strftime("%Y-%m-%d %H:%M")
	templateData = {
	      'title' : 'Spectres secret page!',
	      'time' : timeString,
	      'lockSts' : lockSts,
        }
	return render_template('index.html', **templateData)

def listner():
	while True:
		button_state = GPIO.input(btn)
		if button_state == False:
			GPIO.output(led, False)
		else:
			GPIO.output(led, True)
			
@app.route("/<deviceName>/<action>")
def action(deviceName, action):
	if deviceName == 'lock':
		actuator = relay
	now = datetime.datetime.now()
	timeString = now.strftime("%Y-%m-%d %H:%M")

	if action == "open":
		GPIO.output(actuator, GPIO.LOW)
		sleep(1)
		GPIO.output(actuator, GPIO.HIGH)   
	lockSts = GPIO.input(actuator)
	templateData = {
		'title' : 'Spectres secret page!',
		'time' : timeString,
		'lockSts' : lockSts,
        }
	return render_template('index.html', **templateData)

def listner():
	while True:
		button_state = GPIO.input(btn)
		if button_state == False:
			GPIO.output(led, False)
		else:
			GPIO.output(led, True)
	
if __name__ == "__main__":
	_thread.start_new_thread(listner, ())
	app.run(host="0.0.0.0", port=80,threaded=True)