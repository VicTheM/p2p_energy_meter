"""
THIS FILE SHOULD BE EXECUTED FOR EVERY NEW DB
"""
from dbClass import DBClient

userA = ["House_A", "001", 1, "1"]
userB = ["House_B", "002", 1, "2"]

userAaccount = ["001", 3500]
userBaccount = ["002", 5000]

dbclient = DBClient()

dbclient.add_user(*userA)
dbclient.add_user(*userB)
dbclient.add_account(*userAaccount)
dbclient.add_account(*userBaccount)

print(dbclient.get_user())
print(dbclient.get_account_balance(userAaccount[0])[0])
print(dbclient.get_account_balance(userBaccount[0])[0])
dbclient.disconnect()