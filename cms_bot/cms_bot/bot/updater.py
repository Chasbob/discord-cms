from discord.ext import tasks, commands
import discord
import logging

from cms_bot import crud
from cms_bot.crud.database import SessionLocal


class UpdateCog(commands.Cog):
    def __init__(self, bot):
        self.index = 0
        self.bot = bot
        self.updater.start()
        self.logger = logging.getLogger('cms-bot')

    def cog_unload(self):
        self.updater.cancel()

    @tasks.loop(seconds=1.0)
    async def updater(self):
        db = SessionLocal()
        msgs = crud.Message.list(db)
        db.close()
        for msg in msgs:
            try:
                guild: discord.Guild = await self.bot.fetch_guild(
                    int(msg.guild_id))
                ch_id = int(msg.channel)
                chs = await guild.fetch_channels()
                channel = list(filter(lambda x: x.id == ch_id, chs)).pop()
                message: discord.Message = await channel.fetch_message(
                    int(msg.id))
                if message.content != msg.content:
                    self.logger.info(f"{message.content}!={msg.content}")
                    await message.edit(content=msg.content)
            except:
                self.logger.warning('oopsies')
