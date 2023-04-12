import socket, threading, json, platform, pathlib, sqlite3, utilities.functions as functions, time

class ControlServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.ip = functions.get_private_ip()

    def run(self):
        mi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mi_socket.bind((self.ip, 6003))
        mi_socket.listen(999)

        while True:
            conexion, addr = mi_socket.accept() # Esta se ejecuta hasta que conecta
            try:
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
                        file.write(packet["key"])

                    with open(f'{root}public.key') as file:
                        public = file.read()
                        
                    RPacket = {
                        "type": "key",
                        "id": "server",
                        "key": public
                    }
                    RPacket = json.dumps(RPacket)
                
                if packet["type"] == "control":
                    with sqlite3.connect(f"{root}.db") as con:
                        try:
                            select = con.execute("SELECT * FROM users WHERE user_id=?", (str(packet["id"]),))
                            result = select.fetchall()
                            
                            if len(result) == 0:
                                con.execute("INSERT INTO users VALUES (?,?, 'online')", (str(packet["id"]), str(packet["ip"])))
                            else:
                                con.execute("UPDATE users SET user_ip=?, status='online' WHERE user_id=?", (str(packet["ip"]), str(packet["id"])))

                            RPacket = {
                                "type": "control",
                                "id": "server",
                                "status": "ok"
                            }
                            RPacket = json.dumps(RPacket)
                        except:
                            con.close()
                            raise Exception(f"Cannot find to {file}")

                conexion.sendall(str.encode(RPacket))
                conexion.close()
            except:
                pass