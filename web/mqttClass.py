import paho.mqtt.client as mqtt

class MQTTClient:
    """ Class to handle MQTT communication """
    __numberOfClients__ = 0

    def __init__(self, broker, port):
        self.client = mqtt.Client()
        self.broker = broker
        self.port = port
        self.topic_sub = ""
        self.topic_pub = ""
        type(self).__numberOfClients__ += 1

    def connect(self):
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()

    def subscribe(self, topic_sub, on_message):
        self.topic_sub = topic_sub
        self.client.subscribe(self.topic_sub)
        self.client.on_message = on_message

    def publish(self, topic_pub, message):
        self.topic_pub = topic_pub
        self.client.publish(self.topic_pub, message)