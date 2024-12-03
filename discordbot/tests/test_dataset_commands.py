import pytest
import discord.ext.test as dpytest

@pytest.mark.asyncio
async def test_datasets_command(bot):
    channel = bot.guilds[0].text_channels[0]
    user = bot.guilds[0].members[0]

    user_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VyX2VtYWlsIjoidXNlcjFAZXhhbXBsZS5jb20iLCJleHAiOjE3MzY4ODY5NDQsImlhdCI6MTczMzE3MTc0NH0.kB7ESV7-YVC2-I8-aYWztJY3-dDd4bt507O5srmNhqI"

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
    # print("aaaaa\n\n" + embed.fields[0].value)
    assert embed.fields[0].name == "Sample dataset 1", "The embed name is incorrect."
    assert "Description for dataset 1" in embed.fields[0].value, "The embed description is incorrect."
