"""
This file is used to test every other file in this program. It is not used in the final product.
"""

# from mqttClass import MQTTClient

# broker = "test.mosquitto.org"
# port = 1883
# subtopic = "state/1/+"

# client = MQTTClient(broker, port)
# client.subscribe(subtopic)


# while True:
#     message = client.get_message()
#     if message:
#         print(f"*************   {client.get_message().to_dict()}")
#         print(type(message.current))
#         print(type(message.voltage))
#         print(type(message.duration))
#         print(type(message.state))
#         print(type(message.deviceID))

from dbClass import DBClient

client = DBClient()

# client.add_message('2232332606', True, 3.7, 1.2, 5)
# client.add_message('2232332606', False, 100, 12, 50)

print(client.get_messages('2232332606'))

print("Done")