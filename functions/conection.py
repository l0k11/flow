import uuid, socket, json, time, sqlite3,\
    functions.encryption as encryption

# Estas son las funciones usadas para gestionar el envío de paquetes a los diferentes servidores 

def generate_id(ip, type):
    if type == "message":
        while True:
            id = f"m{uuid.uuid4()}"
            if check_id(ip, id):
                return id
    
    if type == "user":
        while True:
            id = f"u{uuid.uuid4()}"
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

    return True if response["available"] else False

def check_ip(serverIP, ipToCheck):
    packet = {
        "type": "checkIP",
        "ipToCheck": ipToCheck
    }
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((serverIP, 6003))
        client.sendall(bytes(json.dumps(packet), "utf-8"))
        response = json.loads(client.recv(4096).decode())
    
    return response["id"]

def client_control_con(ip, root):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, 6003))
    with sqlite3.connect(f"{root}.db") as con:
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
    with sqlite3.connect(f"{root}.db") as con:
        select = con.execute("SELECT id FROM contacts WHERE name='SUPER UNIQUE CONTACT NAME THAT WILL NOT BE DISPLAYED'")
        id = select.fetchall()[0][0]
    
    with open(f"{root}public.key", "r", encoding = "utf-8") as file:
        key = file.read()

    packet = {
        "type": "key",
        "id": id,
        "key": key,
    }
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((ip, 6003))
        client.sendall(bytes(json.dumps(packet), "utf-8"))
        response = json.loads(client.recv(4096).decode())
    
    with open(f"{root}server.key", "w", encoding = "utf-8") as file:
        file.write(response["key"])

    return response

def send_message(*, ip, port, idMessage = None, idSender, idReceiver, idConv, content, MTime = None, key_file):
    packet = {
        "idMessage": generate_id(ip, "message") if idMessage == None else idMessage,
        "idSender": idSender,
        "idReceiver": idReceiver,
        "idConv": idConv,
        "content": content,
        "time": int(round(time.time() * 1000)) if MTime == None else MTime
    }

    packet = json.dumps(packet).encode()
    packet = encryption.encrypt_message(packet, key_file)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            client.connect((ip, port))
            client.sendall(b'\n\n\n'.join(packet))
            response = json.loads(client.recv(4096).decode())

            if not response["status"]: return 1
            return 0
        except:
            return 1

def get_ip(id, ip):
    packet = {
        "type": "getIP",
        "id": id
    }
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((ip, 6003))
        client.sendall(bytes(json.dumps(packet), "utf-8"))
        response = json.loads(client.recv(4096).decode())
    
    print(response)
    print(type(response))
    if response["ip"] != "0": return response["ip"]
    else: return "Es imposible que llegue aquí"

def generateConvID(ip, idSender, idReceiver):
    packet = {
        "type": "getConvID",
        "idSender": idSender,
        "idReceiver": idReceiver,
    }
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((ip, 6003))
        client.sendall(bytes(json.dumps(packet), "utf-8"))
        response = json.loads(client.recv(4096).decode())
    
    return response["id"]
