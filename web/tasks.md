### Things to do

- change the green buttons to toggle able buttons
- if user with deviceID 001 chooses to send respond by refusing to toggle and alert "nobody is currentlty sending"
- if user with device ID 002 tries to do anything, alert by saying "device is offline. only crediting his account is allowed
- Users with any other ID will be denied access to the dashboard
- rephrase the html like "share" for "send"
- As user 001 device is sharing keep adding to his account on the db, and while the "sharing" button is active, show a green plus oin the account balance to show it is increasing
- since the esp32 pushes data every 3 second, in the api implement a filter that checks if the difference between the time the message was added and the current time is greater than 10 seconds
if it is, then send a signal to the frontend ie: state should be "offline"