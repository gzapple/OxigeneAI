# settings.manager_py - responsible for storing and retrieving Oxigene's server and channel settings.
# located in server_settings folder

import json
import os
import settings

SETTINGS_FILE= "server_settings/server_settings.json"

def load_settings():

    if not os.path.exists(SETTINGS_FILE):
        return {}

    try:
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)

    except (json.JSONDecodeError, FileNotFoundError):
        return {}

server_settings = load_settings()
def save_settings():

    with open(SETTINGS_FILE, "w") as file:
        json.dump(server_settings, file, indent=4)


def get_channel_settings(guild_id, channel_id):

    guild_id = str(guild_id)
    channel_id = str(channel_id)

    if guild_id not in server_settings:
        server_settings[guild_id] = {}

    if channel_id not in server_settings[guild_id]:
        server_settings[guild_id][channel_id] = {
            "read": settings.BOT_READ,
            "enable": settings.BOT_ENABLE,
            "interval": settings.MESSAGE_INTERVAL,
            "memory": settings.MEMORY_SIZE,
            "allow_mentions": settings.ALLOW_BOT_MENTIONS,
            "allow_embeds": settings.ALLOW_CONTENT_EMBEDS,
            "allow_links": settings.ALLOW_LINK_SENT,
            "allow_emoji": settings.ALLOW_EMOJI,
            "allow_images": settings.ALLOW_IMAGE,
            "wipe": False
        }

        save_settings()

    return server_settings[guild_id][channel_id]