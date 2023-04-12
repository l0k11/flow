import socket, threading, json, utilities.functions as functions

class MSGServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.ip = functions.get_private_ip()

    def run(self):
        server_msg_socket = socket.socket()
        server_msg_socket.bind((self.ip, 6002))
        server_msg_socket.listen(999)

        while True:
            conexion, addr = server_msg_socket.accept() # Esta se ejecuta hasta que conecta
            # pack = conexion.recv(1024).decode()
            # pack = json.loads(pack)
            
            # ipDestino = pack["ip"]
            # msg = pack["message"]

            # print(ipDestino)
            # print(msg)

            # enviar = socket.socket()
            # enviar.connect((ipDestino, 8001))
            # enviar.send(str.encode(msg))
            conexion.close()