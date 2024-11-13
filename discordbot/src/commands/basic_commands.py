from discordbot.src.setup import client
import discord
from .. import Session
from src.database.models import ServerPrefix

@client.event
async def on_ready():
    print(f'Discord Bot {client.user} activated')
    
    
@client.command(help="Say hello to check if the bot is working correctly")
async def hello(ctx):
    await ctx.send("Hello!")
    
@client.command(help="Change bot prefix in the server")
async def prefix(ctx, prefix):
    id = ctx.guild.id if ctx.guild else ctx.author.id
    
    if prefix is None:
        await ctx.send("No prefix provided. Please type !prefix <new_prefix>")
        return
    
    try:
        db = Session()
        
        # Check if the prefix already exists
        existing_server_prefix = db.query(ServerPrefix).filter(ServerPrefix.server_id == str(id)).first()
        if existing_server_prefix:
            existing_server_prefix.prefix = prefix
            db.commit()
            message = "Prefix updated successfully!"
        else:
            new_server_prefix = ServerPrefix(server_id=str(id), prefix=prefix)
            db.add(new_server_prefix)
            db.commit()
            db.refresh(new_server_prefix)
            message = "Prefix configurated successfully!"
        await ctx.send(message)
    except Exception as e:
        db.rollback()
        print(f"An error occurred: {str(e)}")
        await ctx.send(f"An error occurred")