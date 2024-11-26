import pytest
import pytest_asyncio
import asyncio
import discord.ext.test as dpytest
from src.setup import client

@pytest.mark.asyncio
async def test_hello_command(bot):
    await dpytest.message("!hello")

    # Verifica que el bot responde con "Hello!"
    assert dpytest.verify().message().content("Hello!")