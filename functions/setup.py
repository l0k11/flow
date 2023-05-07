import os, sqlite3, pathlib, getpass, hashlib, shutil,\
    functions.encryption as encryption,\
    functions.conection as con,\
    functions.other as other
import pdb

# Aquí almaceno las diferentes funciones usadas para preparar tanto el cliente como el servidor
# para su uso, generando la estructura de las bases de datos, las claves, la contraseña de acceso,
# y comprobando la conexión del cliente a ambos servidores (en este proceso es cuando se realiza el
# intercambio de claves) 

def server_db_prepare(file):
    open(file, "w")
    with sqlite3.connect(file) as con:
        try:
            con.execute("""CREATE TABLE conversations (
                id CHAR(37) PRIMARY KEY UNIQUE,
                users VARCHAR(255)
            );""")

            con.execute("""CREATE TABLE users (
                id CHAR(37) PRIMARY KEY UNIQUE,
                ip VARCHAR(255),
                status VARCHAR(255),
                lastCheck VARCHAR(255)
            );""")
            
            con.execute("""CREATE TABLE messages (
                id CHAR(37) PRIMARY KEY UNIQUE,
                idConversation CHAR(37),
                idSender CHAR(37),
                idReceiver CHAR(37),
                content VARCHAR(4096),
                time VARCHAR(255),
                FOREIGN KEY (idConversation) REFERENCES conversations(id),
                FOREIGN KEY (idSender) REFERENCES users(id),
                FOREIGN KEY (idReceiver) REFERENCES users(id)
            );""")

            con.execute("""CREATE TABLE waiting (
                idMessage CHAR(37),
                idReceiver CHAR(37),
                FOREIGN KEY (idMessage) REFERENCES messages(id),
                FOREIGN KEY (idReceiver) REFERENCES users(id)
            );""")
            print("Esqueleto hecho")
            pdb.set_trace()
        except Exception as e:
            con.close()
            raise e

def client_db_prepare(file):
    open(file, "w")
    with sqlite3.connect(file) as con:
        try:
            con.execute("""CREATE TABLE conversations (
                id CHAR(37) PRIMARY KEY,
                users VARCHAR(255),
                name VARCHAR(255),
                lastMsg VARCHAR(4095),
                lastMsgTime VARCHAR(255)
            );""")

            con.execute("""CREATE TABLE contacts (
                id CHAR(37) PRIMARY KEY,
                name VARCHAR(255)
            );""")

            con.execute("""CREATE TABLE messages (
                id CHAR(37) PRIMARY KEY UNIQUE,
                conversation_id CHAR(37),
                sender_id CHAR(37),
                receiver_id CHAR(37),
                content VARCHAR(4095),
                time VARCHAR(255),
                FOREIGN KEY (conversation_id) REFERENCES conversations(id),
                FOREIGN KEY (sender_id) REFERENCES contacts(id)
            );""")

        except Exception as e:
            con.close()
            raise e

def check_files(root, passwd, db, public, private, keys_dir = None):
    return {
        "root": os.path.exists(root),
        "keys": os.path.exists(public) and os.path.exists(private),
        "passwd": os.path.exists(passwd),
        "db": os.path.exists(db),
        "keys_dir": os.path.exists(keys_dir) if keys_dir else False
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

def test_control(ip: str, root: str, db_file):
    try:
        select = other.execute_db_command(
            db_file,
            "SELECT id FROM contacts WHERE name = 'SUPER UNIQUE CONTACT NAME THAT WILL NOT BE DISPLAYED'"
        )
        result = select.fetchall()
        if result: user_id = result[0][0]
        else:
            user_id = con.generate_id(ip, "user")
            other.execute_db_command(
                db_file,
                "INSERT INTO contacts VALUES (?,?,?,?)",
                (user_id, "SUPER UNIQUE CONTACT NAME THAT WILL NOT BE DISPLAYED", None, None)
            )
        
        con.client_keys_exchange(ip, root)
        return user_id
        
    except:
        return False
    
def test_messages(ip: str, root: str):
    con.send_message(
        ip = ip,
        port = 6002,
        idSender = "client",
        idReceiver = "server",
        content = "Nada",
        key_file = f"{root}server.key"
    )
    return ip
        
def client_setup():
    other.clear_console()
    root = f"{pathlib.Path.home()}/.flow/"
    passwd_file = f"{root}passwd"
    db_file = f"{root}.db"
    public = f"{root}public.key"
    private = f"{root}private.key"

    check = check_files(root, passwd_file, db_file, public, private)
    if not all(valor == True for valor in check.values()):
        try:
            if not check["root"]: os.mkdir(root)
            if not check["passwd"]: create_password(passwd_file)
            if not check["db"]: client_db_prepare(db_file)
            if not check["keys"]: encryption.generate_keys(root)
        except Exception as e:
            try: shutil.rmtree(root)
            finally: raise e

    other.clear_console()
    print("Type your password to access flow.")
    check_password(passwd_file)

    print("Now provide the IP address of the server in your local network")
    while True:
        server_ip = input("Type the IP address: ")
        try:
            user_id = test_control(server_ip, root, db_file)
            test_messages(server_ip, root)
            break
        except Exception as e:
            print(f"{server_ip} is not a valid server.")
            raise e

    other.clear_console()
    with open(f"{root}.env", "w") as file:
        file.write(f"#DO NOT SHARE NEITHER MODIFY THIS FILE\nSERVER_IP={server_ip}\nUSER_ID={user_id}")
        
    return {
        "server": server_ip,
        "root": root,
        "id": user_id
    }

def server_setup():
    root = f"{pathlib.Path.home()}/.flow-server/"
    passwd_file = f"{root}passwd"
    db_file = f"{root}.db"
    public = f"{root}public.key"
    private = f"{root}private.key"
    keys_dir = f"{root}client_keys"

    check = check_files(root, passwd_file, db_file, public, private, keys_dir)
    if not all(valor == True for valor in check.values()):
        try:
            if not check["root"]: os.mkdir(root)
            if not check["passwd"]: create_password(passwd_file)
            if not check["db"]: server_db_prepare(db_file)
            if not check["keys"]: encryption.generate_keys(root)
            if not check["keys_dir"]: os.mkdir(keys_dir)
        except Exception as e:
            try: shutil.rmtree(root)
            finally: raise e
    
    other.clear_console()
    print("Type your password to access flow.")
    check_password(passwd_file)
    other.clear_console()