import asyncio
import logging
import os
import discord

logger = logging.getLogger(__name__)
client = discord.Client()
asyncio.create_task(client.login(os.getenv('DISCORD_BOT_TOKEN'), bot=True))


async def guilds():
    # return [x.id for x in client.guilds]
    await client.login(os.getenv('DISCORD_BOT_TOKEN'), bot=True)
    guilds = client.guilds
    await client.logout()
    logger.warning(guilds)
    return guilds
