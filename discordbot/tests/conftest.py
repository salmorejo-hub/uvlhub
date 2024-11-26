import pytest
import pytest_asyncio
import discord.ext.test as dpytest
from discordbot.src.setup import client
import discordbot.src.commands.basic_commands
import discord
from discord.ext import commands

@pytest_asyncio.fixture
async def bot(request):
    await client._async_setup_hook()
    
    dpytest.configure(client)

    yield client
    
    dpytest.empty_queue()

# @pytest.fixture(scope="module", autouse=True)
# def setup_database():
#     # Crea las tablas en la base de datos de pruebas
#     Base.metadata.create_all(bind=engine)
#     yield
#     # Elimina las tablas después de las pruebas
#     Base.metadata.drop_all(bind=engine)