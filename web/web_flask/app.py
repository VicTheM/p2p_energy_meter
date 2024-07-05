# app.py
from flask import Flask, redirect, render_template, request, jsonify, session
from ..dbClass import DBClient
import os
import subprocess

# Execute b.py
subprocess.Popen(['python', '../mqttWatcher.py'])

app = Flask(__name__)
app.secret_key = os.urandom(24)

db_client = DBClient()
usersDBClient = DBClient(connect=False)

print("App started")

# # MQTT broker details
# broker = "test.mosquitto.org"
# port = 1883
# subscribe_topic = "data/1/+"

# mqtt_client = MQTTClient(broker, port)

# def listen_to_mqtt():
#     mqtt_client.subscribe(subscribe_topic)
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
    device_id = request.form.get('deviceID')
    session['device_id'] = device_id
    return redirect('/messages', code=302)
    

@app.route('/messages')
def get_messages():
    """The SPA"""
    device_id = session.get('device_id')
    if not device_id:
        return jsonify({"error": "Not logged in"}), 403

    usersDBClient.connect()
    messages = usersDBClient.get_messages(device_id)
    print(f"Messages: {messages}")
    usersDBClient.disconnect()
    return jsonify(messages)

# @app.route('/actions')

# @app.route('/credit')

if __name__ == '__main__':
    app.run(debug=True)
