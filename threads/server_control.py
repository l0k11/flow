import socket, threading, json, sqlite3, utilities.functions as functions, datetime

class ControlServer(threading.Thread):
    def __init__(self, root):
        threading.Thread.__init__(self)
        self.ip = functions.get_private_ip()
        self.root = root

    def run(self):
        mi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mi_socket.bind((self.ip, 6003))
        mi_socket.listen(999)

        while True:
            conexion, addr = mi_socket.accept()
            try:
                packet = conexion.recv(4096).decode()
                packet = json.loads(packet)
                
                if packet["type"] == "key":
                    with open(f'{self.root}client_keys/{packet["id"]}.key', 'w') as file:
                        file.write(packet["key"])

                    with open(f'{self.root}public.key') as file:
                        public = file.read()
                        
                    RPacket = {
                        "type": "key",
                        "id": "server",
                        "key": public
                    }
                    RPacket = json.dumps(RPacket)
                    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(f"{now} {addr[0]}: Key exchange conection correct")
                
                elif packet["type"] == "control":
                    with sqlite3.connect(f"{self.root}.db") as con:
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
                            print(f"{now} {addr[0]}: Control conection correct")
                        except:
                            con.close()
                            raise Exception(f"Cannot find to {file}")
                
                elif packet["type"] == "checkID":
                    with sqlite3.connect(f"{self.root}.db") as con:
                        con.execute("SELECT ")
                
                conexion.sendall(str.encode(RPacket))
                conexion.close()
            except:
                pass