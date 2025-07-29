import asyncio
import websockets
import json
import os

# Token and Room ID from Render environment variables
API_TOKEN = os.getenv("API_TOKEN")
ROOM_ID = os.getenv("ROOM_ID")

URL = "wss://gateway.highrise.game/web/websocket"

async def connect():
    async with websockets.connect(URL) as websocket:
        await websocket.send(json.dumps({
            "op": 0,
            "d": {
                "token": API_TOKEN,
                "room_id": ROOM_ID
            }
        }))
        print("✅ Connected to Highrise")

        while True:
            try:
                message = await websocket.recv()
                data = json.loads(message)

                if data.get("op") == 1:
                    user = data["d"]["user"]["username"]
                    content = data["d"].get("content", "")

                    print(f"📩 {user}: {content}")

                    if "hello" in content.lower():
                        await websocket.send(json.dumps({
                            "op": 26,
                            "d": {
                                "emote_id": "wave"
                            }
                        }))
                    elif "joke" in content.lower():
                        await websocket.send(json.dumps({
                            "op": 1,
                            "d": {
                                "message": "Why don’t skeletons fight? They don’t have the guts! 💀"
                            }
                        }))
            except Exception as e:
                print("⚠️ Error:", e)
                break

asyncio.run(connect())
