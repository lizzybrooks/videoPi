import asyncio
from aiohttp import web

clients = []

async def handle_message(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    clients.append(ws)
    print("Client connected")

    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            print(f"Received message: {msg.data}")
            # Broadcast the message to all connected clients
            for client in clients:
                if client != ws:
                    await client.send_str(msg.data)
        elif msg.type == web.WSMsgType.ERROR:
            print(f"WebSocket connection closed with exception {ws.exception()}")

    clients.remove(ws)
    print("Client disconnected")
    return ws

app = web.Application()
app.add_routes([web.get('/ws', handle_message)])

if __name__ == "__main__":
    web.run_app(app, port=8080)
