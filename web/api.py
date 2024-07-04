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