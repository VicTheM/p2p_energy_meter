"""
THIS FILE SHOULD BE EXECUTED FOR EVERY NEW DB
IT MAY ALSO BE USED TO RESET THE CURRET DATABASE
"""
from dbClass import DBClient

# Data
userA = ["House_A", "001", 1, "1"]
userB = ["House_B", "002", 1, "2"]
userAaccount = ["001", 2000]
userBaccount = ["002", 70000]
userAmessage = ["001", 0, 0.0, 0.0, 0]
userBmessage = ["002", 0, 0.0, 0.0, 0]

def seed_database(reset=False):
	"""Create the demo records without resetting live data by default."""
	dbclient = DBClient()

	if reset:
		dbclient.delete_user(userA[1])
		dbclient.delete_user(userB[1])

	for user in (userA, userB):
		dbclient.add_user(*user)

	for account in (userAaccount, userBaccount):
		if dbclient.get_account_balance(account[0]) is None:
			dbclient.add_account(*account)

	for message in (userAmessage, userBmessage):
		if not dbclient.get_messages(message[0]):
			dbclient.add_message(*message)

	dbclient.disconnect()


if __name__ == "__main__":
	seed_database(reset=True)