import socket, threading, json, platform, pathlib, sqlite3

class ControlServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.ip = self.get_private_ip()

    def run(self):
        mi_socket = socket.socket()
        mi_socket.bind((self.ip, 6003))
        mi_socket.listen(5)

        while True:
            try:
                conexion, addr = mi_socket.accept() # Esta se ejecuta hasta que conecta
                
                packet = conexion.recv(4096).decode()
                packet = json.loads(packet)

                if platform.system() == "Windows":
                    root = f"{pathlib.Path.home()}\\.flow-server\\"
                    separator = "\\"
                else:    
                    root = f"{pathlib.Path.home()}/.flow-server/"
                    separator = "/"
                
                print(packet)
                
                if packet["type"] == "key":
                    with open(f'{root}client_keys{separator}{packet["id"]}.key', 'w') as file:
                        file.write(packet["key"].decode())

                    with open(f'{root}public.key') as file:
                        public = file.read()

                    RPacket = {
                        "type": "key",
                        "id": "server",
                        "key": str.encode(public)
                    }
                    RPacket = json.dumps(RPacket)
                
                if packet["type"] == "control":
                    with sqlite3.connect(f"{root}.db") as con:
                        
                        try:
                            select = con.execute("SELECT * FROM users WHERE user_id=?", (str(packet["id"]),))
                            result = select.fetchall()
                            
                            if len(result) == 0:
                                con.execute("INSERT INTO users VALUES (?,?)", (str(packet["id"]), str(packet["ip"])))
                                
                            else:
                                con.execute("UPDATE users SET user_ip=? WHERE user_id=?", (str(packet["ip"]), str(packet["id"])))
                                
                            
                            
                            RPacket = {
                                "type": "control",
                                "id": "server",
                                "status": "ok"
                            }
                            RPacket = json.dumps(RPacket)
                        except:
                            con.close()
                            raise Exception(f"Cannot find to {file}")
                
                print(RPacket)
                send = socket.socket()
                send.connect((packet["ip"], 6001))
                send.send(str.encode(RPacket))
                conexion.close()
            except:
                pass
            
    def get_private_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        private_ip = s.getsockname()[0]
        s.close()
        return private_ip

servidor = ControlServer()
servidor.start()