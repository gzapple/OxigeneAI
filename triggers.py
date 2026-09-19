

# triggers.py - responsible for handling triggers, such as when the bot is pinged or mentioned, and responding accordingly.

import discord

MEMORY_STRINGS_PER_PAGE = 256

class MemoryView(discord.ui.View):
    def __init__(self, pages, memory_size, memory_limit):
        super().__init__(timeout=300)

        self.pages = pages
        self.memory_size = memory_size
        self.memory_limit = memory_limit
        self.page = 0

    async def update_message(self, interaction):
        total_pages = len(self.pages)

        embed = discord.Embed(
            title=f"Memory: {self.memory_size} / {self.memory_limit} Tokens",
            description=(
                f"Memory — Page {self.page + 1}/{total_pages}\n\n"
                f"{self.pages[self.page]}"
            )
        )

        await interaction.response.edit_message(
            embed=embed,
            view=self
        )

    @discord.ui.button(label="⏮️", style=discord.ButtonStyle.primary)
    async def first_page(self, interaction, button):
        self.page = 0
        await self.update_message(interaction)

    @discord.ui.button(label="◀️", style=discord.ButtonStyle.primary)
    async def previous_page(self, interaction, button):
        if self.page > 0:
            self.page -= 1
        await self.update_message(interaction)

    @discord.ui.button(label="▶️", style=discord.ButtonStyle.primary)
    async def next_page(self, interaction, button):
        if self.page < len(self.pages) - 1:
            self.page += 1
        await self.update_message(interaction)

    @discord.ui.button(label="⏭️", style=discord.ButtonStyle.primary)
    async def last_page(self, interaction, button):
        self.page = len(self.pages) - 1
        await self.update_message(interaction)


async def handle_message(message, memory, generate_messages):
    # check message.content
    # check if its a .o command
    # check permissions
    # check channel settings
    # handle command
    # handle special triggers
    # handle mentions and replies
    # generate response
    # send response
    if message.content == '.o memory':
        stored_memory = memory.get_memory()

        memory_size = memory.get_size()
        memory_limit = memory.max_tokens

        output = "\n".join(stored_memory)

        if not output:
            await message.channel.send(
                f"Memory: {memory_size} / {memory_limit} Tokens\n\n"
                "Memory is currently empty."
            )
            return

        pages = [
            output[i:i + MEMORY_STRINGS_PER_PAGE]
            for i in range(0, len(output), MEMORY_STRINGS_PER_PAGE)
        ]

        view = MemoryView(
            pages,
            memory_size,
            memory_limit
        )

        embed = discord.Embed(
            title=f"Memory: {memory_size} / {memory_limit} Tokens",
            description=(
                f"Memory — Page 1/{len(pages)}\n\n"
                f"{pages[0]}"
            )
        )

        await message.channel.send(
            embed=embed,
            view=view
        )

    elif message.content == '.o send':
        stored_memory = memory.get_memory()

        output = generate_messages(stored_memory)

        if output:
            await message.channel.send(output)
