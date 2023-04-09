import socket
import threading
import json

class Servidor(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.ip = self.get_private_ip()

    def run(self):
        mi_socket = socket.socket()
        mi_socket.bind((self.ip, 6001))
        mi_socket.listen(5)

        while True:
            conexion, addr = mi_socket.accept() # Esta se ejecuta hasta que conecta
            pack = conexion.recv(1024).decode()
            pack = json.loads(pack)
            
            ipDestino = pack["ip"]
            msg = pack["message"]

            print(ipDestino)
            print(msg)

            enviar = socket.socket()
            enviar.connect((ipDestino, 8001))
            enviar.send(str.encode(msg))
            conexion.close()

    def get_private_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        private_ip = s.getsockname()[0]
        s.close()
        return private_ip

servidor = Servidor()
servidor.start()