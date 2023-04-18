import socket, threading, json, functions.other as other,\
    functions.encryption as encryption

class MSGServer(threading.Thread):
    def __init__(self, root):
        threading.Thread.__init__(self)
        self.ip = other.get_private_ip()
        self.root = root

    def run(self):
        server_msg_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_msg_socket.bind((self.ip, 6002))
        server_msg_socket.listen(999)

        while True:
            server, addr = server_msg_socket.accept()
            raw = server.recv(4096)
            raw = raw.split(b"\n\n\n")
            packet = encryption.decrypt_message(raw[0], f"{self.root}private.key", raw[1])
            packet = json.loads(packet)

            if packet["idReceiver"] == "server":
                RPacket = {
                        "type": "con_test",
                        "status": "ok"
                    }
                server.sendall(json.dumps(RPacket).encode())

            else:
                conv_id = other.get_conv_id(packet["idSender"], packet["idReceiver"], f"{self.root}.db")
                other.execute_db_command(
                    f"{self.root}.db",
                    "INSERT INTO messages VALUES (?,?,?,?,?,?)",
                    (packet["idMessage"], conv_id, packet["idSender"], packet["idReceiver"], packet["content"], packet["time"])
                )
                select = other.execute_db_command(
                    f"{self.root}.db",
                    "SELECT ip FROM users WHERE id = ?",
                    (packet["idReceiver"],)
                )
                result = select.fetchall()

                sendPacket = json.dumps(packet)
                sendPacket = encryption.encrypt_message(sendPacket.encode(), f"{self.root}client_keys/{packet['idReceiver']}.key")
                
                if len(result):
                    # TODO: TRY EXCEPT POR SI ESTAS DESCONECTADO
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                        print("Mandado")
                        client.connect((result[0][0], 6001))
                        client.sendall(str.encode())
                    
            server.close()

# TODO: CONEXION DE CONTROL PARA LOS MENSAJES MANDADOS MIENTRAS ESTABAS DESCONECTADO.