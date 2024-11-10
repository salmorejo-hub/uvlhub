import discord
from discord.ext import commands

def init():
    intents = discord.Intents.default()
    intents.message_content = True
    
    client = commands.Bot(command_prefix="!", intents=intents)
    return client

client = init()