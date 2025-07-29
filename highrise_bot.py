import asyncio
import websockets
import json

# 🔐 Replace with your real token and room_id
API_TOKEN = "b2873944dec863e4fb25857f843528f63f9126dc5bb9b50faa9b1900b7d1ebea"
ROOM_ID = "6888a307b95ec91e67028e2e"

# 🌍 Highrise gateway
URL = "wss://gateway.highrise.game/web/websocket"

async def connect():
    async with websockets.connect(URL) as websocket:
        # 🔑 Authenticate
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

                if data.get("op") == 1:  # Incoming chat or action
                    user = data["d"]["user"]["username"]
                    content = data["d"].get("content", "")

                    print(f"📩 {user}: {content}")

                    # Example emote reaction
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

# Run it
asyncio.run(connect())
