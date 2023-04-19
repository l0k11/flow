import art, uuid
from functions.setup import client_setup
import functions.conection as con

settings = client_setup()
# TODO: schedule.every(1).minutes.do(tarea, nombre="Juan", edad=30)

print(art.text2art("Welcome    to"))
print(art.text2art("flow", font='block'))

con.client_keys_exchange(settings["server"], settings["root"])
con.client_control_con(settings["server"], settings["root"])

con.send_message(
    ip = settings["server"],
    port = 6002,
    idSender = settings["id"],
    idReceiver = "u92d448d1-48ff-4053-be86-c726f570dbf0",
    content = "hola",
    server_key_file = f"{settings['root']}server.key"
)