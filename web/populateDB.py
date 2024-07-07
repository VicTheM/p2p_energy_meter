"""
THIS FILE SHOULD BE EXECUTED FOR EVERY NEW DB
"""
from dbClass import DBClient

# Data
userA = ["House_A", "001", 1, "1"]
userB = ["House_B", "002", 1, "2"]
userAaccount = ["001", 2000]
userBaccount = ["002", 5000]
userAmessage = ["001", 0, 0.0, 0.0, 0]
userBmessage = ["002", 0, 0.0, 0.0, 0]

# set up
dbclient = DBClient()
dbclient.delete_user(userA[1])
dbclient.delete_user(userB[1])

# populate DB
dbclient.add_user(*userA)
dbclient.add_user(*userB)
dbclient.add_account(*userAaccount)
dbclient.add_account(*userBaccount)

# not to be added
dbclient.add_message(*userAmessage)
dbclient.add_message(*userBmessage)

# Visualize change
print(dbclient.get_user())
print(dbclient.get_account_balance(userAaccount[0])[0])
print(dbclient.get_account_balance(userBaccount[0])[0])
print(dbclient.get_messages("001"))
print(dbclient.get_messages("002"))

dbclient.disconnect()