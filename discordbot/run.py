import os
from discordbot.src.setup import client
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("BOT_TOKEN")

client.run(token)
