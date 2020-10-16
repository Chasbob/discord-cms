import logging
import asyncio
from typing import Optional

import discord
from discord.ext import commands, tasks

from ..util import config
from .updater import UpdateCog
from sqlalchemy.orm import Session

from orm import crud
from orm.crud.database import SessionLocal, engine

crud.models.Base.metadata.create_all(bind=engine)

logger = logging.getLogger('cms-bot')
command_prefix = config.config['discord']['command_prefix']
bot: commands.Bot = commands.Bot(command_prefix='-', pass_context=True)


def start():
    global bot
    logger.info("Starting bot...")
    bot.run(config.config['discord']['token'])


@bot.command(name="create")
async def create_message(
    ctx: commands.Context,
    *,
    channel: discord.TextChannel = None,
):
    if channel == None:
        channel = ctx.channel
    db = SessionLocal()
    guild = crud.Guild.get_or_create(db, id=str(ctx.guild.id))
    user = crud.User.get_or_create(db, id=str(ctx.author.id))
    content = f"by: {user.username}"
    logger.info(
        f"creating user={ctx.author}, channel={channel}, content={content}")
    msg: discord.Message = await channel.send(content=content)
    crud.Message.create(db,
                        channel=str(channel.id),
                        id=str(msg.id),
                        user_id=str(user.id),
                        user=user,
                        guild_id=guild.id,
                        guild=guild,
                        name='.',
                        content=content)
    db.close()


@bot.event
async def on_ready():
    guild: discord.Guild
    db = SessionLocal()
    for guild in bot.guilds:
        logger.info(f"Logged into {guild}")
        g = crud.Guild.get_or_create(db, id=str(guild.id))
        logger.info(g.__dict__)
        g.name = guild.name
    logger.info("Bot online")
    db.commit()
    db.close()
    bot.add_cog(UpdateCog(bot=bot))


@bot.after_invoke
async def after_invoke(ctx):
    await ctx.message.delete()
