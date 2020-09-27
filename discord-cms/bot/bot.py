import logging
from typing import Optional

import discord
from discord.ext import commands

from ..util import config
from sqlalchemy.orm import Session

from .. import crud, models
from ..database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

logger = logging.getLogger('cms-bot')
command_prefix = config.config['discord']['command_prefix']
bot: commands.Bot = commands.Bot(command_prefix=command_prefix)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def start():
    global bot
    logger.info("Starting bot...")
    bot.run(config.config['discord']['token'])


@bot.command(name="create")
async def create_message(ctx: commands.Context, channel_id):
    db = SessionLocal()
    user = crud.User.get_or_create(db, id=int(ctx.author.id))
    channel: discord.TextChannel = ctx.guild.get_channel(
        channel_id=int(channel_id))
    logger.info(channel)
    msg: discord.Message = await channel.send(content='.')
    post = crud.Post.create(db,
                            channel=channel_id,
                            message=msg.id,
                            user_id=user.id)
    await ctx.author.send(f"created message {msg.jump_url}")
    db.close()


@bot.command(name="check")
async def check_message(ctx: commands.Context, message_id):
    db = SessionLocal()
    post = crud.Post.get(db, message=message_id)
    logger.info(f"post={post}")
    message: discord.Message = ctx.guild.get_channel(int(
        post.channel)).fetch_message(int(post.message))
    logger.info(message)
    await ctx.send(message.jump_url)
    db.close()


@bot.command(name="list")
async def list_posts(ctx: commands.Context):
    db = SessionLocal()
    user = crud.User.get_or_create(db, id=int(ctx.author.id))
    posts = crud.Post.list(db, user=user)
    for post in posts:
        ch = discord.TextChannel = ctx.guild.get_channel(int(post.channel))
        message: discord.Message = await ch.fetch_message(int(post.message))
        await ctx.send(message.jump_url)
    db.close()


@bot.event
async def on_ready():
    guild: discord.Guild
    for guild in bot.guilds:
        logger.info(f"Logged into {guild}")
    logger.info("Bot online")
