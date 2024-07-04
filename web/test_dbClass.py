import unittest
import os
import sqlite3
from dbClass import DBClient

class TestDBClient(unittest.TestCase):
    def setUp(self):
        # Setup a test database file
        self.test_db = 'test2_solarlink.db'
        self.client = DBClient()
        self.client.__dbname__ = self.test_db
        self.client.conn = sqlite3.connect(self.test_db)
        self.client.create_tables()

    def tearDown(self):
        # Remove the test database file after tests
        self.client.conn.close()
        os.remove(self.test_db)

    def test_add_and_get_user(self):
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
        self.client.add_message('device126', True, 3.7, 1.2)
        messages = self.client.get_messages('device126')
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0][1], True)
        self.assertEqual(messages[0][2], 3.7)
        self.assertEqual(messages[0][3], 1.2)

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
