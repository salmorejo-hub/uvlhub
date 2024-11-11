from discordbot.src.setup import client
import discord

@client.event
async def on_ready():
    print(f'Discord Bot {client.user} activated')
    
    
@client.command(help="Say hello to check if the bot is working correctly")
async def hello(ctx):
    await ctx.send("Hello!")
    
    
@client.command(help="Configurate your access token. This command makes the bot send you a private message to configurate your token")
async def token_config(ctx):
    user = ctx.message.author
    await user.send("To configurate your access token, please type !token <your_token>")
    
    
@client.command(help="Set your access token. Type !token <your_token>")
async def token(ctx, token=None):
    if token is None:
        await ctx.send("No token provided. Please type !token <your_token>")
        return

    if isinstance(ctx.channel, discord.DMChannel):
        message = "Token configurated successfully!"
                
        user = ctx.message.author
        # TODO: Save token        
        await user.send(message)
    else:
        await ctx.send("For security reasons, please configurate your token in a private message.")