# app.py
from flask import Flask, render_template, request, jsonify, session
# import threading
# from mqttClass import MQTTClient
from ..dbClass import DBClient
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

db_client = DBClient()

# MQTT broker details
# broker = "test.mosquitto.org"
# port = 1883

# mqtt_client = MQTTClient(broker, port)

# def listen_to_mqtt():
#     mqtt_client.subscribe("state/1/+")
#     while True:
#         message = mqtt_client.get_message()
#         if message:
#             db_client.add_message(
#                 message.deviceID,
#                 message.state,
#                 message.voltage,
#                 message.current,
#                 message.duration
#             )

# # Start the MQTT listener thread
# mqtt_thread = threading.Thread(target=listen_to_mqtt)
# mqtt_thread.daemon = True
# mqtt_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    device_id = request.json.get('deviceID')
    session['device_id'] = device_id
    return jsonify({"message": "Login successful", "deviceID": device_id})

@app.route('/messages')
def get_messages():
    device_id = session.get('device_id')
    if not device_id:
        return jsonify({"error": "Not logged in"}), 403

    messages = db_client.get_messages(device_id)
    return jsonify(messages)

if __name__ == '__main__':
    app.run(debug=True)
