import functions.conection as con
import uuid

con.send_message(ip = "192.168.1.92", idSender = str(uuid.uuid4()), idReceiver = "hola", content = "hola", server_key_file = "C:/Users/Luis/.flow/server.key")