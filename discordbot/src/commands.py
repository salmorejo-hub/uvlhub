from discordbot.src.setup import client

@client.event
async def on_ready():
    print(f'Discord Bot {client.user} activated')
    
    
@client.command()
async def h(ctx):
    await ctx.send("Hello!")
    
    
@client.command()
async def help(ctx):
    response = """
    **List of commands:**
    - !h: Say hello to check if the bot is working correctly
    - !help: Show this message to list all available commands
    """
    await ctx.send(response)