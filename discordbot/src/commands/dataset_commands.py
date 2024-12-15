import discord
from discordbot.src.util.token import get_token
from discordbot.src.util.embeds import embed_dataset, PaginationView
from discordbot.src.util.api_request import request_api
import requests
import os


async def setup_dataset_commands(client, session):

    @client.command(help="List all datasets")
    async def datasets(ctx):
        url = f"{os.getenv('API_URL')}dataset"
        user = ctx.message.author

        token = get_token(user, session)
        if token is None:
            await ctx.send("You have not registered your token. Use the command `token_config` to register your token.")
            return

        try:
            data = request_api(url, token)
            view = PaginationView(data)
            view.children[1].disabled = len(data) == 1
            await ctx.send(embed=embed_dataset(data[0]), view=view)
        except requests.exceptions.HTTPError as http_err:
            if http_err.response.status_code == 401:
                await ctx.send("Access token not valid.")
            else:
                await ctx.send(f"An HTTP error occurred: {http_err.response.status_code} {http_err.response.reason}")
        except Exception as e:
            await ctx.send(f"An unexpected error occurred: {e}")

    @client.command(help="Search datasets by query")
    async def search(ctx, query=None):
        url = f"{os.getenv('API_URL')}explore/{query}"
        user = ctx.message.author

        token = get_token(user, session)
        if token is None:
            await ctx.send("You have not registered your token. Use the command `token_config` to register your token.")
            return

        if query is None:
            await ctx.send("Please provide a query.")
            return

        try:
            data = request_api(url, token)
            if len(data) == 0:
                await ctx.send("No datasets found.")
            view = PaginationView(data)
            view.children[1].disabled = len(data) == 1
            await ctx.send(embed=embed_dataset(data[0]), view=view)
        except requests.exceptions.HTTPError as http_err:
            if http_err.response.status_code == 401:
                await ctx.send("Access token not valid.")
            else:
                await ctx.send(f"An HTTP error occurred: {http_err.response.status_code} {http_err.response.reason}")
        except Exception as e:
            await ctx.send(f"An unexpected error occurred: {e}")
