import pytest
import pytest_asyncio
import discord.ext.test as dpytest
from discordbot.src.setup import client
from discord.ext import commands
import os

@pytest.fixture(scope="session", autouse=True)
def set_test_db_env():
    os.environ['USE_TEST_DB'] = 'true'
    yield
    os.environ['USE_TEST_DB'] = 'false'

@pytest_asyncio.fixture
async def bot(request):
    await client._async_setup_hook()
    
    dpytest.configure(client)

    yield client
    
    await dpytest.empty_queue()

# @pytest.fixture(scope="module", autouse=True)
# def setup_database():
#     # Crea las tablas en la base de datos de pruebas
#     Base.metadata.create_all(bind=engine)
#     yield
#     # Elimina las tablas después de las pruebas
#     Base.metadata.drop_all(bind=engine)