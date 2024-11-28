import pytest
import pytest_asyncio
import discord.ext.test as dpytest
from discordbot.src.setup import client
import os
from discordbot.src.setup import Base, engine

@pytest.fixture(scope="session", autouse=True)
def set_test_db_env():
    os.environ['USE_TEST_DB'] = 'true'
    yield
    os.environ['USE_TEST_DB'] = 'false'

@pytest_asyncio.fixture
async def bot(request):
    await client._async_setup_hook()
    
    dpytest.configure(client)

    # Configura los guilds
    guild1 = dpytest.backend.make_guild("guild1")
    guild2 = dpytest.backend.make_guild("guild2")
    
    # Configura los canales de texto
    channel1 = dpytest.backend.make_text_channel("channel1", guild=guild1)
    channel2 = dpytest.backend.make_text_channel("channel2", guild=guild2)
    
    # Configura los usuarios
    user1 = dpytest.backend.make_user("user1", 1234)
    user2 = dpytest.backend.make_user("user2", 5678)
    
    # Configura los miembros
    member1 = dpytest.backend.make_member(user1, guild1)
    member2 = dpytest.backend.make_member(user2, guild2)
    
    yield client, guild1, guild2, channel1, channel2, member1, member2
    
    await dpytest.empty_queue()
    Base.metadata.drop_all(bind=engine)
