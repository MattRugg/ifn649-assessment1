import serial
import time
import string
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

# defines which tty device we should use to communicate
# via bluetooth
ttyBluetooth = "/dev/rfcomm0"

# defines MQTT broker IP address
mqttAddress = "13.56.231.2"

# reading and writing data from and to teensy via serial
# rfcomm0 corresponds to the bluetooth device
ser = serial.Serial(ttyBluetooth, 9600)

def on_connect(client, userdata, flags, rc): # func for making connection
	print("Connecting to MQTT")
	print("Connection returned result: " + str(rc))
	client.subscribe("led")
	client.subscribe("buzzer")

def on_message(client, userdata, msg): # func for sending msg
	payload = msg.payload.decode("utf-8")
	if msg.topic == "buzzer":
		ser.write(str.encode("BUZZER_TRACK" + payload))
	elif msg.topic == "led":
		ser.write(str.encode("LED_" + payload))
	print("rcvd from MQTT: " + msg.topic + " " + payload)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqttAddress, 1883, 60)

while True:
	client.loop()

	if ser.in_waiting > 0:
		rawserial = ser.readline()

		print("rcvd from bt: ")
		cookedserial = rawserial.decode('utf-8').strip('\r\n')
		print(cookedserial)

		# publish data comming from bl serial to MQTT server
		# publish.single("ifn649", "Done", mqttAddress)
