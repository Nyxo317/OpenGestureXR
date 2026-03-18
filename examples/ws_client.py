"""
Connect to the gesture API server via WebSocket and print events.

    # start server first: uvicorn gesture_api.server.main:app
    python examples/ws_client.py
"""

import asyncio
import websockets


async def main():
    uri = "ws://localhost:8000/ws/gesture"
    print(f"connecting to {uri}...")
    async with websockets.connect(uri) as ws:
        while True:
            data = await ws.recv()
            print(data)


asyncio.run(main())
