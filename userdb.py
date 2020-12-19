# An Thien Vo, 2000727514, CS 448, Assignment 5
'''Communications facility #7823 was last decommissioned on April 15, 2020. The pandemic at large
prevented any on-site access causing the entire system to be taken offline and a new internet login
portal to be implemented. Some of the magnetic disks used to implement this system have been
corrupted by the experimental electromagnetic shockwave that was fired five years ago to unsuccessfully eradicate the coronavirus. This facility needs to be brought back online but with remote
login capabilities. This means that the old login system must be entirely revamped to include better security and user management. All repairs and improvements to be made are detailed in this
document.'''

import hashlib
import csv
import secrets
from getpass import getpass

filename = "user_db.csv"

# 4. add an user
def addUser(username, password):
    #salt = secrets.token_hex(4)
    # 1. prompt for username
    username = username

    # 2. Prompt for a password. Must not be visible
    password = password

    # 3. Prompt to re-enter the password. The password must not be visible on screen.
    re_enter_password = password

    # 4. If the first entered password and re are incorrect, abort the operation
    # Otherwise, proceed to the next step
    #if(re_enter_password != password):
    #    print("Passwords are not matching. Abort the opeartion")
    #    return -1
    # THIS STEP IS MOVED TO MYSERVER TO HANDLE
    
    # 5. Generate a random salt using the secrets package
    salt = secrets.token_hex(4)

    # 6. generate a sha256 has using the input string given in 3.3
    input_string = username + password + salt
    hash_password = hashlib.sha256(input_string.encode()).hexdigest()
    
    # transfer data from the csv file into a list
    try:
        with open(filename, newline='') as f:
            csv_file = csv.reader(f)
            data = list(csv_file)
    except:
        print ("ERROR: Unable to open file ", filename)
        return ""            

    # append the user
    data.append([username,hash_password,salt])
    
    # plug in the list data into the file
    with open(filename, "w", newline ='') as f:
        csv_file = csv.writer(f)
        csv_file.writerows(data)
    
    return username


# 1. login
def login(username, password):
    print(filename)
    db_row = False
    try:
        with open(filename, newline='') as db:
            csv_reader = csv.reader(db)
            for row in csv_reader:
                if username == row[0]: 
                    db_row = row
    except:
        print ("ERROR: Unable to open file ", filename)
        return -1
    if not db_row: return ""

    # if db_row has salt
    if (len(db_row) == 3):
        salt = db_row[2]
        input_string = username + password + salt
        hash_password = hashlib.sha256(input_string.encode()).hexdigest()
    else:
        hash_password = password

    if (db_row[1] == hash_password): 
        #print ("Logged into", username)
        return username
    else: return ""

# 3. change a password
def changePassword(username, password):
    # 1. copy entire user database into a list
    try:
        with open(filename, newline='') as f:
            csv_file = csv.reader(f)
            data = list(csv_file)
    except:
        print ("ERROR: Unable to open file ", filename)
        return -1  

    # 2. Promt user for their current password
    password = password
    
    # 8. Generate a new salt and use this salt to generate a new hash for the user
    salt = secrets.token_hex(4)
    input_string=username+password+salt
    new_hash_password = hashlib.sha256(input_string.encode()).hexdigest()

    # 9. replace
    for row in data:
        if username == row[0]: 
            row[1] = new_hash_password
            if len(row) == 3:
                row[2] = salt # new salt
            else:
                row.append(salt)

    # 10. write this list to the database file replacing all contents
    with open(filename, "w", newline ='') as f:
        csv_file = csv.writer(f)
        csv_file.writerows(data)

    print("\n")
    return True

# 5. list all accounts
def listAll():
    usernames = []
    try:
        with open(filename, newline='') as db:
            csv_reader = csv.reader(db)
            for row in csv_reader:
                #print(row[0])
                usernames.append(row[0])
    except:
        print ("ERROR: Unable to open file ", filename)
        return -1
    for username in usernames:
        print(username)
    print("Total Users: {}".format(len(usernames)))
    return -1

# 6. remove an user
# return "admin", "", removed_username
# if admin, nothing is done
# if "", nothing is done
# if removed_username, user is removed
def removeUser(removed_username):
    removed_username = removed_username
    # open file and check
    if removed_username == "admin" or removed_username == "":
        return removed_username

    db_row = False
    try:
        with open(filename, newline='') as db:
            csv_file = csv.reader(db)
            data = list(csv_file)
            for row in data:
                if removed_username == row[0]: 
                    db_row = row
    except:
        print ("ERROR: Unable to open file ", filename)
        return -1
    if not db_row: return ""
    
    data.remove(db_row)

    with open(filename, "w", newline ='') as f:
        csv_file = csv.writer(f)
        csv_file.writerows(data)
    return removed_username

# 7. Upload
def upload(username, msg):
    current_user = username
    user_file = current_user + ".csv"

    try:
        with open(user_file, newline='') as f:
            csv_file = csv.reader(f)
            data = list(csv_file)
    except:
        print ("ERROR: Unable to open file ", filename)
        data = []       
    data.append([msg])

    with open(user_file, "w", newline ='') as f:
        csv_file = csv.writer(f)
        csv_file.writerows(data)    