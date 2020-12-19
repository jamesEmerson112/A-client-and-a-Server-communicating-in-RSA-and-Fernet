# An Thien Vo, CS 448, Final project
# You final project will be a working client server system where your clients will be
# accessing a database stored on the server. Clients will need to login as a specific
# user and the server will only serve files that belong to the logged in user. You
# must implement this system using Python. The requirements for this project are
# given below.

import sys
from getpass import getpass

'''
1 Server - Client System
Implement a server system that clients can connect to. Also implement client code that connects to
your server. You may hard code the server’s port and IP address in your client code if you wish. Refer
to the socket programming example provided on Canvas if you need help. All communication must
be done using socket programming in Python. Optionally, if you have multiple computers available
to you on the same network, you could test your server and client system on separate computers.

'''
import socket
from cryptography.fernet import Fernet

current_user = ""
admin_identifier = ""

host = socket.gethostname()     # Server hostname or IP addresses
port = 8080                     # Server port to connect to.

s = socket.socket()             # initialize a socket object
s.connect((host, port))         # Use socket object to connect to server

# receiving the key  DISABLE THIS WHEN USING RSA
#key = s.recv(1024)
#print("key = ", key)
#codec = Fernet(key)

# *************** RSA receiving
# This function receives a Fernet key from server encrypted in RSA
# Input: n/a
# Output: codec = Fernet(key)
def RSA_receiving():
    # This function determines whether a number is prime
    # Input: a number
    # Output: True or False
    def is_prime(n):
        if n == 2 or n == 3:
            return True
        if n < 2 or n % 2 == 0:
            return False
        if n < 9:
            return True
        if n % 3 == 0:
            return False
        r = int(n**0.5)
        # since all primes > 3 are of the form 6n ± 1
        # start with f=5 (which is prime)
        # and test f, f+2 for being prime
        # then loop by 6.
        f = 5
        while f <= r:
            # print('\t',f)
            if n % f == 0:
                return False
            if n % (f+2) == 0:
                return False
            f += 6
        return True

    # Returns mod multiplicative inverse of a number using the Euclidean method.
    # input: 2 numbers
    # output: mod mult inverse
    def modInverse(a, m):
        def egcd(a, b):
            if a == 0:
                return (b, 0, 1)
            else:
                g, y, x = egcd(b % a, a)
                return (g, x - (b // a) * y, y)
        g, x, y = egcd(a, m)
        if g != 1:
            raise Exception('modular inverse does not exist')
        else:
            return x % m

    # computing Greatest Common Divisor
    # input: 2 numbers
    # output: greatest common divisor
    def compute_gcd(x, y):
        while(y):
            x, y = y, x % y
        return x


    # computing Greatest Common Divisor
    # input: 2 numbers  
    # output: least common divisor  
    def compute_lcm(x, y):
        lcm = (x*y)//compute_gcd(x, y)
        return lcm

    # read input files
    key_message_received = s.recv(1024).decode('utf-8')
    # print("key_message_received = ", key_message_received)            # for debugging
    encrypted_message = (key_message_received.split(","))
    # convert encrypted_messages string to int
    for i in range(0, len(encrypted_message)):
        encrypted_message[i] = int(encrypted_message[i])

    # print(encrypted_message)
    with open('public.key', 'r') as input_data:
        public_key = input_data.read().splitlines()
        # print(public_key[0])
        # print(public_key[1])
        # The first line contains a number corresponding to the first number (n) of a public key pair
        n = int(public_key[0])
        # the second line contains a number corresponding to the second number (e) of a public key pair
        e = int(public_key[1])

    # decrypting messages
    # input: encrypted number
    # output: decrypted number
    def decrypt(c):
        # Decrypt c using m≡c^d(mod n).
        c = pow(c, e, n)
        #print("c =", c)
        return c

    # print(encrypted_message)
    message_list = []
    message = ""
    # encrypted_message = [49,50,51]
    for e_c in encrypted_message:
        #print("e_c", e_c)
        c = decrypt(e_c)
        # convert number c to character
        c = chr(c)
        #print("c", c)
        message_list.append(c)
        message = "".join(message_list)

    key = message
    key = key.encode('utf-8')
    codec = Fernet(key)

# ************************************************

# server_socket, server_addr = s.accept()
# ******************** database


# ******************** parsing the command line
# input: string
# output: function
def parser(query):
    query_args = query.split(" ")
    print("Query split: ", query_args)
    dispatcher = {
        "login"         : login,
        "quit"          : quitApp,
        "adduser"       : addUser,
        "invalid"       : invalid,
        "remove"        : remove,
        "changePass"    : changePass,
        "help"          : help,
        "upload"        : upload
    }
    dispatch = dispatcher.get(query_args[0], invalid)
    dispatch(query_args)

# ******************** upload, user uploads their text entires
def upload(args):
    if current_user == "":
        print("Please login firstly")
        main()

    if len(args) <= 2:
        choice = "choice: upload"
        send_msg_to_server_and_server_responds(choice)
    else:
        invalid(args)    

    while True:
        data_entry = input("Please enter your data entry. Type \"quit\" to stop \n")
        # send 1
        send_msg_to_server_and_server_responds(data_entry)
        if data_entry == "quit":
            break  
    main()      


# ******************** help, displaying possible commands
def help(args):
    dispatcher = ["login", "quit", "adduser", "invalid", 
    "remove", "changePass", "help", "upload"]
    print("Available commands are: ")
    print(dispatcher)

# ******************** remove accout
def remove(args):
    if current_user != "admin":
        print("client is not admin. Please log in as admin")
        return

    # send commands of choice
    if len(args) <= 2:
        choice = "choice: remove"
        send_msg_to_server_and_server_responds(choice)
    else:
        invalid(args)

    # waiting for a respond to verify that the current user is
    is_current_user_admin_on_server = msg_received()
    if is_current_user_admin_on_server != current_user:
        print("Server says the client is not admin")
        return
    # if received message says "yes, you can add an user", then addUser, else invalid
    if len(args) == 1:
        # username
        username = input("Please enter the removed username: ")
        send_msg_to_server_and_server_responds(username)
        # if the user is admin, deny this functionality
        if username == "admin":
            msg_received()      # receive warning from server
            main()              # end the function and go back to main
        # receiving response
        msg_received()

        # receiving the result
        msg_received()

    elif len(args) == 2:
        username = args[1]
        send_msg_to_server_and_server_responds(username)
        # if the user is admin, deny this functionality
        if username == "admin":
            msg_received()      # receive warning from server
            main()              # end the function and go back to main
        # receiving response
        msg_received()

        # receiving the result
        msg_received()
    else:
        invalid(args)
    

# ******************** change password
def changePass(args):
    global current_user
    if current_user == "":
        print("Please login firstly")
        main()

    if len(args) <= 1:
        choice = "choice: changePass"
        send_msg_to_server_and_server_responds(choice)
    else:
        invalid(args)

    send_msg_to_server_and_server_responds(current_user)
    if len(args) == 1:
        # re-enter the user
        # password
        password2 = getpass(
            prompt="Please the new password: ", stream=None)

        password3 = getpass(
            prompt="Please re-enter the new password: ", stream=None)

        if password2 != password3:
            print("New passwords are unmatched!")
            main()
        else:
            # Receive results from the server
            send_msg_to_server_and_server_responds(password2)
            msg_received()
    else:
        invalid(args)

# ******************** log in
def login(args):
    global current_user
    if len(args) <= 2:
        choice = "choice: login"
        send_msg_to_server_and_server_responds(choice)
    else:
        invalid(args)

    if len(args) == 1:          # login
        # ******************* starting logging in
        print("Enter Login Information...")
        # msg_received()
        username = input("Username: ")
        send_msg_to_server_and_server_responds(username)
        msg_received()
        # password = input("Password: ")
        password = getpass(prompt="Password: ", stream=None)
        send_msg_to_server_and_server_responds(password)
        # msg_received()
        testing = msg_received()
        if testing == "Logged In Successfully!":
            current_user = username
            print("current_user is", current_user)

    elif len(args) == 2:        # login username
        # ******************* starting logging in
        print("Enter Login Information...")
        # msg_received()
        username = args[1]
        send_msg_to_server_and_server_responds(username)
        msg_received()
        # password = input("Password: ")
        password = getpass(prompt="Password: ", stream=None)
        send_msg_to_server_and_server_responds(password)
        testing = msg_received()
        if testing == "Logged In Successfully!":
            current_user = username
            print("current_user is", current_user)
    else:
        invalid(args)


# ******************** quit app
def quitApp(args):
    s.close()
    sys.exit()

# ******************** add users
# 3.2	Adding users should be restricted for the clients. You may either implement
# an administrator based system which allows clients to login to an administrator
# account to add users
def addUser(args):
    if current_user != "admin":
        print("client is not admin. Please log in as admin")
        return

    if len(args) <= 2:
        choice = "choice: adduser"
        send_msg_to_server_and_server_responds(choice)
        is_current_user_admin_on_server = msg_received()
    else:
        invalid(args)
    if is_current_user_admin_on_server != current_user:
        print("Server says the client is not admin")
        return
    # if received message says "yes, you can add an user", then addUser, else invalid
    if len(args) == 1:
        # username
        username = input("Please enter a new username: ")
        send_msg_to_server_and_server_responds(username)
        # if the user is admin, deny this functionality
        if username == "admin":
            msg_received()      # receive warning from server
            main()              # end the function and go back to main
        msg_received()
        # password
        password = getpass(prompt="Password: ", stream=None)
        send_msg_to_server_and_server_responds(password)
        # msg_received()

        # re-enter the user
        # password
        password2 = getpass(
            prompt="Please re-enter the password: ", stream=None)
        send_msg_to_server_and_server_responds(password2)
        # msg_received()

        # Receive results from the server
        msg_received()

    elif len(args) == 2:
        username = args[1]
        send_msg_to_server_and_server_responds(username)
        # if the user is admin, deny this functionality
        if username == "admin":
            msg_received()      # receive warning from server
            main()              # end the function and go back to main
        msg_received()
        # password
        password = getpass(prompt="Password: ", stream=None)
        send_msg_to_server_and_server_responds(password)
        
        # msg_received()

        # re-enter the user
        # password
        password2 = getpass(
            prompt="Please re-enter the password: ", stream=None)
        send_msg_to_server_and_server_responds(password2)
        # msg_received()

        # Receive results from the server
        msg_received()
    else:
        invalid(args)

# ******************** invalid commands
def invalid(args):
    print("Unrecognized command.")
    main()

# ******************** sending inputs to the server
def send_msg_to_server_and_server_responds(data):
    msg = data
    # **************** you may either encrypt every message using Fernet cryptography for communicaiton
    encrypted_msg = codec.encrypt(msg.encode('utf-8'))
    # print("encrypted_msg =", encrypted_msg)
    # Encode message to utf-8 and send to server
    s.send(encrypted_msg)
    # daat is the encrypted message received from the server

def msg_received():
    msg_received = s.recv(1024)
    # print("msg_received = ", msg_received)        # s.recv(1024) generates b'message'
    decrypt_message = codec.decrypt(msg_received).decode('utf-8')
    print("Server says: ", decrypt_message)# Receive message from server and decode it before printing   
    return decrypt_message


# ******************** running the program
def main():
    query = ""
    while (True):
        query = input("client> ")
        parser(query)
        # Close socket

RSA_receiving()
main()
