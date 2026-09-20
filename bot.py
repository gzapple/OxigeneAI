# bot.py - responsible for the bot's main functionality, such as connecting to Discord, reading messages, and sending messages.

import discord
import config
import settings

from triggers import handle_message

from memory.memory import ServerMemory
from genai.genai import generate_messages
from server_settings.settings_manager import get_channel_settings

memories = {}
message_counters = {}

def get_memory(guild_id, channel_id, memory_size):
    if guild_id not in memories:
        memories[guild_id] = {}

    if channel_id not in memories[guild_id]:
        memories[guild_id][channel_id] = ServerMemory(memory_size)

    return memories[guild_id][channel_id]

#invite link: https://discord.com/oauth2/authorize?client_id=1550582722555019435&permissions=120832&integration_type=0&scope=bot



class Client(discord.Client):
    async def on_ready(self): 
        print(f'Logged in as {self.user}')

    async def on_message(self, message):

        if message.author == self.user:
            return

        print(f'Message from {message.author}: {message.content}')

        current_settings = get_channel_settings(
            message.guild.id,
            message.channel.id
        )

        memory = get_memory(
            message.guild.id,
            message.channel.id,
            current_settings["memory"]
        )

        channel_key = (
            message.guild.id,
            message.channel.id
        )

        if current_settings["read"]:
            memory.add_message(message)

            if channel_key not in message_counters:
                message_counters[channel_key] = 0

            message_counters[channel_key] += 1

        await handle_message(
            message,
            memory,
            generate_messages
        )

intents = discord.Intents.default() 
intents.message_content = True 
intents.typing = True 

client = Client(intents=intents)
client.run(config.TOKEN) 

