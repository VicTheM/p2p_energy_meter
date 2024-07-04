from flask import Flask, render_template, request, jsonify
import threading
from mqttClass import MQTTClient
from dbClass import DBClient

app = Flask(__name__)

# Initialize the database client
db_client = DBClient()

# MQTT broker details
broker = "test.mosquitto.org"
port = 1883

# Initialize the MQTT client
mqtt_client = MQTTClient(broker, port)
topic = "state/1/+"

# Background thread to listen for MQTT messages and store them in the database
def listen_to_mqtt():
    mqtt_client.subscribe(topic)
    while True:
        message = mqtt_client.get_message()
        if message:
            db_client.add_message(
                message.deviceID,
                message.state,
                message.voltage,
                message.current,
                message.duration
            )

# Start the MQTT listener thread
mqtt_thread = threading.Thread(target=listen_to_mqtt)
mqtt_thread.daemon = True
mqtt_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    device_id = request.form.get('deviceID')
    messages = db_client.get_messages(device_id)
    return jsonify(messages)

if __name__ == '__main__':
    app.run(debug=True)
