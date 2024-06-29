from classes import MQTTClient, DBClient, UserManager, IoTManager
import json


if __name__ == "__main__":
    broker = "test.mosquitto.org"
    port = 1883
    topic_sub = "VictoryIsNotangry"
    topic_pub = "HeJustChanged...Again"
    db_url = ""  # Yet to get one

    mqtt_client = MQTTClient(broker, port, topic_sub, topic_pub)
    db_client = DBClient(db_url)
    user_manager = UserManager()
    iot_manager = IoTManager(mqtt_client, db_client, user_manager)

    iot_manager.start()

    # Example of user operations
    device_id = "user_device_id"
    if user_manager.login(device_id):
        user_manager.create_record(device_id, "topic", "payload")
        records = user_manager.read_records(device_id)
        print(records)
        user_manager.update_record(records[0].id, "new_payload")
        user_manager.delete_record(records[0].id)

    # Example of sending a command
    iot_manager.send_command(json.dumps({"command": "turn_on_led"}))
