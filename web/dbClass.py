""" 
THIS FILE DEFINES THE DATABASE CLIENT CLASS
"""
import sqlite3
from datetime import datetime

class DBClient:
    """
    The class can perform the basic CRUD operations
    The database has three tables

    - Users: stores the following
            * Username
            * deviceID (primary key)
            * Node (an integer)
            * UserID (unique)

    - messages: Has the following fields
            * DeviceID (foreign key)
            * state (boolean)
            * voltage (float)
            * current (float)
            * time (now)

    - Accounts: table to hold users account balance
            * deviceID (foreign key)
            * currentBalance
    """

    __dbname__ = "test_solarlink.db"
    __usertable__ = "users"
    __accounttable__ = "accounts"
    __messagetable__ = "messages"

    def __init__(self):
        """Connects or creates the database"""
        self.conn = sqlite3.connect(self.__dbname__)
        self.create_tables()

    def create_tables(self):
        """Creates all the required table for the db if they don't exist"""
        with self.conn:
            self.conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.__usertable__} (
                Username TEXT,
                deviceID TEXT PRIMARY KEY,
                Node INTEGER,
                UserID TEXT UNIQUE
            );
            """)
            self.conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.__messagetable__} (
                DeviceID TEXT,
                state BOOLEAN,
                voltage FLOAT,
                current FLOAT,
                time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(DeviceID) REFERENCES {self.__usertable__}(deviceID)
            );
            """)
            self.conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.__accounttable__} (
                deviceID TEXT,
                currentBalance FLOAT,
                FOREIGN KEY(deviceID) REFERENCES {self.__usertable__}(deviceID)
            );
            """)

    def add_user(self, username, device_id, node, user_id):
        """Adds a new user to the user table if user does not already exist"""
        with self.conn:
            duplicate = self.conn.execute(f"""
            SELECT * FROM {self.__usertable__} WHERE deviceID = {device_id}
            OR UserID = {user_id}
            """)

            if not duplicate.fetchone():
                self.conn.execute(f"""
                INSERT INTO {self.__usertable__} (Username, deviceID, Node, UserID)
                VALUES (?, ?, ?, ?)
                """, (username, device_id, node, user_id))

    def get_user(self, device_id=None):
        cursor = self.conn.cursor()
        if device_id is None:
            cursor.execute(f"""
            SELECT * FROM {self.__usertable__}""")
            return cursor.fetchall()
        else:
            cursor.execute(f"""
            SELECT * FROM {self.__usertable__} WHERE deviceID = ?
            """, (device_id,))
            return cursor.fetchone()

    def update_user(self, device_id, **kwargs):
        columns = ", ".join(f"{key} = ?" for key in kwargs.keys())
        values = list(kwargs.values()) + [device_id]
        with self.conn:
            self.conn.execute(f"""
            UPDATE {self.__usertable__} SET {columns} WHERE deviceID = ?
            """, values)

    def delete_user(self, device_id):
        with self.conn:
            self.conn.execute(f"""
            DELETE FROM {self.__usertable__} WHERE deviceID = ?
            """, (device_id,))
            self.conn.execute(f"""
            DELETE FROM {self.__messagetable__} WHERE DeviceID = ?
            """, (device_id,))
            self.conn.execute(f"""
            DELETE FROM {self.__accounttable__} WHERE deviceID = ?
            """, (device_id,))

    def add_message(self, device_id, state, voltage, current):
        with self.conn:
            self.conn.execute(f"""
            INSERT INTO {self.__messagetable__} (DeviceID, state, voltage, current)
            VALUES (?, ?, ?, ?)
            """, (device_id, state, voltage, current))

    def get_messages(self, device_id):
        cursor = self.conn.cursor()
        cursor.execute(f"""
        SELECT * FROM {self.__messagetable__} WHERE DeviceID = ?
        ORDER BY time DESC
        """, (device_id,))
        return cursor.fetchall()

    def add_account(self, device_id, balance):
        with self.conn:
            self.conn.execute(f"""
            INSERT INTO {self.__accounttable__} (deviceID, currentBalance)
            VALUES (?, ?)
            """, (device_id, balance))

    def get_account_balance(self, device_id):
        cursor = self.conn.cursor()
        cursor.execute(f"""
        SELECT currentBalance FROM {self.__accounttable__} WHERE deviceID = ?
        """, (device_id,))
        return cursor.fetchone()

    def update_account_balance(self, device_id, new_balance):
        with self.conn:
            self.conn.execute(f"""
            UPDATE {self.__accounttable__} SET currentBalance = ? WHERE deviceID = ?
            """, (new_balance, device_id))

    def __del__(self):
        self.conn.close()