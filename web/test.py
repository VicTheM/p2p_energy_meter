"""
This file takes us through a tutorial of using the Python in-built db
"""
import sqlite3
from dbClass import DBClient

client = DBClient()
client.create_tables()

# Test inserting same user multiple times
client.add_user("a", 7, 0, 7)
client.add_user("a", 4, 0, 4)
client.add_user("b", 5, 0, 5)
client.add_user("a", 6, 0, 6)


users = client.get_user()
for user in users:
    print(user)

# con = sqlite3.connect("test_solarlink.db")
# cur = con.cursor()

# with con:
#     all = con.execute("SELECT * FROM users WHERE  deviceID = 5 OR UserID = 5")
#     duplicate = all.fetchone()

#     if duplicate[1] == '5':
#         print(f"deviceid: {duplicate[1]}")