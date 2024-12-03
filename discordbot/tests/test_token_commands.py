import pytest
import discord.ext.test as dpytest


@pytest.mark.asyncio
async def test_token_config_command(bot):
    channel = bot.guilds[0].text_channels[0]
    user = bot.guilds[0].members[0]
    
    await dpytest.message("!token_config", channel=channel, member=user)
    message = dpytest.get_message()
    assert message.channel == user.dm_channel, "The bot did not send a private message"
    assert message.content.__contains__("To configurate your access token"), "The bot did not send the expected message"
    
    dm = await user.create_dm()
    await dpytest.message("!token_config", dm)
    assert dpytest.verify().message().contains().content("To configurate your access token"), "The bot did not send the expected message in a DM"
    
    
@pytest.mark.asyncio
async def test_token_command(bot):
    channel = bot.guilds[0].text_channels[0]
    user = bot.guilds[0].members[0]
    
    await dpytest.message("!token", channel=channel, member=user)
    assert dpytest.verify().message().contains().content("No token provided"), "The bot did not send the expected message when no token is provided"
    
    await dpytest.message("!token test_token", channel=channel, member=user)
    assert dpytest.verify().message().contains().content("For security reasons"), "The bot permited the token to be configured in a guilds channel"
    
    dm = await user.create_dm()
    await dpytest.message("!token test_token", dm)
    assert dpytest.verify().message().content("Token configured successfully!"), "The bot did not send the expected message when the token is configured"
    
    await dpytest.message("!token test_token", dm)
    assert dpytest.verify().message().content("Token updated successfully!"), "The bot did not send the expected message when the token is updated"
    
    