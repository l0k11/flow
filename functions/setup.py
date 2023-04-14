import os, sqlite3, pathlib, getpass, hashlib, socket, shutil,\
    functions.encryption as encryption,\
    functions.conection as con,\
    functions.other as other

def server_db_prepare(file):
    open(file, "w")
    with sqlite3.connect(file) as con:
        try:
            con.execute("""CREATE TABLE conversations (
                id CHAR(37) PRIMARY KEY,
                name VARCHAR(255) 
            );""")

            con.execute("""CREATE TABLE users (
                id CHAR(37) PRIMARY KEY,
                ip VARCHAR(255),
                status VARCHAR(255)
            );""")
            
            con.execute("""CREATE TABLE messages (
                id CHAR(37) PRIMARY KEY,
                conversation_id CHAR(37),
                user_id CHAR(37),
                content VARCHAR(4096),
                timestamp VARCHAR(255),
                FOREIGN KEY (conversation_id) REFERENCES conversations(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            );""")
        except:
            con.close()
            raise Exception(f"Cannot find {file}")

def client_db_prepare(file):
    open(file, "w")
    with sqlite3.connect(file) as con:
        try:
            con.execute("""CREATE TABLE conversations (
                id CHAR(37) PRIMARY KEY,
                name VARCHAR(255) 
            );""")

            con.execute("""CREATE TABLE contacts (
                id CHAR(37) PRIMARY KEY,
                name VARCHAR(255)
            );""")
        except:
            con.close()
            raise Exception(f"Cannot find {file}")

def check_files(root, passwd, db, public, private):
    root_e = True if os.path.exists(root) else False
    keys = True if os.path.exists(public) and os.path.exists(private) else False
    passwd = True if os.path.exists(passwd) else False
    db = True if os.path.exists(db) else False
    return {
        "root": root_e,
        "keys": keys,
        "passwd": passwd,
        "db": db
    }

def check_password(passwd_file):
    passwd = open(passwd_file).readlines()[1]
    passwd_in = getpass.getpass("Password: ")

    while passwd != hashlib.md5(passwd_in.encode()).hexdigest():
        print("")
        print("Incorrect password")
        passwd_in = getpass.getpass("Type your password: ")

def create_password(passwd_file):
    print("Please provide a secure password that will be use every time you start the app")
    password1 = getpass.getpass("Password: ")
    password2 = getpass.getpass("Repeat the password: ")
    while password1 != password2:
        print("Passwords do not match")
        password1 = getpass.getpass("Password: ")
        password2 = getpass.getpass("Repeat the password: ")

    password = hashlib.md5(password1.encode()).hexdigest()
    with open(passwd_file, "w") as file:
        file.write("DO NOT MODIFY THIS FILE\n")
        file.write(password)
    os.chmod(passwd_file, 0o444)

def test_conection(ip: str, ports: list):
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as con:
            test = con.connect_ex((ip, port))
            if test: return False
        return ip

def execute_db_command(db, command, args : tuple = None):
    with sqlite3.connect(db) as con:
        try: 
            command = con.execute(command, args) if args else con.execute(command)
            return command
        except Exception as e:
            con.close()
            raise e
        
def client_setup():
    root = f"{pathlib.Path.home()}/.flow/"
    passwd_file = f"{root}passwd"
    db_file = f"{root}.db"
    public = f"{root}public.key"
    private = f"{root}private.key"

    check = check_files(root, passwd_file, db_file, public, private)
    if not all(valor == True for valor in check.values()):
        try:
            if not check["root"]: os.mkdir(root)
            if not check["keys"]: encryption.generate_keys(root)
            if not check["passwd"]: create_password(passwd_file)
            if not check["db"]: client_db_prepare(db_file)
        except Exception as e:
            try: shutil.rmtree(root)
            finally: raise e    
    
    other.clear_console()
    print("Type your password to access flow.")
    check_password(passwd_file)

    print("Now provide the IP address of the server in your local network")
    while True:
        server_ip = input("Type the IP address: ")
        if test_conection(server_ip, [6002, 6003]):
            print(f"Successfully connected to {server_ip}. Have a nice chatting!")
            break
        else: print(f"{server_ip} is not a valid server.")

    user_id = con.generate_id(server_ip, "user")
    execute_db_command(
        db_file,
        "INSERT INTO contacts VALUES (?,?)",
        (user_id, "SUPER UNIQUE CONTACT NAME THAT WILL NOT BE DISPLAYED")
    )
    other.clear_console()
    return {
        "server": server_ip,
        "root": root
    }

def server_setup():
    root = f"{pathlib.Path.home()}/.flow-server/"
    passwd_file = f"{root}passwd"
    db_file = f"{root}.db"
    public = f"{root}public.key"
    private = f"{root}private.key"

    check = check_files(root, passwd_file, db_file, public, private)
    if not all(valor == True for valor in check.values()):
        try:
            if not check["root"]: os.mkdir(root)
            if not check["keys"]: encryption.generate_keys(root)
            if not check["passwd"]: create_password(passwd_file)
            if not check["db"]: server_db_prepare(db_file)
        except Exception as e:
            try: shutil.rmtree(root)
            finally: raise e
    
    other.clear_console()
    print("Type your password to access flow.")
    check_password(passwd_file)
    other.clear_console()