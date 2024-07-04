
""" 
THIS FILE DEFINES THE DATABASE CLIENT CLASS
"""
import sqlite3

class DBClient:
    """
    The class can perform the basic CRUD operations
    The database has three tables

    - Users: stores the following
            * Username
            * deviceID (primary key)
            * Node (an integer)
            * UserID

    - messages: Has the following fields
            * DeviceID (foreign key)
            * state (boolean)
            * voltage (float)
            * current (float)
            * duration (float)
            * time (now)

    - Accounts: table to hold users account balance
            * deviceID (foreign key)
            * currentBalance
    """
        
    __dbname__ = "test_solarlink.db"
    __usertable__ = "users"
    __accounttable__ = "accounts"
    __messagetable__ = "messages"

    def __init__(self, dbname=None):
        if dbname:
            self.__dbname__ = dbname
        self.conn = sqlite3.connect(self.__dbname__)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.__usertable__} (
                Username TEXT,
                deviceID TEXT PRIMARY KEY,
                Node INTEGER,
                UserID TEXT
            );
            """)
            self.conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.__messagetable__} (
                DeviceID TEXT,
                state BOOLEAN,
                voltage FLOAT,
                current FLOAT,
                duration FLOAT,
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
        """ Add a new user to the database. If the user already exists, update the user"""
        with self.conn:
            duplicate = self.get_user(device_id)
            if duplicate:
                self.update_user(device_id, Username=username, Node=node, UserID=user_id)
                return
            self.conn.execute(f"""
            INSERT INTO {self.__usertable__} (Username, deviceID, Node, UserID)
            VALUES (?, ?, ?, ?)
            """, (username, device_id, node, user_id))

    def get_user(self, device_id=None):
        cursor = self.conn.cursor()

        if device_id is None:
            cursor.execute(f"""
            SELECT * FROM {self.__usertable__}
            """)
            return cursor.fetchall()
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

    def add_message(self, device_id, state, voltage, current, duration=0.0):
        with self.conn:
            self.conn.execute(f"""
            INSERT INTO {self.__messagetable__} (DeviceID, state, voltage, current, duration)
            VALUES (?, ?, ?, ?, ?)
            """, (device_id, state, voltage, current, duration))

    def get_messages(self, device_id):
        cursor = self.conn.cursor()
        cursor.execute(f"""
        SELECT * FROM {self.__messagetable__} WHERE DeviceID = ?
        ORDER BY time DESC
        """, (device_id,))
        return cursor.fetchall()
    
    def update_message(self, device_id, state, voltage, current, duration=0.0):
        with self.conn:
            self.conn.execute(f"""
            UPDATE {self.__messagetable__} SET state = ?, voltage = ?, current = ?, duration = ?
            WHERE DeviceID = ?
            """, (state, voltage, current, device_id, duration))

    def delete_message(self, device_id, num_messages=None):
        with self.conn:
            cursor = self.conn.cursor()
            
            if num_messages is None:
                # Delete all messages with the specified device_id
                cursor.execute(f"""
                DELETE FROM {self.__messagetable__} WHERE DeviceID = ?
                """, (device_id,))
            
            elif num_messages == 0:
                # Delete the most recent message with the specified device_id
                cursor.execute(f"""
                DELETE FROM {self.__messagetable__} WHERE rowid = (
                    SELECT rowid FROM {self.__messagetable__} 
                    WHERE DeviceID = ? 
                    ORDER BY time DESC 
                    LIMIT 1
                )
                """, (device_id,))
            
            else:
                # Delete the oldest N messages with the specified device_id
                cursor.execute(f"""
                SELECT rowid FROM {self.__messagetable__} 
                WHERE DeviceID = ? 
                ORDER BY time ASC
                """, (device_id,))
                
                rows = cursor.fetchall()
                if len(rows) >= num_messages:
                    row_ids_to_delete = tuple(row[0] for row in rows[:num_messages])
                    cursor.execute(f"""
                    DELETE FROM {self.__messagetable__} 
                    WHERE rowid IN ({','.join('?' for _ in row_ids_to_delete)})
                    """, row_ids_to_delete)

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
