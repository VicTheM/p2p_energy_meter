"""
This module contains unit tests for the dbClass module.

All test must pass everytime a chnage is made to the dbClass module.
"""

import unittest
import os
import sqlite3
from dbClass import DBClient

class TestDBClient(unittest.TestCase):
    def setUp(self):
        # Setup a test database file
        self.test_db = 'test2_solarlink.db'
        self.client = DBClient(self.test_db)
        self.client.create_tables()

    def tearDown(self):
        # Remove the test database file after tests
        self.client.conn.close()
        os.remove(self.test_db)

    def test_add_and_get_user(self):
        self.client.add_user('Victory', 'device143', 1, 'user001')
        self.client.add_user('Victory', 'device143', 1, 'user001')
        self.client.add_user('Victory', 'device123', 1, 'user001')
        user = self.client.get_user('device123')
        self.assertIsNotNone(user)
        self.assertEqual(user[0], 'Victory')
        self.assertEqual(user[1], 'device123')
        self.assertEqual(user[2], 1)
        self.assertEqual(user[3], 'user001')

    def test_update_user(self):
        self.client.add_user('Bob', 'device124', 2, 'user002')
        self.client.update_user('device124', Username='Bobby', Node=3)
        user = self.client.get_user('device124')
        self.assertIsNotNone(user)
        self.assertEqual(user[0], 'Bobby')
        self.assertEqual(user[2], 3)

    def test_delete_user(self):
        self.client.add_user('Charlie', 'device125', 3, 'user003')
        self.client.delete_user('device125')
        user = self.client.get_user('device125')
        self.assertIsNone(user)

    def test_add_and_get_message(self):
        self.client.add_user('David', 'device126', 4, 'user004')
        self.client.add_message('device126', True, 3.7, 1.2, 5)
        messages = self.client.get_messages('device126')
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0][1], True)
        self.assertEqual(messages[0][2], 3.7)
        self.assertEqual(messages[0][3], 1.2)
        self.assertEqual(messages[0][4], 5)

    def insert_message_data(self):
        sample_data = [
            ('device123', True, 2.3, 1.2, 60.0),
            ('device123', False, 3.3, 1.2, 40.0),
            ('device123', True, 4.3, 1.2, 30.0),
            ('device123', True, 5.3, 1.5, 3.0),
            ('device123', True, 6.3, 1.2, 0.1),
        ]
        for data in sample_data:
            self.client.add_message(*data)

    def test_delete_all_messages(self):
        self.insert_message_data()
        self.client.delete_message('device123')
        cursor = self.client.conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {self.client.__messagetable__} WHERE DeviceID = 'device123'")
        count = cursor.fetchone()[0]
        self.assertEqual(count, 0)

    def test_delete_most_recent_message(self):
        self.insert_message_data()
        self.client.delete_message('device123', 0)
        cursor = self.client.conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {self.client.__messagetable__} WHERE DeviceID = 'device123'")
        count = cursor.fetchone()[0]
        self.assertEqual(count, 4)

    def test_delete_oldest_n_messages(self):
        self.insert_message_data()
        self.client.delete_message('device123', 2)
        cursor = self.client.conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {self.client.__messagetable__} WHERE DeviceID = 'device123'")
        count = cursor.fetchone()[0]
        self.assertEqual(count, 3)

    def test_delete_oldest_n_messages_not_enough(self):
        self.insert_message_data()
        self.client.delete_message('device123', 6)
        cursor = self.client.conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {self.client.__messagetable__} WHERE DeviceID = 'device123'")
        count = cursor.fetchone()[0]
        self.assertEqual(count, 5)

    def test_add_and_get_account_balance(self):
        self.client.add_user('Eve', 'device127', 5, 'user005')
        self.client.add_account('device127', 100.0)
        balance = self.client.get_account_balance('device127')
        self.assertIsNotNone(balance)
        self.assertEqual(balance[0], 100.0)

    def test_update_account_balance(self):
        self.client.add_user('Frank', 'device128', 6, 'user006')
        self.client.add_account('device128', 200.0)
        self.client.update_account_balance('device128', 250.0)
        balance = self.client.get_account_balance('device128')
        self.assertIsNotNone(balance)
        self.assertEqual(balance[0], 250.0)

if __name__ == '__main__':
    unittest.main()
