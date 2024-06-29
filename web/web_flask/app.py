"""
THE FLASK WEB SERVER

This is the entry point of the web application
The MQTT Client also starts here
"""

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
import json

from mqtt_client import MQTTClient
from db_client import DBClient, IoTData
from user_manager import UserManager
from iot_manager import IoTManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///iot_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initialize MQTT, DB and User Manager
broker = "test.mosquitto.org"
port = 1883
topic_sub = "data/#"
topic_pub = "commands/+/+"

mqtt_client = MQTTClient(broker, port, topic_sub, topic_pub)
db_client = DBClient('sqlite:///iot_data.db')
user_manager = UserManager()
iot_manager = IoTManager(mqtt_client, db_client, user_manager)

iot_manager.start()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    device_id = data.get('device_id')
    if user_manager.login(device_id):
        return jsonify({'status': 'success', 'message': 'Logged in successfully'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Login failed'}), 400

@app.route('/data', methods=['POST'])
def create_data():
    data = request.json
    device_id = data.get('device_id')
    topic = data.get('topic')
    payload = data.get('payload')
    
    if user_manager.is_logged_in(device_id):
        db_client.insert_data(device_id, topic, payload)
        return jsonify({'status': 'success', 'message': 'Data inserted successfully'}), 201
    else:
        return jsonify({'status': 'error', 'message': 'User not logged in'}), 403

@app.route('/data/<device_id>', methods=['GET'])
def get_data(device_id):
    if user_manager.is_logged_in(device_id):
        records = db_client.query_data(device_id)
        return jsonify([{
            'id': record.id,
            'device_id': record.device_id,
            'topic': record.topic,
            'payload': record.payload,
            'timestamp': record.timestamp
        } for record in records]), 200
    else:
        return jsonify({'status': 'error', 'message': 'User not logged in'}), 403

@app.route('/data/<record_id>', methods=['PUT'])
def update_data(record_id):
    data = request.json
    new_payload = data.get('payload')
    
    try:
        db_client.update_data(record_id, new_payload)
        return jsonify({'status': 'success', 'message': 'Data updated successfully'}), 200
    except SQLAlchemyError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/data/<record_id>', methods=['DELETE'])
def delete_data(record_id):
    try:
        db_client.delete_data(record_id)
        return jsonify({'status': 'success', 'message': 'Data deleted successfully'}), 200
    except SQLAlchemyError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/command', methods=['POST'])
def send_command():
    data = request.json
    device_id = data.get('device_id')
    command = data.get('command')
    iot_manager.send_command(device_id, json.dumps({'command': command}))
    return jsonify({'status': 'success', 'message': 'Command sent successfully'}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
