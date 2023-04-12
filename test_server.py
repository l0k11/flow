import socket, utilities.functions as functions

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((functions.get_private_ip(), 6004))
server_socket.listen(10)

while True:
    print("Esperando conexión entrante...")
    connection, client_address = server_socket.accept()
    try:
        print("Conexión desde:", client_address[0])
        datos_recibidos = connection.recv(1024)
        mensaje = datos_recibidos.decode()
        print("Mensaje recibido:", mensaje)
        respuesta = "hola cliente"
        connection.sendall(respuesta.encode())

    finally:
        connection.close()