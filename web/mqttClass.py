# Description: Class to handle MQTT communication
import paho.mqtt.client as mqtt
import json

class Message:
    """ The message structue coming from broker """
    def __init__(self, deviceID, state, voltage, current, duration):
        self.deviceID = deviceID
        self.state = state
        self.voltage = voltage
        self.current = current
        self.duration = duration

    def to_dict(self):
        return {
            "deviceID": self.deviceID,
            "state": self.state,
            "voltage": self.voltage,
            "current": self.current,
            "duration": self.duration
        }
    
    def from_dict(self, info):
        self.deviceID = info["deviceID"]
        self.state = info["state"]
        self.voltage = info["voltage"]
        self.current = info["current"]
        self.duration = info["duration"]

    def __str__(self):
        return f"deviceID: {self.deviceID}, state: {self.state}, voltage: {self.voltage}, current: {self.current}, duration: {self.duration}"

    def __repr__(self):
        return f"deviceID: {self.deviceID}, state: {self.state}, voltage: {self.voltage}, current: {self.current}, duration: {self.duration}"






class MQTTClient:
    """ Class to handle MQTT communication """

    def __init__(self, broker, port):
        self.client = mqtt.Client()
        self.broker = broker
        self.port = port
        self.client.on_message = self.on_message
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()
        self.message = Message("", "", 0.0, 0.0, 0.0)
        self.update = False

    def on_message(self, client, userdata, message):
        """Receives the message in json form and deserialize it"""
        print(f"Received message '{message.payload.decode()}' on topic '{message.topic}'")
        self.message.from_dict(self.extract(message))
        self.update = True

    def subscribe(self, topic_sub):
        self.client.subscribe(topic_sub)
        print(f"Subscribed to topic '{topic_sub}'")

    def publish(self, topic_pub, message):
        self.client.publish(topic_pub, message)

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
        print("Disconnected from MQTT broker")

    def extract(self, message):
        """Extracts a dictionary from the message payload
        
        The dictionary will have the template:
        {
            "deviceID": "deviceID",
            "state": "state",
            "voltage": "voltage",
            "current": "current",
            "duration": "duration"
        }
        """
        deviceID = message.topic.split('/')[-1]
        info = json.loads(message.payload.decode())
        return {
            "deviceID": deviceID,
            "state": info["state"],
            "voltage": info["voltage"],
            "current": info["current"],
            "duration": info["duration"]
        }
    
    def get_message(self):
        return self.message
    
    def get_update(self):
        if (self.update):
            self.update = False
            return True
        return self.update