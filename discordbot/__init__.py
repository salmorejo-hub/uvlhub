import os
from discordbot.src.setup import client
import discordbot.src.commands
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("BOT_TOKEN")

client.run(token)
