from core.blueprints.base_blueprint import BaseBlueprint
import discord
from discord.ext import commands
import os

explore_bp = BaseBlueprint('explore', __name__, template_folder='templates')


def init():
    intents = discord.Intents.default()
    intents.message_content = True
    
    client = commands.Bot(command_prefix="!", intents=intents)
    return client

token = os.getenv("DISCORD_TOKEN")

client = init()

client.run(token)
