# bot.py - responsible for the bot's main functionality, such as connecting to Discord, reading messages, and sending messages.

import discord
import config
import settings

from triggers import handle_message

from memory.memory import ServerMemory
from genai.genai import generate_messages
memory = ServerMemory()



message_counter = 0

#invite link: https://discord.com/oauth2/authorize?client_id=1550582722555019435&permissions=120832&integration_type=0&scope=bot

class Client(discord.Client):
    async def on_ready(self): 
        print(f'Logged in as {self.user}')

    async def on_message(self, message): 
        global message_counter
        if message.author == self.user:
            return
        print(f'Message from {message.author}: {message.content}')

        memory.add_message(message)
        message_counter += 1

        await handle_message(message, memory, generate_messages)


        if self.user in message.mentions:
            stored_memory = memory.get_memory()
            output = generate_messages(stored_memory)
            if output:
                await message.channel.send(output)
            return
        
        if message_counter >= settings.MESSAGE_INTERVAL:
            stored_memory = memory.get_memory()
            output = generate_messages(stored_memory)
            if output:
                await message.channel.send(output)

            message_counter = 0

intents = discord.Intents.default() 
intents.message_content = True 
intents.typing = True 

client = Client(intents=intents)
client.run(config.TOKEN) 

