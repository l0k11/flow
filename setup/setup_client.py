import pathlib, platform, os, shutil
import getpass, hashlib
import sqlite3, uuid
import socket
import utilities.encryption as encryption

def db_prepare(file):
    pathlib.Path(file).touch()
    with sqlite3.connect(file) as con:
        try:
            con.execute("""CREATE TABLE conversations (
                conversation_id CHAR(36) PRIMARY KEY,
                conversation_name VARCHAR(255) 
            );""")

            con.execute("""CREATE TABLE contacts (
                contact_id CHAR(36) PRIMARY KEY,
                contact_name VARCHAR(255)
            );""")

            con.execute("INSERT INTO contacts VALUES (?,?)", (str(uuid.uuid4()), "SUPER UNIQUE CONTACT NAME THAT WILL NOT BE DISPLAYED"))
        except:
            con.close()
            raise Exception(f"Cannot find to {file}")

def check_keys(root):
    if os.path.exists(f"{root}public.key") and os.path.exists(f"{root}private.key"):
        return True
    else:
        return False

def setup():
    root_win = f"{pathlib.Path.home()}\\.flow\\"
    root_other = f"{pathlib.Path.home()}/.flow/"

    passwd_win = f"{root_win}passwd"
    passwd_other = f"{root_other}passwd"

    db_win = f"{root_win}.db"
    db_other = f"{root_other}.db"

    if platform.system() == "Windows": 
        os.system("cls")
        print("Welcome to flow, your local chat app!")
        print("")
        root = root_win
        
        if os.path.exists(root_win) and os.path.exists(passwd_win) and os.path.exists(db_win) and check_keys(root_win):
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
                    os.chmod(passwd_win, 0o444)

                    password = hashlib.md5(password1.encode()).hexdigest()

                    with open(passwd_win, "w") as file:
                        file.write("DO NOT MODIFY THIS FILE\n")
                        file.write(password)

                if not os.path.exists(db_win):
                    pathlib.Path(db_win).touch()
                    db_prepare(db_win)

                if not check_keys(root_win):
                    encryption.generate_keys(root_win)

                print("flow successfully installed!")
            except:
                shutil.rmtree(root_win)
                print("Error while installing flow.")
                exit(1)

    else:
        try:
            os.system("clear")
            print("Welcome to flow, your local chat app!")
            print("")
            root = root_other
            
            if os.path.exists(root_other) and os.path.exists(passwd_other) and os.path.exists(db_other) and check_keys(root_win):
                passwd = open(passwd_other).readlines()[1]
                passwd_in = getpass.getpass("Type your password: ")

                while passwd != hashlib.md5(passwd_in.encode()).hexdigest():
                    print("")
                    print("Incorrect password")
                    passwd_in = getpass.getpass("Type your password: ")
            
            else:
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
                        file.write("¡¡DO NOT MODIFY THIS FILE!!\n")
                        file.write(password)
                    os.chmod(passwd_other, 0o444)

                if not os.path.exists(db_other):
                    pathlib.Path(db_other).touch()
                    db_prepare(db_other)

                if not check_keys(root_other):
                    encryption.generate_keys(root_other)

                print("flow successfully installed!")
        except:
            shutil.rmtree(root_other)
            print("Error while installing flow.")
            exit(1)

    print("")
    print("Now provide the IP address of the server in your local network")
    while True:
        ip = input("Type the IP address: ")
        try:
            con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            con.connect((ip, 6002))
            con.close()

            con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            con.connect((ip, 6003))
            con.close()
            print(f"Successfully connected to {ip}. Have a nice chatting!")
            
            return {
                "ip": ip,
                "root": root
            }
        except:
            print(f"Server in {ip} unavailable")

#setup()