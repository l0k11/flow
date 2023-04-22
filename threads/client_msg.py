import socket, threading, json, datetime,\
    functions.other as other,\
    functions.encryption as encryption,\
    functions.conection as con

class MSGClient(threading.Thread):
    def __init__(self, root):
        threading.Thread.__init__(self)
        self.ip = other.get_private_ip()
        self.root = root

    def run(self):
        server_msg_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_msg_socket.bind((self.ip, 6001))
        server_msg_socket.listen(999)

        while True:
            server, addr = server_msg_socket.accept()
            raw = server.recv(4096)
            raw = raw.split(b"\n\n\n")
            packet = encryption.decrypt_message(raw[0], f"{self.root}private.key", raw[1])
            packet = json.loads(packet)
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # TODO: ABSOLUTAMENTE TODO

            other.execute_db_command(
                f"{self.root}.db",
                "INSERT INTO messages VALUES (?,?,?,?,?,?)",
                (packet["idMessage"], packet["conv_id"], packet["idSender"], packet["idReceiver"], packet["content"], packet["time"])
            )
            # TODO: EVENTO DE SOCKETIO
            other.execute_db_command(
                f"{self.root}.db",
                "UPDATE contacts SET lastMsg = ?, lastMsgTime = ? WHERE id = ?",
                (packet["content"], packet["time"], packet["idReceiver"])
            )

            server.close()