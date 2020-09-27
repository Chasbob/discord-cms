import logging
from typing import Optional

import discord
from discord.ext import commands

from discord_interactive import Page, Help

from ..util import config
from sqlalchemy.orm import Session

from .. import crud, models
from ..database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

logger = logging.getLogger('cms-bot')
command_prefix = config.config['discord']['command_prefix']
bot: commands.Bot = commands.Bot(command_prefix=command_prefix)

# Define each page
root = Page('Welcome !\n')
page_1 = Page('This is page 1')
page_2 = Page('This is page 2')

# Link pages together
page_1.link(page_2,
            description='Click this icon to access page 2',
            reaction=':regional_indicator_c:')
root.link(page_1, description='Click this icon to access page 1')

# Set the root page as the root of other page (so user can come back with a specific reaction)
root.root_of([page_1, page_2])
h = Help(bot, root)

# class PostConverter(commands.Converter):
#     async def convert(self, ctx, argument):


class UserConverter(commands.Converter):
    async def convert(self, ctx, argument):
        db = SessionLocal()
        user = crud.User.get_or_create(db, id=int(ctx.author.id))
        db.close()
        return user


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


@bot.command(name="int")
async def view_int(ctx: commands.Context):
    await h.display(ctx.author)


@bot.command(name="create")
async def create_message(ctx: commands.Context,
                         channel: discord.TextChannel = 0,
                         post_name: str = ''):
    db = SessionLocal()
    user = crud.User.get_or_create(db, id=int(ctx.author.id))
    logger.info(channel)
    msg: discord.Message = await channel.send(content='.')
    crud.Post.create(db,
                     channel=channel.id,
                     message=msg.id,
                     user_id=user.id,
                     name=post_name)
    await ctx.author.send(f"created message {msg.jump_url}")
    db.close()


@bot.command(name="check")
async def check_message(ctx: commands.Context, message: discord.Message):
    db = SessionLocal()
    post = crud.Post.get(db, message=message.id)
    logger.info(f"post={post}")
    logger.info(message)
    await ctx.send(f"id={message.id}, link={message.jump_url}")
    db.close()


@bot.command(name="list")
async def list_posts(ctx: commands.Context, *, user: UserConverter):
    db = SessionLocal()
    # user = crud.User.get_or_create(db, id=int(ctx.author.id))
    posts = crud.Post.list(db, user=user)
    for post in posts:
        ch = discord.TextChannel = ctx.guild.get_channel(int(post.channel))
        message: discord.Message = await ch.fetch_message(int(post.message))
        await ctx.send(message.jump_url)
    db.close()


@bot.command(name="edit")
async def edit_post(ctx: commands.Context, message_id: int, content: str):
    db = SessionLocal()
    user = crud.User.get_or_create(db, id=int(ctx.author.id))
    post = crud.Post.get(db, message=message_id)
    if user != post.user:
        await ctx.send(f"Can't edit someone else's message!")
    logger.info(f"post={post}")
    message: discord.Message = await ctx.guild.get_channel(int(
        post.channel)).fetch_message(int(post.message))
    # if message.author != bot:
    #     await ctx.send(f"I can only edit messages I sent!")
    #     return
    await message.edit(content=content)
    logger.info(message)


@bot.after_invoke
async def after_invoke(ctx):
    await ctx.message.delete()


@bot.event
async def on_ready():
    guild: discord.Guild
    for guild in bot.guilds:
        logger.info(f"Logged into {guild}")
    logger.info("Bot online")
