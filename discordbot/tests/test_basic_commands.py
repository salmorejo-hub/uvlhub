import pytest
import pytest_asyncio
import asyncio
import discord.ext.test as dpytest
from src.setup import client

@pytest.mark.asyncio
async def test_hello_command(bot):
    assert bot is not None, "Fixture bot no devolvió datos válidos"
    
    channel1 = bot.guilds[0].text_channels[0]
    user1 = bot.guilds[0].members[0]
    
    # Check bot response in a guild
    await dpytest.message("!hello", channel=channel1, member=user1)
    assert dpytest.verify().message().peek().content("Hello!"), "The bot did not respond with the expected message"
    message = dpytest.get_message()
    assert message.channel == channel1, "No message was sent in the correct channel"
    assert dpytest.verify().message().nothing(), "The bot sent more messages than expected"
    
    dpytest.empty_queue()
    
    # Check bot response in a DM
    dm = await user1.create_dm()
    await dpytest.message("!hello", dm)
    assert dpytest.verify().message().content("Hello!"), "The bot did not respond to the DM"
    assert dpytest.verify().message().nothing(), "The bot sent more messages than expected on a DM message"
    
    