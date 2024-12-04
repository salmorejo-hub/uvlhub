import discord
from src.util.token import get_token
from src.util.embeds import embed_dataset, PaginationView
from src.util.api_request import request_api
import requests


async def setup_dataset_commands(client, session):

    @client.command(help="List all datasets")
    async def datasets(ctx):
        url = "http://127.0.0.1:5000/api/dataset"
        user = ctx.message.author

        token = get_token(user, session)
        if token is None:
            await ctx.send("You have not registered your token. Use the command `token_config` to register your token.")
            return

        try:
            data = request_api(url, token)
            view = PaginationView(data)
            view.children[1].disabled = len(data) == 1  # Deshabilitar "Next" si hay solo una página
            await ctx.send(embed=embed_dataset(data[0]), view=view)
        except requests.exceptions.HTTPError as http_err:
            if http_err.response.status_code == 401:  # Manejo específico para 401
                await ctx.send("Access token not valid.")
            else:
                await ctx.send(f"An HTTP error occurred: {http_err.response.status_code} {http_err.response.reason}")
        except Exception as e:
            await ctx.send(f"An unexpected error occurred: {e}")
