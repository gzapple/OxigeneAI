# genai.py - responsible for generating random messages based on the bot's memory and the randomization settings.

import random #imports random fucntion library from python

MAX_MESSAGE = 100 #hardcap on the message length amount

def generate_messages(tokens):
    if not tokens:
        return none #

    used_tokens = [
        token for token in tokens
        if len(token) <= MAX_MESSAGE
    ]
    if not used_tokens:
        return None

    token_count = random.randint(1, len(used_tokens))

    select_tokens = random.sample(used_tokens,token_count)

    random.shuffle(select_tokens)

    output = ""

    for token in select_tokens:
        if output == "":
            candidate = token
        else:
            candidate = output+ " " + token
        if len(candidate) >  MAX_MESSAGE:
            break
        output = candidate
    return output