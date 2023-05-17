import art, uuid
from functions.setup import client_setup
import functions.conection as con
import threads.client_control as client_control
import threads.client_msg as client_msg
import threads.client_websocket as client_websocket

settings = client_setup()

print(art.text2art("Welcome    to"))
print(art.text2art("flow", font='block'))

client_msg.MSGClient(settings["root"]).start()
client_control.ControlCon(settings["server"], settings["root"]).start()
client_websocket.WebSocket().start()

