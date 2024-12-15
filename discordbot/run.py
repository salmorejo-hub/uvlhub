import os
from discordbot.src.setup import init
from dotenv import load_dotenv
import asyncio

load_dotenv()

token = os.getenv("BOT_TOKEN")
client, engine, Base = asyncio.run(init())
client.run(token)
