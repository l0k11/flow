import art, waitress, threading
from functions.setup import client_setup
from functions.other import get_private_ip
import threads.client_control as client_control
import threads.client_msg as client_msg
import threads.client_websocket as client_websocket
import threads.client_api as api

settings = client_setup()

print(art.text2art("Welcome    to"))
print(art.text2art("flow", font='block'))
print(f"You can now chat in http://localhost:6005 or http://{get_private_ip()}:6005")

client_msg.MSGClient(settings["root"]).start()
client_control.ControlCon(settings["server"], settings["root"]).start()
client_websocket.WebSocket().start()
threading.Thread(target = lambda: waitress.serve(api.app, host = "0.0.0.0", port = 6005)).start()


