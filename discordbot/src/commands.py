from discordbot.src.setup import client
import discord
from . import Session
from src.database.models import UserToken

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

    # Check if the channel is a private message
    if isinstance(ctx.channel, discord.DMChannel):
        message = "Token configurated successfully!"
                
        user = ctx.message.author
        db = Session()
        try:
            # Check if user already has a token
            existing_user = db.query(UserToken).filter(UserToken.user_id == str(user.id)).first()
            if existing_user:
                # If the user already exists, update the token
                existing_user.token = token
                db.commit()
                message = "Token updated successfully!"
            else:
                # If the user does not exist, create a new user
                new_user_token = UserToken(user_id=str(user.id), token=token)
                db.add(new_user_token)
                db.commit()
                db.refresh(new_user_token)
                message = "Token configurated successfully!"
            await ctx.send(message)
        except Exception as e:
            db.rollback()
            message = f"An error occurred: {str(e)}"
            await ctx.send(message)
        finally:
            Session.remove()
    else:
        await ctx.send("For security reasons, please configurate your token in a private message.")
        
        
#This command needs to be removed. It is only for testing purposes       
@client.command(help="Get your access token")
async def GetToken(ctx):
    user = ctx.message.author
    db = Session()
    try:
        user_token = db.query(UserToken).filter(UserToken.user_id == str(user.id)).first()
        if user_token:
            await ctx.send(f"Your token is: {user_token.token}")
        else:
            await ctx.send("You don't have a token configurated. Please type !token_config to configurate your token.")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")
    finally:
        Session.remove()