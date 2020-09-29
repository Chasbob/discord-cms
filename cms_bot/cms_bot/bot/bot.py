import logging
from typing import Optional

import discord
from discord.ext import commands

from cms_bot.util import config
from sqlalchemy.orm import Session

from cms_bot import crud
from cms_bot.crud.database import SessionLocal, engine

crud.models.Base.metadata.create_all(bind=engine)

logger = logging.getLogger('cms-bot')
command_prefix = config.config['discord']['command_prefix']
bot: commands.Bot = commands.Bot(command_prefix='-', pass_context=True)


class DefaultChannelConverter(commands.Converter):
    async def convert(self, ctx: commands.Context, argument):
        if int(argument) == 0:
            return ctx.channel
        else:
            return ctx.guild.get_channel(int(argument))


class UserConverter(commands.Converter):
    async def convert(self, ctx, argument):
        db = SessionLocal()
        user = crud.User.get_or_create(db, id=int(ctx.author.id))
        db.close()
        return user


def start():
    global bot
    logger.info("Starting bot...")
    bot.run(config.config['discord']['token'])


@bot.command(name="create")
async def create_message(
    ctx: commands.Context,
    *,
    channel: DefaultChannelConverter = None,
):
    logger.info("create...")
    db = SessionLocal()
    user = crud.User.get_or_create(db, id=str(ctx.author.id))
    logger.info(f"create -> user={user}")
    if channel == None:
        channel = ctx.channel
    logger.info(channel)
    msg: discord.Message = await channel.send(content='.')
    crud.Message.create(db,
                        channel=str(channel.id),
                        id=str(msg.id),
                        user_id=str(user.id),
                        user=user,
                        name='.',
                        content='.')
    await ctx.author.send(f"created message {msg.jump_url}")
    db.close()


@bot.command(name="check")
async def check_message(ctx: commands.Context, message: discord.Message):
    db = SessionLocal()
    post = crud.Message.get(db, message=message.id)
    logger.info(f"post={post}")
    logger.info(message)
    await ctx.send(f"id={message.id}, link={message.jump_url}")
    db.close()


@bot.command(name="users")
async def list_users(ctx: commands.Context):
    db = SessionLocal()
    users = crud.User.list()
    for user in users:
        logger.info(user)
        await ctx.send(str(user))


@bot.command(name="list")
async def list_posts(ctx: commands.Context):
    db = SessionLocal()
    user = crud.User.get_or_create(db, id=str(ctx.author.id))
    posts = crud.Message.list(db, user=user)
    for post in posts:
        ch = discord.TextChannel = ctx.guild.get_channel(int(post.channel))
        message: discord.Message = await ch.fetch_message(int(post.id))
        await ctx.send(message.jump_url)
    db.close()


@bot.command(name="edit")
async def edit_post(ctx: commands.Context, message_id: int, content: str):
    db = SessionLocal()
    user = crud.User.get_or_create(db, id=int(ctx.author.id))
    post = crud.Message.get(db, message=message_id)
    if user != post.user:
        await ctx.send(f"Can't edit someone else's message!")
    logger.info(f"post={post}")
    message: discord.Message = await ctx.guild.get_channel(int(
        post.channel)).fetch_message(int(post.message))
    await message.edit(content=content)
    logger.info(message)


@bot.event
async def on_ready():
    guild: discord.Guild
    for guild in bot.guilds:
        logger.info(f"Logged into {guild}")
    logger.info("Bot online")
