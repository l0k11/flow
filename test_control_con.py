import socket, json, utilities.other_functs as other_functs


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((other_functs.get_private_ip(), 6003))
pack = {
    "type": "control",
    "id": "hola",
    "ip": other_functs.get_private_ip()
}
client.sendall(str.encode(json.dumps(pack)))

response = client.recv(4096).decode()
print("Respuesta del servidor: ", response)

client.close()