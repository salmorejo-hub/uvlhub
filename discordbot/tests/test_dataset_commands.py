import pytest
import discord.ext.test as dpytest

user_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VyX2VtYWlsIjoidXNlcjFAZXhhbXBsZS5jb20iLCJleHAiOjE3Mzg3NzkzODcsImlhdCI6MTczMzU5NTM4N30.JMbVIPOTI_SIDlx2vGp48w9bjiwCbYV4JSiwLer88-8"

@pytest.mark.asyncio
async def test_datasets_command(bot):
    channel = bot.guilds[0].text_channels[0]
    user = bot.guilds[0].members[0]

    # Check command when the user has not registered a token
    await dpytest.message("!datasets", channel=channel, member=user)
    assert dpytest.verify().message().contains().content(
        "You have not registered your token"
    ), "The bot did not respond with the expected message when no token used."

    # Check command when an invalid token is used
    dm = await user.create_dm()
    await dpytest.message("!token false_token", dm)
    await dpytest.empty_queue()
    await dpytest.message("!datasets", channel=channel, member=user)
    assert dpytest.verify().message().content(
        "Access token not valid."
    ), "The bot did not respond with the expected message when an invalid token is used."

    # Check command in a guild with valid token and embed response
    await dpytest.empty_queue()
    await dpytest.message(f"!token {user_token}", dm)
    await dpytest.empty_queue()
    await dpytest.message("!datasets", channel=channel, member=user)

    # Verify the embed response
    response = dpytest.get_message()  # Get the bot's response
    assert response.embeds, "The bot did not respond with an embed."

    # Access the first embed
    embed = response.embeds[0]
    assert embed.title == "List of Datasets", "The embed title is incorrect."
    print(embed.fields[0])
    
    assert embed.fields[0].name == "Sample dataset 3", "The embed name is incorrect."
    assert "Description for dataset 3" in embed.fields[0].value, "The embed description is incorrect."


@pytest.mark.asyncio
async def test_search_command_no_token(bot):
    channel = bot.guilds[0].text_channels[0]
    user = bot.guilds[0].members[0]

    # Check command when the user has not registered a token
    await dpytest.message("!search test", channel=channel, member=user)
    assert dpytest.verify().message().contains().content(
        "You have not registered your token"
    ), "The bot did not respond with the expected message when no token used."
    
    
@pytest.mark.asyncio
async def test_search_command_invalid_token(bot):
    channel = bot.guilds[0].text_channels[0]
    user = bot.guilds[0].members[0]

    # Check command when an invalid token is used
    dm = await user.create_dm()
    await dpytest.message("!token false_token", dm)
    await dpytest.empty_queue()
    await dpytest.message("!search test", channel=channel, member=user)
    assert dpytest.verify().message().content(
        "Access token not valid."
    ), "The bot did not respond with the expected message when an invalid token is used."
    
    
@pytest.mark.asyncio
async def test_search_command_no_query(bot):
    channel = bot.guilds[0].text_channels[0]
    user = bot.guilds[0].members[0]

    # Check command when no query is provided
    dm = await user.create_dm()
    await dpytest.message("!token false_token", dm)
    await dpytest.empty_queue()
    await dpytest.message("!search", channel=channel, member=user)
    assert dpytest.verify().message().content(
        "Please provide a query."
    ), "The bot did not respond with the expected message when no query is provided."
    

@pytest.mark.asyncio
async def test_search_command_valid_query(bot):
    channel = bot.guilds[0].text_channels[0]
    user = bot.guilds[0].members[0]

    # Check command when a valid query is provided
    dm = await user.create_dm()
    await dpytest.message(f"!token {user_token}", dm)
    await dpytest.empty_queue()
    await dpytest.message("!search test", channel=channel, member=user)

    # Verify the embed response
    response = dpytest.get_message()  # Get the bot's response
    assert response.embeds, "The bot did not respond with an embed."

    # Access the first embed
    embed = response.embeds[0]
    assert embed.title == "List of Datasets", "The embed title is incorrect."
    print(embed.fields[0])
    
    assert embed.fields[0].name == "Test dataset for discord bot", "The embed name is incorrect."
    assert "Test dataset for testing explore command in discord bot." in embed.fields[0].value, "The embed description is incorrect."
    
    
@pytest.mark.asyncio
async def test_search_command_no_results(bot):
    channel = bot.guilds[0].text_channels[0]
    user = bot.guilds[0].members[0]

    # Check command when a query returns no results
    dm = await user.create_dm()
    await dpytest.message(f"!token {user_token}", dm)
    await dpytest.empty_queue()
    await dpytest.message("!search invalid_query", channel=channel, member=user)
    assert dpytest.verify().message().content(
        "No datasets found."
    ), "The bot did not respond with the expected message when no results were found."