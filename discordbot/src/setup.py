import discord
from discord.ext import commands
from . import Session
from src.database.models import ServerPrefix

def get_prefix(bot, message):
    id = str(message.guild.id) if message.guild else str(message.author.id)
    
    try:
        db = Session()
        server_prefix = db.query(ServerPrefix).filter(ServerPrefix.server_id == id).first()
        if server_prefix:
            prefix = server_prefix.prefix
        else:
            prefix = "!"
        return prefix
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return "!"
    
    

def init():
    intents = discord.Intents.default()
    intents.message_content = True
    
    client = commands.Bot(command_prefix=get_prefix, intents=intents)
    return client

client = init()