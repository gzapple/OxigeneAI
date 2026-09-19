# genai.py - responsible for generating random messages
# based on the bot's memory and randomization settings.

import random
import settings


def generate_messages(tokens):

    if not tokens:
        return None

    used_tokens = [
        token for token in tokens
        if len(token) <= settings.MAX_MESSAGE_LENGTH
    ]

    if not used_tokens:
        return None

    token_count = random.randint(
        settings.MIN_GENERATED_TOKENS,
        min(settings.MAX_GENERATED_TOKENS, len(used_tokens))
    )

    select_tokens = random.sample(
        used_tokens,
        token_count
    )

    random.shuffle(select_tokens)

    output = ""

    for token in select_tokens:

        if output == "":
            candidate = token
        else:
            candidate = output + " " + token

        if len(candidate) > settings.MAX_MESSAGE_LENGTH:
            break

        output = candidate

    return output