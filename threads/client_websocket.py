import asyncio, websockets, threading, functions.other as other

class WebSocket(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.ip = other.get_private_ip()
        self.clientes = []

    def run(self):
        start_server = websockets.serve(self.websocket_handler, self.ip, 6004)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    async def websocket_handler(self, websocket, path):
        self.clientes.append(websocket)
        try:
            while True:
                mensaje = await websocket.recv()
                for cliente in self.clientes:
                    await cliente.send(mensaje)
        except websockets.exceptions.ConnectionClosedOK:
            self.clientes.remove(websocket)


