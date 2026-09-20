# triggers.py - responsible for handling triggers, such as when the bot is pinged or mentioned, and responding accordingly.

import discord
import settings

from server_settings.settings_manager import get_channel_settings

class MemoryView(discord.ui.View):
    def __init__(self, pages, memory_size, memory_limit):
        super().__init__(timeout=300)

        self.pages = pages
        self.memory_size = memory_size
        self.memory_limit = memory_limit
        self.page = 0

    async def update_message(self, interaction):
        total_pages = len(self.pages)

        page_text = "\n".join(self.pages[self.page])

        embed = discord.Embed(
            title=f"Memory: {self.memory_size} / {self.memory_limit} Tokens",
            description=(
                f"Memory — Page {self.page + 1}/{total_pages}\n\n"
                f"{page_text}"
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

CONFIGURATIONS = {
    "read",
    "enable",
    "interval",
    "memory",
    "allow_mentions",
    "allow_embeds",
    "allow_links",
    "allow_emoji",
    "allow_images"
}
def send_config_help():
    return (
        "Usage:\n"
        ".o config [configuration] [attribute]\n\n"
        "Configurations:\n"
        "read\n"
        "enable\n"
        "interval\n"
        "memory\n"
        "allow_mentions\n"
        "allow_embeds\n"
        "allow_links\n"
        "allow_emoji\n"
        "allow_images"
    )


def send_config_attribute_help(configuration):
    boolean_settings = {
        "read",
        "enable",
        "allow_mentions",
        "allow_embeds",
        "allow_links",
        "allow_emoji",
        "allow_images"
    }

    numeric_settings = {
        "interval",
        "memory"
    }

    if configuration in boolean_settings:
        return (
            f"Usage:\n"
            f".o config {configuration} [attribute]\n\n"
            "Attribute:\n"
            "true\n"
            "false"
        )

    if configuration in numeric_settings:
        return (
            f"Usage:\n"
            f".o config {configuration} [attribute]\n\n"
            "Attribute:\n"
            "integer"
        )

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

        if not stored_memory:
            await message.channel.send(
                f"Memory: {memory_size} / {memory_limit} Tokens\n\n"
                "Memory is currently empty."
            )
            return

        pages = [
            stored_memory[i:i + settings.MEMORY_STRINGS_PER_PAGE]
            for i in range(
                0,
                len(stored_memory),
                settings.MEMORY_STRINGS_PER_PAGE
            )
        ]

        view = MemoryView(
            pages,
            memory_size,
            memory_limit
        )

        page_text = "\n".join(pages[0])

        embed = discord.Embed(
            title=f"Memory: {memory_size} / {memory_limit} Tokens",
            description=(
                f"Memory — Page 1/{len(pages)}\n\n"
                f"{page_text}"
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

    elif message.content == '.o status':

        current_settings = get_channel_settings(
            message.guild.id,
            message.channel.id
        )

        embed = discord.Embed(
            title="Oxigene Status",
            description=(
                f"Channel: {message.channel.mention}\n\n"
                f"Read: {'ON' if current_settings['read'] else 'OFF'}\n"
                f"Send: {'ON' if current_settings['enable'] else 'OFF'}\n"
                f"Interval: {current_settings['interval']} messages\n"
                f"Memory: {current_settings['memory']} tokens\n\n"
                f"Links: {'ON' if current_settings['allow_links'] else 'OFF'}\n"
                f"Embeds: {'ON' if current_settings['allow_embeds'] else 'OFF'}\n"
                f"Emojis: {'ON' if current_settings['allow_emoji'] else 'OFF'}\n"
                f"Images: {'ON' if current_settings['allow_images'] else 'OFF'}"
            )
        )

        await message.channel.send(embed=embed)

    elif message.content.startswith('.o config'):
        parts = message.content.split()

        if len(parts) == 2:
            await message.channel.send(send_config_help())
            return

        configuration = parts[2]

        if configuration not in CONFIGURATIONS:
            await message.channel.send(
                "Invalid configuration.\n\n"
                "Available configurations:\n" +
                "\n".join(sorted(CONFIGURATIONS))
            )
            return

        if len(parts) == 3:
            await message.channel.send(
                send_config_attribute_help(configuration)
            )
            return

        attribute = parts[3]

    # actual setting modification will go here later