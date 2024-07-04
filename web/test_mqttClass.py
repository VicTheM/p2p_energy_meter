import unittest
from mqttClass import Message

class TestMessage(unittest.TestCase):
    def test_from_dict(self):
        info = {
            "deviceID": "device001",
            "state": "on",
            "voltage": 220.0,
            "current": 1.5,
            "duration": 10.0
        }
        message = Message("", "", 0.0, 0.0, 0.0)
        message.from_dict(info)
        self.assertEqual(message.deviceID, "device001")
        self.assertEqual(message.state, "on")
        self.assertEqual(message.voltage, 220.0)
        self.assertEqual(message.current, 1.5)
        self.assertEqual(message.duration, 10.0)

if __name__ == '__main__':
    unittest.main()