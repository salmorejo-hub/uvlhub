import pytest
import pytest_asyncio
import discord.ext.test as dpytest
from discordbot.src.setup import init#, Base, engine
import os


@pytest.fixture(scope="session", autouse=True)
def set_test_db_env():
    os.environ['USE_TEST_DB'] = 'true'
    yield
    os.environ['USE_TEST_DB'] = 'false'


@pytest_asyncio.fixture
async def bot(request):
    client, engine, Base = await init()
    await client._async_setup_hook()
    
    # Crear listas de guilds, miembros y canales con nombres específicos
    guild_names = ["guild1", "guild2"]
    channel_names = ["channel1", "channel2"]
    member_names = ["user1", "user2"]

    # Configuración para dpytest: pasamos las listas con los nombres
    dpytest.configure(
        client=client,
        guilds=guild_names,      # Pasamos los nombres de los guilds
        text_channels=channel_names,  # Pasamos los nombres de los canales
        members=member_names     # Pasamos los nombres de los miembros
    )

    yield client
    
    await dpytest.empty_queue()
    Base.metadata.drop_all(bind=engine)
