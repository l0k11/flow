import socket, threading, json, sqlite3, functions.other as other, datetime,\
    functions.encryption as en

class ControlServer(threading.Thread):
    def __init__(self, root):
        threading.Thread.__init__(self)
        self.ip = other.get_private_ip()
        self.root = root

    def run(self):
        mi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mi_socket.bind((self.ip, 6003))
        mi_socket.listen(999)

        while True:
            conexion, addr = mi_socket.accept()
            packet = conexion.recv(4096).decode()
            packet = json.loads(packet)

            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            packetID = str(packet["id"])
            
            if packet["type"] == "key":
                try:
                    with open(f'{self.root}client_keys/{packetID}.key', 'w') as file:
                        file.write(packet["key"])

                    with open(f'{self.root}public.key') as file:
                        public = file.read()
                        
                    RPacket = {
                        "type": "key",
                        "id": "server",
                        "key": public
                    }
                    
                except Exception as e:
                    conexion.close()
                    raise e
            
            elif packet["type"] == "control":
                with sqlite3.connect(f"{self.root}.db") as con:
                    try:
                        select = con.execute("SELECT id FROM users WHERE id=?", (packetID,))
                        result = select.fetchall()
                        
                        if len(result) == 0:
                            con.execute("INSERT INTO users VALUES (?,?)", (packetID, addr[0]))
                        else:
                            con.execute("UPDATE users SET ip = ? WHERE id = ?", (addr[0], packetID))

                        RPacket = {
                            "type": "control",
                            "id": "server",
                            "status": "ok"
                        }

                        # TODO: TESTEAR ESTO
                        select = con.execute("SELECT idMessage FROM waiting WHERE idReceiver = ?", (packetID,))
                        result = select.fetchall()
                        for message in result:
                            messages = []
                            MSelect = con.execute("SELECT * FROM messages WHERE idMessage = ?", (message[0],))
                            MResult = MSelect.fetchall()
                            messages.append({
                                "idMessage": MResult[0][0],
                                "idSender": MResult[0][2],
                                "idReceiver": MResult[0][3],
                                "content": MResult[0][4],
                                "time": MResult[0][5]
                            })
                        
                        packet = en.encrypt_message("\n\n\n".join(messages).encode(), f'{self.root}client_keys/{packetID}.key')
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                            client.connect((addr[0], 6001))
                            client.sendall("\n\n\n".join(packet).encode())
                        
                        con.execute("DELETE FROM waiting WHERE idReceiver = ?", (packetID,))
                        print(f"{now} {addr[0]}: Control conection correct")
                        
                    except Exception as e:
                        con.close()
                        conexion.close()
                        raise e

            elif packet["type"] == "checkID":
                with sqlite3.connect(f"{self.root}.db") as con:
                    try:
                        select = con.execute(f"SELECT id FROM {packet['table']} WHERE id = ?", (packet["idToCheck"],))
                        result = select.fetchall()
                        if len(result) == 0:
                            RPacket = {
                                "id": "server",
                                "available": True
                            }
                        else:
                            RPacket = {
                                "id": "server",
                                "available": False
                            }

                    except Exception as e:
                        con.close()
                        conexion.close()
                        raise e

            RPacket = json.dumps(RPacket)
            conexion.sendall(str.encode(RPacket))
            conexion.close()