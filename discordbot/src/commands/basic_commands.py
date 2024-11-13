from discordbot.src.setup import client
import discord
from .. import Session
from src.database.models import UserToken

@client.event
async def on_ready():
    print(f'Discord Bot {client.user} activated')
    
    
@client.command(help="Say hello to check if the bot is working correctly")
async def hello(ctx):
    await ctx.send("Hello!")