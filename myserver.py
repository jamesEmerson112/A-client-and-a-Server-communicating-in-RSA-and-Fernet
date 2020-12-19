# implement removing user
# not adding duplicated user
import sys
import socket
from cryptography.fernet import Fernet
import userdb
# RSA


# ******* Connecting to host **************
# get a host name(IP address, localhost, or hostname), replaced this with your ip address
host = socket.gethostname()
print(host)
port = 8080                                  # Port number to receive requests from

# ******* Key *****************************
key = Fernet.generate_key()
codec = Fernet(key)
print("key ", key)

# initialize a socket object
s = socket.socket()
# Bind the hostname/IP and port number to the socket
s.bind((host, port))

# Listen for connections. Accept up to 1 client connection.
s. listen(1)
print("Waiting for client...")

"""
# accept incoming connection. Store client address/hostname in #
client_addr. Store client socket object in client_socket.
Username and password can be sent to the server using Fernet encryption. The server will decrypt
these and generate a hash to compare it to the user database
"""
client_socket, client_addr = s.accept()
# Connection accepted from client. Print client address.
print("Connection from ", str(client_addr))

# send a key from the server to the client when a connection is established
# ********* SENDING THE KEY
# client_socket.send(key)           # if RSA, disable this

# ******* RSA sending key procedure *********************************
# Determine is a number is prim
# input: a number
# output: true or false
def RSA_sending():
    # read private key
    # computing d
    with open('private.key', 'r') as input:
        private_key = input.read().splitlines()
        # print(public_key[0])
        # print(public_key[1])
        # The first line contains a number corresponding to the first number (n) of a public key pair
        n = int(private_key[0])
        # the second line contains a number corresponding to the second number (e) of a public key pair
        d = int(private_key[1])

    decrypted_key = key
    c = []
    # print(decrypted_message)
    for i in range(0, len(decrypted_key)):
        c.append(int((decrypted_key[i])))

    encrypted_number = []
    for i in range(0, len(c)):
        encrypted_number.append(pow(c[i], d, n))

    # rearrange the message
    message_list = []
    message = ""
    for i in range(0, len(encrypted_number)):
        message_list.append(str(encrypted_number[i]))
        message = ",".join(message_list)

    # this function is to encode the message to utf-8 then send to client


    def send_key(msg):
        msg = msg.encode('utf-8')
        # Echo data back to client after encoding it to utf-8
        client_socket.send(msg)


    # print(message)                        # for debugging.  Comparing the key with the client
    send_key(message)                       # send key to the client

# print(message)
# ********************************************** END OF RSA

# ************************** global variables
current_user = ""

# ************************** choice
# input: nothing
# output: return a username if it is a successful login
# login
def login():
    """
    log in
    """
    global current_user
    print("global current_user = ", current_user)
    """
    if current_user == "":
        msg = "Enter Login Information..."
        send_encrypted_msg(msg)
    else:
        msg = "Already logged in as " + current_user
        send_encrypted_msg(msg)
        main()
    """
    current_user = ""
    # receive username
    username = received_and_decrypt()
    # Print the received data
    print("client> username is ", username)
    send_encrypted_msg(username)

    # receive password and not returning an answer to the client
    password = client_socket.recv(1024)
    password = codec.decrypt(password).decode('utf-8')
    print("received pass is ", password)
    returned_user = userdb.login(username, password)

    if returned_user == username:
        msg = "Logged In Successfully!"
        current_user = returned_user
        print(msg)
        send_encrypted_msg(msg)
    else:
        msg = "Username or Password Incorrect!"
        print(msg)
        send_encrypted_msg(msg)
    main()

# adduser
def adduser():
    """
    docstring
    """
    global current_user

    # Or let the server decide if the function is valid or not.
    # The server knows if your user is an admin
    # The client can be hacked. So server should double check
    if current_user == "admin":
        send_encrypted_msg(current_user)
    else:  # if not admin
        blank_msg = ""
        send_encrypted_msg(blank_msg)
        main()

    print("starting addUser")
    # username
    username = received_and_decrypt()
    # if new user is another admin, say no
    if username == "admin":
        msg = "Adding another admin is not allowed"
        send_encrypted_msg(msg)
        main()

    # Print the received data
    print("client> new user is ", username)
    send_encrypted_msg(username)

    # password
    password = client_socket.recv(1024)
    password = codec.decrypt(password).decode('utf-8')
    print("received pass is ", password)

    # re-enter the password
    password2 = client_socket.recv(1024)
    password2 = codec.decrypt(password2).decode('utf-8')
    print("received pass is ", password2)
    
    if password == password2:
        username = userdb.addUser(username, password)
        msg = "New user is added: username " + username
        send_encrypted_msg(msg)
    else:
        msg = "Passwords are not matching. Abort the opeartion"
        send_encrypted_msg(msg)
    
    main()

