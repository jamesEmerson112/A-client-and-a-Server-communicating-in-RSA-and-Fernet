# A client and a Server communicating in RSA and Fernet
 This project will be a working client server system where your clients will be accessing a database stored on the server. Clients will need to login as a specific # user and the server will only serve files that belong to the logged in user. You # must implement this system using Python

## Installation
**python**
This project mainly runs in Pthon; therefore, if using Windows, please follow this link to install [Python](https://www.python.org/downloads/)

**python packages**
The following packages are needed to be installed with [pip](https://www.python.org/downloads/) for this project: socket and Fernet
The following commands can be used to install the packages:
```
pip get install socket
pip get install fernet
```

## How to use
1. Please run myserver.py
```
py myserver.py
``` 
2. Please run parse.py
```
py parse.py
```

3. Commands: myserver will not do anything but responds to parse.py (client)
    - parse has 8 available commands
        - "login"         : login an account (admin default password is "admin")
        - "quit"          : quit the application
        - "adduser"       : add an user (only available for admin)
        - "invalid"       : return invalid message for invalid commands
        - "remove"        : remove an account
        - "changePass"    : change password
        - "help"          : display available commands
        - "upload"        : upload text entries for personal accounts
