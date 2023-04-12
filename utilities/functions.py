import socket, json, sqlite3, uuid, pathlib
from time import time

def generate_id(ip, type):
    if type == "message":
        while True:
            id = f"m{uuid.uuid4}"
            if check_id(ip, id):
                return id
    
    if type == "user":
        while True:
            id = f"u{uuid.uuid4}"
            if check_id(ip, id):
                return id
            
    if type == "conversation":
        while True:
            id = f"c{uuid.uuid4}"
            if check_id(ip, id):
                return id
            
def check_id(ip, id: str):
    if id.startswith("u"):
        table = "users"
    elif id.startswith("m"):
        table = "messages"
    elif id.startswith("c"):
        table = "conversations"

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, 6003))
    packet = {
        "type": "checkID",
        "idToCheck": id,
        "table": table
    }
    client.sendall(str.encode(json.dumps(packet)))
    response = json.loads(client.recv(4096).decode())
    client.close()

    if response["status"] == "available":
        return True
    else:
        return False

def get_private_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    private_ip = s.getsockname()[0]
    s.close()
    return private_ip

def client_control_con(ip, db_file):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, 6003))
    with sqlite3.connect(db_file) as con:
        select = con.execute("SELECT contact_id FROM contacts WHERE contact_name='SUPER UNIQUE CONTACT NAME THAT WILL NOT BE DISPLAYED'")
        id = select.fetchall()[0][0]
    
    packet = {
        "type": "control",
        "id": id
    }
    client.sendall(str.encode(json.dumps(packet)))
    response = json.loads(client.recv(4096).decode())
    client.close()
    return response

def client_keys_exchange(ip, root):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, 6003))

    with sqlite3.connect(f"{root}.db") as con:
        select = con.execute("SELECT contact_id FROM contacts WHERE contact_name='SUPER UNIQUE CONTACT NAME THAT WILL NOT BE DISPLAYED'")
        id = select.fetchall()[0][0]
    
    with open(f"{root}public.key", "r", encoding = "utf-8") as file:
        key = file.read()

    packet = {
        "type": "key",
        "id": id,
        "key": key,
    }

    client.sendall(str.encode(json.dumps(packet)))
    response = json.loads(client.recv(4096).decode())
    client.close()
    
    with open(f"{root}server.key", "w", encoding = "utf-8") as file:
        file.write(response["key"])
    
    return response

def send_message(*, idSender, idReceiver, content):
    packet = {
        "idSender": idSender,
        "idReceiver": idReceiver,
        "idMessage": uuid.uuid4(),
        "content": content,
        "time": int(round(time() * 1000))
    }


def server_db_prepare(file):
    pathlib.Path(file).touch()
    with sqlite3.connect(file) as con:
        try:
            con.execute("""CREATE TABLE conversations (
                id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) 
            );""")

            con.execute("""CREATE TABLE users (
                id CHAR(36) PRIMARY KEY,
                ip VARCHAR(255),
                status VARCHAR(255)
            );""")
            
            con.execute("""CREATE TABLE messages (
                message_id CHAR(36) PRIMARY KEY,
                conversation_id CHAR(36),
                user_id CHAR(36),
                content VARCHAR(1000),
                timestamp VARCHAR(255),
                FOREIGN KEY (conversation_id) REFERENCES conversations(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            );""")
        except:
            con.close()
            raise Exception(f"Cannot find {file}")