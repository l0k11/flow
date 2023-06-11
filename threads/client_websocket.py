import asyncio
import websockets
import functions.other as other
import threading

class WebSocket:
    def __init__(self):
        self.ip = other.get_private_ip()
        self.clientes = []
        self.websocket_thread = None

    async def websocket_handler(self, websocket, path):
        self.clientes.append(websocket)
        try:
            while True:
                mensaje = await websocket.recv()
                print(self.clientes)
                for cliente in self.clientes:
                    print(cliente)
                    await cliente.send(mensaje)
        except websockets.exceptions.ConnectionClosedOK:
            self.clientes.remove(websocket)

    def run_websocket_server(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        start_server = websockets.serve(self.websocket_handler, self.ip, 6004)
        loop.run_until_complete(start_server)
        loop.run_forever()

    def start(self):
        self.websocket_thread = threading.Thread(target=self.run_websocket_server)
        self.websocket_thread.start()

