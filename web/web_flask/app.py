# app.py
from flask import Flask, redirect, render_template, request, jsonify, session
from ..dbClass import DBClient
from ..mqttClass import MQTTClient
import os
import subprocess
from .. import utilFunctions as func

broker = "test.mosquitto.org"
port = 1883
subtopic = "data/1/{}" # deviceID is the last part of the topic
pubtopic = "commands/1/{}"

subprocess.Popen(['python', '../mqttWatcher.py'])
app = Flask(__name__)
app.secret_key = os.urandom(24)

usersDBClient = DBClient(connect=False)
mqttClient = MQTTClient(broker, port)



@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    device_id = request.form.get('deviceID')
    usersDBClient.connect()
    user = usersDBClient.get_user(device_id)
    if not user:
        return jsonify({"ERROR": f"No device with id '{device_id}'"}), 404
    session['device_id'] = device_id

    account_balance = usersDBClient.get_account_balance(device_id)[0]
    messages = usersDBClient.get_messages(device_id)
    print(messages)
    usersDBClient.disconnect()
    
    totalPowerReceived = 0
    totalPowerSent = 0
    state = 0
    voltage = 0
    current = 0
    duration = 0
    if len(messages) > 0:
        state = messages[0][1]
        voltage = messages[0][2]
        current = messages[0][3]
        duration = messages[0][4]
        sending = [message for message in messages if message[1] == 1]
        if len(sending) > 0:
            totalPowerSent = func.calculate_energy(sending)
        receiving = [message for message in messages if message[1] == 2]
        if len(receiving) > 0:
            totalPowerReceived = func.calculate_energy(receiving)

    return render_template(
        'dashboard.html',
        device_id=device_id,
        state=state,
        voltage=voltage,
        current=current,
        duration=duration,
        account_balance=account_balance,
        totalPowerSent=totalPowerSent,
        totalPowerReceived=totalPowerReceived
        )

    # return jsonify({"device_id": device_id, "state": state, "voltage": voltage, "current": current, "duration": duration, "account_balance": account_balance})  

@app.route('/updatepage')
def get_messages():
    """The SPA"""
    device_id = session.get('device_id')
    if not device_id:
        return jsonify({"error": "Not logged in"}), 403
    
    usersDBClient.connect()
    account_balance = usersDBClient.get_account_balance(device_id)[0]
    messages = usersDBClient.get_messages(device_id)
    usersDBClient.disconnect()
    
    totalPowerReceived = 0
    totalPowerSent = 0
    state = 0
    voltage = 0
    current = 0
    duration = 0
    if len(messages) > 0:
        state = messages[0][1]
        voltage = messages[0][2]
        current = messages[0][3]
        duration = messages[0][4]
        sending = [message for message in messages if message[1] == 1]
        if len(sending) > 0:
            totalPowerSent = func.calculate_energy(sending)
        receiving = [message for message in messages if message[1] == 2]
        if len(receiving) > 0:
            totalPowerReceived = func.calculate_energy(receiving)

    payload = {
        "state": state,
        "voltage": voltage,
        "current": current,
        "duration": duration,
        "account_balance": account_balance,
        "totalPowerSent": totalPowerSent,
        "totalPowerReceived": totalPowerReceived,
        "newstate": state
    }
    return jsonify(payload)

@app.route('/actions', methods=['POST'])
def actions():
    device_id = session.get('device_id')
    state = request.args.get('state')
    credit = request.args.get('credit')

    if not device_id:
        return jsonify({"error": "Not logged in"}), 403
    
    if not state and not credit:
        return jsonify({"error": "No state provided"}), 400
    
    if credit:
        amount = float(credit)
        usersDBClient.connect()
        prev_balance = usersDBClient.get_account_balance(device_id)[0]
        credit = prev_balance + amount
        usersDBClient.update_account_balance(device_id, credit)
        usersDBClient.disconnect()

        return jsonify({"credit": credit})
    
    if state:
        print(f"state: {state}")
        mqttClient.publish(pubtopic.format(device_id), f'{{"state":{state}, "ack":1}}')
        return jsonify({"state": state})


    return jsonify({"message": "success"})

@app.route('/logout')
def logout():
    session.pop('device_id', None)
    return redirect('/', code=302)

if __name__ == '__main__':
    app.run(debug=True)
