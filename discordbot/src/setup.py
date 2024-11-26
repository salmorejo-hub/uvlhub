import discord
from discord.ext import commands
from .database.models import ServerPrefix
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from discordbot.src.database.models import *
from dotenv import load_dotenv
from .commands.basic_commands import setup_basic_commands
from .commands.token_commands import setup_token_commands
import asyncio

load_dotenv()


# Configure database
DATABASE_URL = f"mysql+pymysql://{os.getenv('MARIADB_USER')}:{os.getenv('MARIADB_PASSWORD')}@{os.getenv('MARIADB_HOSTNAME')}:{os.getenv('MARIADB_PORT')}/{os.getenv('MARIADB_DATABASE')}"
# DATABASE_URL = f"mysql+pymysql://{os.getenv('MARIADB_USER')}:{os.getenv('MARIADB_PASSWORD')}@{os.getenv('MARIADB_HOSTNAME')}:{os.getenv('MARIADB_PORT')}/{os.getenv('MARIADB_TEST_DATABASE', os.getenv('MARIADB_DATABASE'))}"
engine = create_engine(DATABASE_URL)

session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = scoped_session(session_factory)

# Create database tables
Base.metadata.create_all(bind=engine)


 # Funtion to automatically get the prefix of the server/user
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
    
    

async def init():
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    
    client = commands.Bot(command_prefix=get_prefix, intents=intents)
    await setup_basic_commands(client, Session)
    await setup_token_commands(client, Session)
    return client

client = asyncio.run(init())