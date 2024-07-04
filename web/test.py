"""
This file is used to test every other file in this program. It is not used in the final product.
"""

from mqttClass import MQTTClient

broker = "test.mosquitto.org"
port = 1883
subtopic = "state/1/+"

client = MQTTClient(broker, port)
client.subscribe(subtopic)


while True:
    message = client.get_message()
    if message:
        print(f"*************   {client.get_message().to_dict()}")
        print(type(message.current))
        print(type(message.voltage))
        print(type(message.duration))
        print(type(message.state))
        print(type(message.deviceID))