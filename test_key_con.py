import socket, json, utilities.functions as functions

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((functions.get_private_ip(), 6003))
with open("C:/Users/Luis/.flow/public.key", encoding = "utf-8") as file:
    key = file.read()

pack = {
    "type": "key",
    "id": "hola",
    "key": key
}
client.sendall(str.encode(json.dumps(pack)))

response = json.loads(client.recv(4096).decode())
client.close()

with open("C:/Users/Luis/.flow/server.key", "w", encoding = "utf-8") as file:
    file.write(response["key"])