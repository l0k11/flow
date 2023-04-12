import socket, json, utilities.functions as functions


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((functions.get_private_ip(), 6003))
pack = {
    "type": "control",
    "id": "hola",
    "ip": functions.get_private_ip()
}
client.sendall(str.encode(json.dumps(pack)))

response = client.recv(4096).decode()
print("Respuesta del servidor: ", response)

client.close()