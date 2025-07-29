import asyncio
import websockets
import json
import os

# ✅ These are now pulled securely from environment variables
API_TOKEN = os.getenv("API_TOKEN")
ROOM_ID = os.getenv("ROOM_ID")

# 🌍 Highrise WebSocket Gateway
URL = "wss://gateway.highrise.game/web/websocket"

async def connect():
    async with websockets.connect(URL) as websocket:
        # 🔑 Authenticate the bot
        await websocket.send(json.dumps({
            "op": 0,
            "d": {
                "token": API_TOKEN,
                "room_id": ROOM_ID
            }
        }))

        print("✅ Bot connected and joined the room!")

        while True:
            try:
                message = await websocket.recv()
                data = json.loads(message)

                # Handle chat messages
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
                                "message": "Why don't skeletons fight each other? Because they don't have the guts! 💀"
                            }
                        }))
            except Exception as e:
                print("⚠️ Error:", e)
                break

# 🚀 Start the bot
asyncio.run(connect())
