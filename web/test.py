"""
This file is used to test every other file in this program. It is not used in the final product.
"""
# import sqlite3
# from dbClass import DBClient

# client = DBClient()
# client.create_tables()

# Test inserting same user multiple times
# client.add_user("a", 7, 0, 7)
# client.add_user("a", 4, 0, 4)
# client.add_user("b", 5, 0, 5)
# client.add_user("a", 6, 0, 6)


# users = client.get_user()
# for user in users:
#     print(user)

# client.add_user('David', 'device126', 4, 'user004')
# client.add_message('device126', True, 3.7, 1.2)
# messages = client.get_messages('device126')

# for message in messages:
#     print(message)
# con = sqlite3.connect("test_solarlink.db")
# cur = con.cursor()

# with con:
#     all = con.execute("SELECT * FROM users WHERE  deviceID = 5 OR UserID = 5")
#     duplicate = all.fetchone()

#     if duplicate[1] == '5':
#         print(f"deviceid: {duplicate[1]}")

from mqttClass import MQTTClient

broker = "test.mosquitto.org"
port = 1883
subtopic = "state/1/+"

client = MQTTClient(broker, port)
client.subscribe(subtopic)


while True:
    if client.get_update():
        print(client.get_message().to_dict())

        message = client.get_message()
        print(type(message.current))
        print(type(message.voltage))
        print(type(message.duration))
        print(type(message.state))
        print(type(message.deviceID))