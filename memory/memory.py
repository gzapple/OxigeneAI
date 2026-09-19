# memory.py  - responsible of storing and retrieving the bot's memory, such as the last X strings read from a channel.

class ServerMemory:

    def __init__(self):
        self.tokens = [] 
        self.max_tokens = 1000
        # this is a constructor responsible to create an amount of tokens

    def add_message(self, message):
        new_tokens = message.content.split()

        for token in new_tokens:
            self.tokens.append(token)

    def get_memory(self):
        return self.tokens