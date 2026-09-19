# bot.py - responsible for the bot's main functionality, such as connecting to Discord, reading messages, and sending messages.

import discord
import config

from memory.memory import ServerMemory
from genai.genai import generate_messages
memory = ServerMemory()

#invite link: https://discord.com/oauth2/authorize?client_id=1550582722555019435&permissions=120832&integration_type=0&scope=bot

class Client(discord.Client):
    async def on_ready(self): 
        print(f'Logged in as {self.user}')
    async def on_message(self, message): 
        if message.author == self.user:
            return
        print(f'Message from {message.author}: {message.content}')

        #placeholder stuff to test the bot's functionality, will be replaced with actual functionality later

        memory.add_message(message) # this adds a message into the bot's memory

        if 'stfu' in message.content:
            await message.channel.send('shut the fuck up')

        elif 'bacon when the' in message.content:
            await message.channel.send('https://cdn.discordapp.com/emojis/992779523730972693.webp?size=96')

        elif 'biology' in message.content:
            await message.channel.send('https://cdn.discordapp.com/attachments/727679310109868033/907389719380389908/biology.mp4?ex=6aafaf47&is=6aae5dc7&hm=aa2b7266ec20a7d5862a274f7afd94f31fcf63c95933718c5c2107a4c7578ada&')

        elif message.content.startswith('genai'):
            await message.channel.send('<@974297735559806986>')
        elif message.content == '!memory':
            stored_memory = memory.get_memory()
            output = "\n".join(stored_memory)
            await message.channel.send(output)

        elif message.content == '!garbage':
            stored_memory = memory.get_memory()

            output = generate_messages(stored_memory)

            if output:
                await message.channel.send(output)

intents = discord.Intents.default() 
intents.message_content = True 
intents.typing = True 

client = Client(intents=intents)
client.run(config.TOKEN) 

