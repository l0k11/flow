import socket
import json

def get_private_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    private_ip = s.getsockname()[0]
    s.close()
    return private_ip

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pack = {
    "type": "control",
    "id": "hola",
    "ip": get_private_ip()
}

client.connect(("192.168.8.102", 6003))
client.send(str.encode(json.dumps(pack)))

client.close()