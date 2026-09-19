# memory.py  - responsible of storing and retrieving the bot's memory, such as the last X strings read from a channel.

from collections import deque
import settings

class ServerMemory:

    def __init__(self, max_tokens=settings.MEMORY_SIZE):
        self.max_tokens = max_tokens
        self.tokens = deque(maxlen=max_tokens)

    def add_message(self, message):
        new_tokens = message.content.split()

        for token in new_tokens:
            self.tokens.append(token)

    def get_memory(self):
        return list(self.tokens)

    def get_size(self):
        return len(self.tokens)