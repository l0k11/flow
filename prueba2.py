import websocket

ws = websocket.WebSocket()
ws.connect(f"ws://192.168.8.102:6004")
ws.send("/n/n".join(["u7a9ac7bf-e9f6-4296-bfb2-22d92ae9d7c4", "uda95dff7-2367-46b8-a2d4-f4fcc64f257d", "content", "1684863042904"]))
ws.close()
