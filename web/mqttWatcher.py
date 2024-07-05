from mqttClass import MQTTClient
from dbClass import DBClient


dbclient = DBClient()

broker = "test.mosquitto.org"
port = 1883
subtopic = "data/1/+"

client = MQTTClient(broker, port)
client.subscribe(subtopic)

print("Started MQTT watcher")
while True:
    message = client.get_message()
    if message:
        dbclient.add_message(message.deviceID, message.state, message.voltage, message.current, message.duration) # Add message to database