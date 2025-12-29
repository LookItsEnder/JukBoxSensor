import asyncio
from websockets.asyncio.server import broadcast, serve

async def noop(websocket):
    await websocket.wait_closed()

async def show_data(server):
    message = "Hello World!"
    broadcast(server.connections, message)
    await asyncio.sleep(5)

async def main():
    async with serve(noop, "localhost", 5678) as server:
        while(True):
            await show_data(server)

if __name__ == "__main__":
    asyncio.run(main())
