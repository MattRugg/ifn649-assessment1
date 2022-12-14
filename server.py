from flask import Flask
from flask_mqtt import Mqtt

airtemp = "airtemp: Not Available"
airhum = "airhum: Not Available"
heatindex = "heatindex: Not Available"
soilhum = "soilhum: Not Available"

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'localhost'  # use the free broker from HIVEMQ
app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes

mqtt = Mqtt(app)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
	print("MQTT connected")
	mqtt.subscribe('airtemp')
	mqtt.subscribe('airhum')
	mqtt.subscribe('soilhum')
	mqtt.subscribe('heatindex')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
	print("MQTT received: " + message.topic + "=" + message.payload.decode())
	if message.topic == "airtemp":
		global airtemp
		airtemp = "airtemp: " + message.payload.decode()
	if message.topic == "airhum":
		global airhum
		airhum = "airhum: " + message.payload.decode()
	if message.topic == "heatindex":
		global heatindex
		heatindex = "heatindex: " + message.payload.decode()
	if message.topic == "soilhum":
		global soilhum
		soilhum = "soilhum: " + message.payload.decode()

@app.route('/ledon')
def ledon():
	mqtt.publish('led','on')
	return index()

@app.route('/ledoff')
def ledoff():
	mqtt.publish('led','off')
	return index()

@app.route('/buzzer1')
def buzzer1():
	mqtt.publish('buzzer','1')
	return index()

@app.route('/buzzer2')
def buzzer2():
	mqtt.publish('buzzer','2')
	return index()

@app.route('/')
def index():
	# HTML header tags
	retHTML  = "<html><head><title>IFN649 Assessment </title>"

	# basic styling
	retHTML += "<style>body{font-family:verdana;font-size:14px;background-color: #eee;}"
	retHTML += "a{padding:15px;text-align:center;color:black;margin:5px;border-radius:10px;display:inline-block;text-decoration:none;background-image:linear-gradient(to bottom right, cyan, #c6f6c6);}"
	retHTML += "div{margin:auto;width:400px;border-radius:10px;background-color:white;padding:10px 30px 20px}</style></head>"

	# Title block
	retHTML += "<body><div style='margin-top:40px;margin-bottom:10px;background-image:linear-gradient(to bottom right, cyan, #c6f6c6)'><h2>IFN649 Assessment 1</h2></h3>Matheus Cavalca Ruggiero<br />N10913556</h3></div>"

	# update fields according to MQTT messages
	retHTML += "<div><p>" + airtemp + "</p>"
	retHTML += "<p>" + airhum + "</p>"
	retHTML += "<p>" + soilhum + "</p>"
	retHTML += "<p>" + heatindex + "</p>"

	# operate actuators
	retHTML += "<a href='/ledon'>Turn LED on</a>"
	retHTML += "<a href='/ledoff'>Turn LED off</a>"
	retHTML += "<a href='/buzzer1'>Play buzzer track 1</a>"
	retHTML += "<a href='/buzzer2'>Play buzzer track 2</a>"

	retHTML += "</div></body></html>"
	return retHTML

if __name__ == '__main__':
	app.run(debug=True, port=80, host='0.0.0.0')
