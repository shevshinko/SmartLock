import RPi.GPIO as GPIO
import datetime
from flask import *
from time import sleep
import _thread

key = "19511369"

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define actuators GPIOs
relay  = 18 #GPIO 18 to IN port on Relay
btn = 23 
led = 24

# Define led pins as output
GPIO.setup(relay, GPIO.OUT)
GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(led, GPIO.OUT)

# Turn lock ON
GPIO.output(relay, GPIO.HIGH)

@app.route("/", methods=['GET', 'POST'])
def index():
	# Read Sensors Status
	now = datetime.datetime.now()
	timeString = now.strftime("%Y-%m-%d %H:%M")
	button_state = GPIO.input(btn)
	if button_state == False:
		lockSts = "Locked!"
	else:
		lockSts = "Unlocked!"
		
	templateData = {
	      'title' : 'Spectres secret page!',
	      'time' : timeString,
	      'lockSts' : lockSts,
        }
	
	if request.method == 'POST':
		passkey = request.form['pwd']
	
		if passkey == key:
			return redirect(url_for('device'))
		return redirect(url_for('index'))
    
	return render_template('pass.html', **templateData)

def listner():
	while True:
		button_state = GPIO.input(btn)
		if button_state == False:
			GPIO.output(led, False)
			lockSts = "Locked!"
		else:
			GPIO.output(led, True)
			lockSts = "Unlocked!"

@app.route("/lock")
def device():
	actuator = relay
	now = datetime.datetime.now()
	timeString = now.strftime("%Y-%m-%d %H:%M")
	button_state = GPIO.input(btn)
	if button_state == False:
		lockSts = "Locked!"
	else:
		lockSts = "Unlocked!"
	
	templateData = {
	      'title' : 'Spectres secret page!',
	      'time' : timeString,
	      'lockSts' : lockSts,
        }
	return render_template('index.html', **templateData)

@app.route("/lock/open")
def action():
	actuator = relay
	GPIO.output(actuator, GPIO.LOW)
	sleep(1)
	GPIO.output(actuator, GPIO.HIGH)
	return render_template('lock.html', title='Spectres secret page!')

@app.route("/spectre")
def spectre():
	filename = 'spectre.jpg'
	return send_file(filename)
	
@app.route("/final")
def final():
	filename = 'final.png'
	return send_file(filename)

@app.route("/stroomschema")
def stroom():
	filename = 'stroomschema.png'
	return send_file(filename)

if __name__ == "__main__":
	_thread.start_new_thread(listner, ())
	app.run(host="0.0.0.0", port=80,threaded=True)
