import discord
from discordbot.src.database.models import UserToken


async def setup_token_commands(client, session):

    @client.command(help="Configurate your access token. This command makes the bot send you a private message to configurate your token")
    async def token_config_on_dm(ctx):
        user = ctx.message.author
        await user.send("To configurate your access token, please type !token <your_token>")

    @client.command(help="Set your access token. Type !token <your_token>")
    async def token(ctx, token=None):

        if token is None:
            await ctx.send("No token provided. Please type !token <your_token>")
            return

        # Check if the channel is a private message
        if isinstance(ctx.channel, discord.DMChannel):
            message = ""

            user = ctx.message.author
            db = session()
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
                    message = "Token configured successfully!"
                await ctx.send(message)
            except Exception as e:
                db.rollback()
                print(f"An error occurred: {str(e)}")
                await ctx.send(f'An error occurred: {str(e)}')
            finally:
                session.remove()
        else:
            await ctx.send("For security reasons, please  change your token and configurate it in a private message.")

