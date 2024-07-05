"""
This file is used to test every other file in this program. It is not used in the final product.
"""

from mqttClass import MQTTClient
from dbClass import DBClient


dbclient = DBClient()

broker = "test.mosquitto.org"
port = 1883
subtopic = "data/1/+"

client = MQTTClient(broker, port)
client.subscribe(subtopic)


while True:
    message = client.get_message()
    if message:
        print(f"*************   {message.to_dict()}")
        print(type(message.current))
        print(type(message.voltage))
        print(type(message.duration))
        print(type(message.state))
        print(type(message.deviceID))

        dbclient.add_message(message.deviceID, message.state, message.voltage, message.current, message.duration) # Add message to database

        print("***************************************************************************************")    
        print(dbclient.get_messages('001'))
        print("----------------------------------------------------------------------------------------")