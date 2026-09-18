import discord
import config #imports the config.py file, which contains the bot's token. This allows the bot to access the token without hardcoding it into the code, keeping it hidden from anyone who looks at the code.

class Client(discord.Client): #pulls discord client
    async def on_ready(self): #onready is a predefined function that runs when the bot is ready, it iwll run the code inside it when the bot is ready
        print(f'Logged in as {self.user}')
        #self.user is the bot's user object, which contains information about the bot, such as its username and ID. The f-string is used to format the string with the bot's username and ID.
    async def on_message(self, message): #onmessage is a predefined function that runs when a message is sent in a channel the bot has access to. It will run the code inside it when a message is sent.
        print(f'Message from {message.author}: {message.content}')

intents = discord.Intents.default() #creates an instance of the Intents class, which is used to specify which events the bot should listen to. The default() method returns an instance of the Intents class with all events enabled.
intents.typing = True #enables the typing event, which is triggered when a user starts typing in a channel.

client = Client(intents=intents) #creates an instance of the Client class, passing in the intents object as an argument. This allows the bot to listen to the events specified in the intents object.
client.run(config.TOKEN) #imports the TOKEN variable from the config.py file and passes it to the run() method, which starts the bot and connects it to Discord using the provided token.