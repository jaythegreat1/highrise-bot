# main.py

from flask import Flask
from threading import Thread
from highrise import BaseBot, User, Position, AnchorPosition, BotDefinition
from highrise.__main__ import main, arun
from importlib import import_module
import asyncio
import time
import random
import traceback
import os

dancs = [
    "emote-lust", "emote-superpose", "dance-tiktok10", "dance-weird",
    "emote-charging", "emote-snowball", "emote-hot", "emote-snowangel",
]

class WebServer:
    def __init__(self):
        self.app = Flask(__name__)

        @self.app.route('/')
        def index() -> str:
            return "Alive"

    def run(self) -> None:
        self.app.run(host='0.0.0.0', port=8080)

    def keep_alive(self):
        t = Thread(target=self.run)
        t.start()

class RunBot:
    room_id = "6416069d115b0b88a8c38805"
    bot_token = os.getenv("BOT_TOKEN")
    bot_file = "main"
    bot_class = "MyBot"

    def __init__(self) -> None:
        self.definitions = [
            BotDefinition(
                getattr(import_module(self.bot_file), self.bot_class)(),
                self.room_id,
                self.bot_token
            )
        ]

    def run_loop(self) -> None:
        while True:
            try:
                arun(main(self.definitions))
            except Exception:
                traceback.print_exc()
                time.sleep(1)

class MyBot(BaseBot):
    def __init__(self):
        self.dances = {dance: random.uniform(1, 10) for dance in dancs}

    async def on_ready(self):
        print("Bot is ready!")
        asyncio.create_task(self.send_continuous_dances())

    async def on_user_join(self, user: User, position: Position | AnchorPosition) -> None:
        await self.highrise.chat(f"Welcome, {user.username}!")
        await self.highrise.send_whisper(user.id, "Welcome! 🤍") 
        await asyncio.sleep(1)
        await self.highrise.chat(f"Type a number from 1 to 102, {user.username}.")
        await self.highrise.react("wave", user.id)

    async def send_continuous_dances(self):
        while True:
            valid_users = []
            users_positions = await self.highrise.get_room_users()
            for user, position in users_positions.content:
                if isinstance(position, Position):
                    valid_users.append(user)

            random_dance, duration = random.choice(list(self.dances.items()))
            tasks = [self.highrise.send_emote(random_dance, user.id) for user in valid_users]
            await asyncio.gather(*tasks)
            await asyncio.sleep(duration)

if __name__ == "__main__":
    WebServer().keep_alive()
    RunBot().run_loop()
