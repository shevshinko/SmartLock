import RPi.GPIO as GPIO
import datetime
from flask import *
from time import sleep
import _thread

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define actuators GPIOs
relay  = 18	#GPIO 18 to IN port on Relay
btn = 23 
led = 24

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
	button_state = GPIO.input(btn)
	if button_state == False:
		lockSts = "Lock closed!"
	else:
		lockSts = "Lock open!"
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
			lockSts = "Lock closed!"
		else:
			GPIO.output(led, True)
			lockSts = "Lock open!"
			
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
	button_state = GPIO.input(btn)
	if button_state == False:
		lockSts = "Lock closed!"
	else:
		lockSts = "Lock open!"

	return redirect(url_for("index"))

if __name__ == "__main__":
	_thread.start_new_thread(listner, ())
	app.run(host="0.0.0.0", port=80,threaded=True)
