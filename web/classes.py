""" THIS FILE DEFINS ALL CLASSES THAT WILL BE USED IN APPLICATION LOGIC"""
import paho.mqtt.client as mqtt

from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class IoTData(Base):
    """ Class to represent the IoT data """
    __tablename__ = 'iot_data'
    id = Column(Integer, primary_key=True)
    device_id = Column(String)
    topic = Column(String)
    payload = Column(String)
    timestamp = Column(DateTime, default=func.now())

class DBClient:
    """ Class to handle database operations """
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def insert_data(self, device_id, topic, payload):
        session = self.Session()
        new_data = IoTData(device_id=device_id, topic=topic, payload=payload)
        session.add(new_data)
        session.commit()
        session.close()

    def query_data(self, device_id):
        session = self.Session()
        data = session.query(IoTData).filter_by(device_id=device_id).all()
        session.close()
        return data

    def update_data(self, record_id, new_payload):
        session = self.Session()
        data = session.query(IoTData).filter_by(id=record_id).first()
        if data:
            data.payload = new_payload
            session.commit()
        session.close()

    def delete_data(self, record_id):
        session = self.Session()
        data = session.query(IoTData).filter_by(id=record_id).first()
        if data:
            session.delete(data)
            session.commit()
        session.close()


class MQTTClient:
    """ Class to handle MQTT communication """
    def __init__(self, broker, port, topic_sub, topic_pub):
        self.client = mqtt.Client()
        self.broker = broker
        self.port = port
        self.topic_sub = topic_sub
        self.topic_pub = topic_pub

    def connect(self):
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()

    def subscribe(self, on_message):
        self.client.subscribe(self.topic_sub)
        self.client.on_message = on_message

    def publish(self, message):
        self.client.publish(self.topic_pub, message)


class UserManager:
    """ Class to manage users """
    def __init__(self):
        self.logged_in_users = {}

    def login(self, device_id):
        # Simulate a login process
        self.logged_in_users[device_id] = True
        return True

    def is_logged_in(self, device_id):
        return self.logged_in_users.get(device_id, False)

    def logout(self, device_id):
        self.logged_in_users.pop(device_id)


class IoTManager:
    """ The main guy who uses every other class to do the job"""
    def __init__(self, mqtt_client, db_client):
        self.messenger = mqtt_client
        self.organiser = db_client
        self.messenger.client.on_message = self.on_message

    def on_message(self, client, userdata, message):
        topic = message.topic
        payload = message.payload.decode('utf-8')
        print(f"Received message: {payload} on topic: {topic}")
        self.organiser.insert_data(topic, payload)

    def start(self):
        self.messenger.connect()
        self.messenger.subscribe(self.on_message)

    def send_command(self, command):
        self.messenger.publish(command)