import socket, json, sqlite3, uuid, time

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
    
    pack = {
        "type": "control",
        "id": id
    }
    client.sendall(str.encode(json.dumps(pack)))
    response = json.loads(client.recv(4096).decode())
    client.close()
    return response



def client_keys_exchange(*, ip, root):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, 6003))

    with sqlite3.connect(f"{root}.db") as con:
        select = con.execute("SELECT contact_id FROM contacts WHERE contact_name='SUPER UNIQUE CONTACT NAME THAT WILL NOT BE DISPLAYED'")
        id = select.fetchall()[0][0]
    
    with open(f"{root}public.key", "r", encoding = "utf-8") as file:
        key = file.read()

    pack = {
        "type": "key",
        "id": id,
        "key": key,
    }

    client.sendall(str.encode(json.dumps(pack)))
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
        "time": "time"
    },