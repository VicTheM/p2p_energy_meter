"""
SERVER ENTRY POINT

BOTH THE WEB ROUTES AND API ARE DEFINED HERE
"""
from flask import Flask, redirect, render_template, request, jsonify, session
from dbClass import DBClient
from mqttClass import MQTTClient
import os
import subprocess
import utilFunctions as func
import sys
import atexit
from pathlib import Path

broker = "broker.hivemq.com"
port = 1883
subtopic = "data/1/{}" # deviceID is the last part of the topic
pubtopic = "commands/1/{}"

app = Flask(__name__)
# app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = os.urandom(24)


usersDBClient = DBClient(connect=False)
mqttClient = MQTTClient(broker, port)
watcher_process = None


def start_background_services():
    """Seed the database and start the MQTT watcher for this app process."""
    global watcher_process
    if watcher_process is not None and watcher_process.poll() is None:
        return watcher_process

    app_dir = Path(__file__).resolve().parent
    web_dir = app_dir.parent
    seed_script = web_dir / 'populateDB.py'
    watcher_script = app_dir / 'mqttWatcher.py'

    subprocess.run(
        [sys.executable, str(seed_script)],
        cwd=str(app_dir),
        check=True,
    )
    watcher_process = subprocess.Popen(
        [sys.executable, str(watcher_script)],
        cwd=str(app_dir),
    )
    return watcher_process


def stop_background_services():
    if watcher_process is not None and watcher_process.poll() is None:
        watcher_process.terminate()
        watcher_process.wait()


atexit.register(stop_background_services)

if os.environ.get('START_BACKGROUND_SERVICES') == '1':
    start_background_services()



@app.route('/', methods = ['GET'])
def index():
    return render_template('index_modern.html')

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
        'dashboard_modern.html',
        device_id=device_id,
        state=state,
        voltage=voltage,
        current=current,
        duration=duration,
        account_balance=account_balance,
        totalPowerSent=round(totalPowerSent/1000, 2),
        totalPowerReceived=round(totalPowerReceived/1000, 2)
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
        "voltage": 226,
        "current": current,
        "duration": duration,
        "account_balance": account_balance,
        "totalPowerSent": round(totalPowerSent/1000, 2),
        "totalPowerReceived": round(totalPowerReceived/1000, 2),
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
        usersDBClient.connect()
        usersDBClient.add_message(device_id=device_id, state=state, voltage=0, current=0)
        usersDBClient.disconnect()
        return jsonify({"state": state})


    return jsonify({"message": "success"})


@app.route('/logout')
def logout():
    session.pop('device_id', None)
    return redirect('/', code=302)


if __name__ == '__main__':
    start_background_services()
    app.run(host='0.0.0.0', port='5000')
