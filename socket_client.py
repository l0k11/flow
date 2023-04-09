import socket
import threading
import json

class Servidor(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.ip = self.get_private_ip()

    def run(self):
        server = socket.socket()
        server.bind((self.ip, 8001))
        server.listen(5)

        while True:
            conexion, addr = server.accept() # Esta se ejecuta hasta que conecta
            packet = conexion.recv(4096).decode()
            conexion.close()

    def get_private_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        private_ip = s.getsockname()[0]
        s.close()
        return private_ip


servidor = Servidor()
servidor.start()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ipDestino = input("IP: ")
msg = input("Mensaje: ")
pack = {
    "ip": ipDestino,
    "message": msg
}

client.connect(("192.168.8.103", 8000))
client.send(str.encode(json.dumps(pack)))

client.close()