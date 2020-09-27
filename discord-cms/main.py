import logging

from .util import log
log.init()

from .util import config
config.init()

from .bot import bot

logger = logging.getLogger('cms-bot')
VERSION = '0.1.0-beta.1'


def init():
    logger.info(f'Starting cms-bot v{VERSION}')
    bot.start()
