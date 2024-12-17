import pytest
import discord.ext.test as dpytest


@pytest.mark.asyncio
async def test_hello_command_guild(bot):
    channel = bot.guilds[0].text_channels[0]
    user = bot.guilds[0].members[0]

    # Check bot response in a guild
    await dpytest.message("!hello", channel=channel, member=user)
    assert dpytest.verify().message().peek().content("Hello!"), "The bot did not respond with the expected message"
    message = dpytest.get_message()
    assert message.channel == channel, "No message was sent in the correct channel"
    assert dpytest.verify().message().nothing(), "The bot sent more messages than expected"


@pytest.mark.asyncio
async def test_hello_command_dm(bot):
    user = bot.guilds[0].members[0]

    # Check bot response in a DM
    dm = await user.create_dm()
    await dpytest.message("!hello", dm)
    assert dpytest.verify().message().content("Hello!"), "The bot did not respond to the DM"
    assert dpytest.verify().message().nothing(), "The bot sent more messages than expected on a DM message"


@pytest.mark.asyncio
async def test_prefix_command_no_prefix(bot):
    channel = bot.guilds[0].text_channels[0]
    user = bot.guilds[0].members[0]

    await dpytest.message("!prefix", channel=channel, member=user)
    assert dpytest.verify().message().contains().content("No prefix provided"), "Error when no prefix is provided"


@pytest.mark.asyncio
async def test_prefix_command_first_time(bot):
    channel = bot.guilds[0].text_channels[0]
    user = bot.guilds[0].members[0]

    await dpytest.message("!prefix ?", channel=channel, member=user)
    assert dpytest.verify().message().content(
        "Prefix configured successfully!"), "Error when changing the prefix for the first time in a guild"

    await dpytest.message("?hello", channel=channel, member=user)
    assert dpytest.verify().message().content("Hello!"), "Prefix change did not work correctly"

    await dpytest.message("!hello", channel=channel, member=user)
    assert dpytest.verify().message().nothing(), "Bot still using old prefix"


@pytest.mark.asyncio
async def test_prefix_command_update(bot):
    channel = bot.guilds[0].text_channels[0]
    user = bot.guilds[0].members[0]

    await dpytest.message("!prefix ?")
    await dpytest.empty_queue()
    await dpytest.message("?prefix $", channel=channel, member=user)
    assert dpytest.verify().message().content(
        "Prefix updated successfully!"), "Error when updating the prefix for the second time in a guild"

    await dpytest.message("$hello", channel=channel, member=user)
    assert dpytest.verify().message().content("Hello!"), "Prefix change did not work correctly second time"


@pytest.mark.asyncio
async def test_prefix_command_affect_other_guild(bot):
    channel1 = bot.guilds[0].text_channels[0]
    user1 = bot.guilds[0].members[0]

    channel2 = bot.guilds[1].text_channels[0]
    user2 = bot.guilds[1].members[0]

    await dpytest.message("!prefix ?", channel=channel1, member=user1)
    await dpytest.empty_queue()

    # Check prefix did not affect other guilds
    await dpytest.message("!hello", channel=channel2, member=user2)
    assert dpytest.verify().message().content("Hello!"), "Prefix change affected other guilds"

    await dpytest.message("$hello", channel=channel2, member=user2)
    assert dpytest.verify().message().nothing(), "Bot still using old prefix in other guilds"