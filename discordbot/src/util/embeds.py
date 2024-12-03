import discord
from discord.ui import View, Button

def get_embed_authors(authors):
    names=""
    for author in authors:
        names += author['name'] + ", "
    return names[:-2]

def get_embed_tags(tags):
    names=""
    for tag in tags:
        names += tag + ", "
    return names[:-2]

def get_embed_files(files):
    message = ""
    for file in files:
        message += (
            f"- **Name:** {file['name']}  \n"
            f"  **Size:** {file['size_in_human_format']}  \n"
            f"  **[View file]({file['url']})**  \n\n"
        )
    return message

def embed_dataset(dataset):
    embed = discord.Embed(
        title="List of Datasets",
        description="Here are the available datasets:",
        color=discord.Color.blue()
    )
    dataset_info = (
        f"**Description:** {dataset['description']}\n"
        f"**Authors:** {get_embed_authors(dataset['authors'])}\n"
        f"**Created at:** {dataset['created_at']}\n"
        f"**Tags:** {get_embed_tags(dataset['tags'])}\n"
        f"**Type:** {dataset['publication_type']}\n"
        f"**Size:** {dataset['total_size_in_human_format']}\n"
        f"**[View Dataset]({dataset['url']})**\n\n"
        f"**Number of files:** {dataset['files_count']}\n"
        f"{get_embed_files(dataset['files'])}\n"            
        
    )
    embed.add_field(name=dataset['title'], value=dataset_info, inline=False)
        
    return embed


class PaginationView(View):
        def __init__(self, pages):
            super().__init__()
            self.page_index = 0
            self.pages = pages

        @discord.ui.button(label="Previous", style=discord.ButtonStyle.primary, disabled=True)
        async def previous(self, interaction: discord.Interaction, button: Button):
            self.page_index -= 1
            self.children[0].disabled = self.page_index == 0
            self.children[1].disabled = self.page_index == len(self.pages) - 1
            await interaction.response.edit_message(embed=embed_dataset(self.pages[self.page_index]), view=self)

        @discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
        async def next(self, interaction: discord.Interaction, button: Button):
            self.page_index += 1
            self.children[0].disabled = self.page_index == 0
            self.children[1].disabled = self.page_index == len(self.pages) - 1
            await interaction.response.edit_message(embed=embed_dataset(self.pages[self.page_index]), view=self)