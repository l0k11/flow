import pathlib, platform, os, shutil
import getpass, hashlib
import sqlite3, uuid
import socket

def db_prepare(file):
    pathlib.Path(file).touch()
    with sqlite3.connect(file) as con:
        try:
            con.execute("""CREATE TABLE conversations (
                conversation_id CHAR(36) PRIMARY KEY,
                conversation_name VARCHAR(255) 
            );""")

            con.execute("""CREATE TABLE users (
                user_id CHAR(36) PRIMARY KEY,
                user_ip VARCHAR(255)
            );""")
            
            con.execute("""CREATE TABLE messages (
                message_id CHAR(36) PRIMARY KEY,
                conversation_id CHAR(36),
                user_id CHAR(36),
                message_text VARCHAR(1000),
                message_timestamp DATETIME,
                FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );""")

        except:
            con.close()
            raise Exception(f"Cannot find to {file}")

def setup():
    root_win = f"{pathlib.Path.home()}\\.flow-server"
    # root_win = "C:\\Users\\Luis\\OneDrive\\Documentos\\ASIR\\2º\\TFG\\flow-server"
    root_other = f"{pathlib.Path.home()}/.flow-server"

    passwd_win = f"{root_win}\\passwd"
    passwd_other = f"{root_other}/passwd"

    db_win = f"{root_win}\\.db"
    db_other = f"{root_other}/.db"

    keys_win = f"{root_win}\\client_keys"
    keys_other = f"{root_other}/client_keys"

    if platform.system() == "Windows":
        os.system("cls")
        print("Welcome to flow, your local chat app!")
        print("")
        
        if os.path.exists(root_win) and os.path.exists(passwd_win) and os.path.exists(db_win) and os.path.exists(keys_win):
            passwd = open(passwd_win).readlines()[1]
            passwd_in = getpass.getpass("Type your password: ")

            while passwd != hashlib.md5(passwd_in.encode()).hexdigest():
                print("")
                print("Incorrect password")
                passwd_in = getpass.getpass("Type your password: ")
        
        else:
            try:
                if not os.path.exists(root_win):
                    os.mkdir(root_win)

                if not os.path.exists(passwd_win):
                    print("Please provide a secure password that will be use every time you start the app")
                    password1 = getpass.getpass("Password: ")
                    password2 = getpass.getpass("Repeat the password: ")
                    while password1 != password2:
                        print("Passwords do not match")
                        password1 = getpass.getpass("Password: ")
                        password2 = getpass.getpass("Repeat the password: ")

                    password = hashlib.md5(password1.encode()).hexdigest()

                    with open(passwd_win, "w") as file:
                        file.write("DO NOT MODIFY THIS FILE\n")
                        file.write(password)

                if not os.path.exists(db_win):
                    pathlib.Path(db_win).touch()
                    db_prepare(db_win)

                if not os.path.exists(keys_win):
                    os.mkdir(keys_win)

                print("flow successfully installed!")
            except:
                shutil.rmtree(root_win)
                print("Error while installing flow.")
                exit(1)

    else:
        os.system("clear")
        print("Welcome to flow, your local chat app!")
        print("")
        
        if os.path.exists(root_other) and os.path.exists(passwd_other) and os.path.exists(db_other) and os.path.exists(keys_other):
            password = input("Type the password: ")
        
        else:
            try:
                if not os.path.exists(root_other):
                    os.mkdir(root_other)

                if not os.path.exists(passwd_other):
                    print("Please provide a secure password that will be use every time you start the app")
                    password1 = getpass.getpass("Password: ")
                    password2 = getpass.getpass("Repeat the password: ")
                    while password1 != password2:
                        print("Passwords do not match")
                        password1 = getpass.getpass("Password: ")
                        password2 = getpass.getpass("Repeat the password: ")

                    password = hashlib.md5(password1.encode()).hexdigest()

                    with open(passwd_other, "w") as file:
                        file.write("# DO NOT MODIFY THIS FILE\n")
                        file.write(password)
                    os.chmod(passwd_other, 0o444)

                if not os.path.exists(db_other):
                    pathlib.Path(db_other).touch()
                    db_prepare(db_other)

                if not os.path.exists(keys_other):
                    os.mkdir(keys_other)

                print("flow successfully installed!")
            except:
                shutil.rmtree(root_win)
                print("Error while installing flow.")
                exit(1)

    print("")

setup()