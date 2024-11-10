from discordbot.src.setup import client

@client.event
async def on_ready():
    print(f'Discord Bot {client.user} activated')
    
    
@client.command()
async def h(ctx):
    await ctx.send("Hello!")