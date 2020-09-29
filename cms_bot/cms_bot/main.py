import logging

from cms_bot.util import log
log.init()

from cms_bot.util import config
config.init()

from cms_bot.bot import bot

logger = logging.getLogger('cms-bot')
VERSION = '0.1.0-beta.1'


def init():
    logger.info(f'Starting cms-bot v{VERSION}')
    bot.start()