# removeUser()
def removeUser():
    """
    remove user
    """
    # if the user is not admin, user can't remove anybody else
    if current_user == "admin":
        send_encrypted_msg(current_user)
    else:
        msg = "Only admin can remove users"
        print(msg)
        send_encrypted_msg(msg)
        main()

    # receive removed_username
    removed_username = received_and_decrypt()

    # if removed_username is admin, admin must exist
    if removed_username == current_user:
        msg = "Admin must exist! Admin can't be removed!"
        print(msg)
        send_encrypted_msg(msg)
        main()
                
    # Print the received data
    print("client> Removing user ", removed_username)
    send_encrypted_msg(removed_username)

    returned_username = userdb.removeUser(removed_username)

    if returned_username != removed_username:
        msg = "Removing unsuccessfully!"
        print(msg)
        send_encrypted_msg(msg)
    else:
        msg = "Removing " + returned_username + " unsuccessfully!"
        print(msg)
        send_encrypted_msg(msg)    
    main()

# upload
def upload():
    while True:
        msg = received_and_decrypt()
        if msg != "quit":
            userdb.upload(current_user, msg)
        else:
            break
    main()
# changePass()
def changePass():
    # receive current_user
    current_user = received_and_decrypt()
                
    # Print the received data
    print("client> Changing password for ", current_user)

    new_password = received_and_decrypt()
    print("New password is ", new_password)

    userdb.changePassword(current_user, new_password)

    msg = "Changing password successfully!"
    print(msg)
    send_encrypted_msg(msg)

    main()
"""
receive and send functions
"""

def received_and_decrypt():
    # Receive data from client and decode it to utf-8
    data = client_socket.recv(1024)
    # print(data)

    decrypt_message = codec.decrypt(data).decode('utf-8')
    print("decrypt_message = ", decrypt_message)
    #encrypted_message = codec.encrypt(decrypt_message.encode('utf-8'))
    return decrypt_message


def send_encrypted_msg(msg):
    decrypt_message = msg
    #print("test =",decrypt_message)
    encrypted_message = codec.encrypt(decrypt_message.encode('utf-8'))
    #print("encrypted_message ", encrypted_message)
    # Echo data back to client after encoding it to utf-8
    client_socket.send(encrypted_message)
    # print("test ", decrypt_message)
    # client_socket.send(data.encode('utf-8'))                        # Echo data back to client after encoding it to utf-8

# ******** receive msg and decrypt it


# quit
def quit():
    print("choice: quit")
    client_socket.close()


# main
def main():
    decrypt_message = ""
    while True:
        # Receive data from client and decode it to utf-8
        data = client_socket.recv(1024)
        #print("Received {} bytes from client.".format(len(data)))

        # ************************* reading inputs and responding
        if len(data) > 0:
            # *************************** rendering choices
            decrypt_message = codec.decrypt(data).decode('utf-8')
            # Print the received data
            print("client> ", decrypt_message)
            # encrypt messages from server then sendF
            #msg_from_server = codec.encrypt(decrypt_message.encode('utf-8'))
            # client_socket.send(decrypt_message.encode('utf-8'))                        # Echo data back to client after encoding it to utf-8

            if decrypt_message == "choice: login":
                login()
            elif decrypt_message == "choice: adduser":
                adduser()
            elif decrypt_message == "choice: remove":
                removeUser()
            elif decrypt_message == "choice: quit":
                decrypt_message = ""
            elif decrypt_message == "choice: changePass":
                changePass()
            elif decrypt_message == "choice: upload":
                upload()            
            else:
                decrypt_message = ""

            # ************************* closing connection
            # If client connection is closed, data received is 0 bytes.
        if not decrypt_message:
            print("client connection is closed")
            break
    # Close the socket
    client_socket.close()
    sys.exit()

RSA_sending()
main()
