import os
import json
import logging

from .log import fatal_error

logger = logging.getLogger('cms-bot')

CONFIG = os.getenv('CONFIG', 'config.json')


def init():
    global config
    logger.info('Loading config...')

    config = {
        "discord": {
            "command_prefix": os.getenv("COMMAND_PREFIX"),
            "token": os.getenv("DISCORD_BOT_TOKEN")
        }
    }
