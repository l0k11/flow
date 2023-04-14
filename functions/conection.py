import uuid, socket, json, time, sqlite3

def generate_id(ip, type):
    if type == "message":
        while True:
            id = f"m{uuid.uuid4()}"
            if check_id(ip, id):
                return id
    
    if type == "user":
        while True:
            id = f"u{uuid.uuid4()}"
            print(f"generate_id id {id}")
            print(f"generate_id ip {ip}")
            if check_id(ip, id):
                return id
            
    if type == "conversation":
        while True:
            id = f"c{uuid.uuid4()}"
            if check_id(ip, id):
                return id
            
    else:
        raise TypeError(f"Type {type} not valid")
            
def check_id(ip, id: str):
    if id.startswith("u"): table = "users"
    elif id.startswith("m"): table = "messages"
    elif id.startswith("c"): table = "conversations"

    packet = {
        "type": "checkID",
        "idToCheck": id,
        "table": table
    }
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((ip, 6003))
        client.sendall(bytes(json.dumps(packet), "utf-8"))
        response = json.loads(client.recv(4096).decode())
        
    print(response)

    return True if response["available"] else False
    
def client_control_con(ip, db_file):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, 6003))
    with sqlite3.connect(db_file) as con:
        select = con.execute("SELECT id FROM contacts WHERE name='SUPER UNIQUE CONTACT NAME THAT WILL NOT BE DISPLAYED'")
        id = select.fetchall()[0][0]
    
    packet = {
        "type": "control",
        "id": id
    }

    client.sendall(bytes(json.dumps(packet), "utf-8"))
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

    client.sendall(bytes(json.dumps(packet), "utf-8"))
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
        "time": int(round(time.time() * 1000))
    }



