"""
This file is used to test every other file in this program. It is not used in the final product.
"""
import time

from mqttClass import MQTTClient
from dbClass import DBClient


dbclient = DBClient()

broker = "test.mosquitto.org"
port = 1883
subtopic = "data/1/+"

def calculate_energy(data):
  """
  Calculates the energy consumed from either a list single tuple or a list of multiple tuples containing voltage, current, and duration data.

  Args:
      data: Either a single array representing a data point or a list of arrays, where each array contains:
          - Index 2: Voltage in volts
          - Index 3: Current in milliamperes (mA)
          - Index 4: Duration in seconds

  Returns:
      The total energy consumed in joules.
  """

  if len(data) > 1:
    # If a list of arrays is provided, calculate energy for each entry
    total_energy = 0
    for entry in data:
      voltage = entry[2]
      current = entry[3] / 1000  # Convert mA to A
      duration = entry[4]
      energy = voltage * current * duration
      total_energy += energy 
    return total_energy
  else:
    # If a single array is provided, calculate energy directly
    data = data[0]
    voltage = data[2]
    current = data[3] / 1000  # Convert mA to A
    duration = data[4]
    return voltage * current * duration

# client = MQTTClient(broker, port)
# client.subscribe(subtopic)


# while True:
#     message = client.get_message()
#     if message:
#         print(f"*************   {message.to_dict()}")
#         print(type(message.current))
#         print(type(message.voltage))
#         print(type(message.duration))
#         print(type(message.state))
#         print(type(message.deviceID))

#         dbclient.add_message(message.deviceID, message.state, message.voltage, message.current, message.duration) # Add message to database
# ID = '007'
# dbclient.add_message(ID, True, 2, 3, 5)
# time.sleep(1)
# dbclient.add_message(ID, True, 4, 5, 5)
# time.sleep(1)
# dbclient.add_message(ID, False, 6, 5, 2)
# time.sleep(1)
# dbclient.add_message(ID, False, 2, 10, 5)

# print("***************************************************************************************")
# messages = dbclient.get_messages(ID)    
# print(messages)
# print("----------------------------------------------------------------------------------------")

# sending = [message for message in messages if message[1] == True]
# receiving = [message for message in messages if message[1] == False]

# print(sending)
# print(receiving)

# dbclient.delete_message(ID)
# print(dbclient.get_messages(ID))
# state = messages[0][1]
# voltage = messages[0][2]
# current = messages[0][3]
# duration = messages[0][4]

# account_balance = dbclient.get_account_balance('001')[0]
# print(account_balance)

# I want to obtain the total power sent or received

messages = [
  ('001', 1, 9.0, 2.0, 0.500999987, '2024-07-05 11:08:44'),
  ('001', 1, 9.0, 53.0, 0.0, '2024-07-05 11:08:00'),
  ('001', 11, 11.0, 11.0, 11.0, '2024-07-05 10:39:19'),
  ('001', 10, 10.0, 10.0, 10.0, '2024-07-05 10:38:43'),
  ('001', 9, 9.0, 9.0, 9.0, '2024-07-05 10:38:07'),
  ('001', 8, 8.0, 8.0, 8.0, '2024-07-05 10:37:52'),
  ('001', 7, 7.0, 7.0, 7.0, '2024-07-05 10:37:46'),
  ('001', 6, 6.0, 6.0, 6.0, '2024-07-05 10:31:22'),
  ('001', 0, 4.0, 4.0, 4.0, '2024-07-05 10:10:23'),
  ('001', 3, 3.0, 3.0, 3.0, '2024-07-05 10:10:16'),
  ('001', 2, 2.0, 2.0, 2.0, '2024-07-05 10:09:55'),
  ('001', 0, 1.0, 0.0, 0.0, '2024-07-05 10:07:40'), 
  ('001', 9, 10.0, 11.0, 12.0, '2024-07-05 10:07:26')
  ]

sending = [message for message in messages if message[1] == True]
receiving = [message for message in messages if message[1] == False]
print(sending)
print(receiving)

print(type(sending))
print(type(receiving))

print(type(sending[0]))
print(type(receiving[0]))