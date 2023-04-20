import os
import discord
from discord import Intents
from discord import Streaming
from discord.utils import get
from discord.ext import commands
from config import *
import random
# from replit import db
from keep_awake import keep_awake
import logging

### ---------- TODO ---------- ###
"""
 - Add a database element storing suggestions user can add with !suggest

 - Add API where you can request a random image

"""
### ---------- INSTANCE BOT ---------- ###

# Initialize token from env
BOT_TOKEN = os.environ['TOKEN']

# Initialize intents
intents = Intents.all()

# Initialize bot
bot = commands.Bot(command_prefix="!", intents=intents)


# On-Ready
@bot.event
async def on_ready():
  print('Logged in as BathBot')


# On-Live
@bot.event
async def on_member_update(before, after):
  if after.guild.id == 509048163802415128:  # "Copy ID" for Bath discord
    if before.activity == after.activity:
      return

    role = get(after.guild.roles, id=1062883441810612306)  #"Copy ID" for role "Streamer" in Bath discord
    channel = get(after.guild.channels, id=728821228806340678)  #"Copy ID" for going-live channel in Bath discord

    async for message in channel.history(limit=200):
      if before.mention in message.content and "is now streaming" in message.content:
        if isinstance(after.activity, Streaming):
          return

    if isinstance(after.activity, Streaming):
      await after.add_roles(role)
      stream_url = after.activity.url
      stream_url_split = stream_url.split(".")
      streaming_service = stream_url_split[1]
      streaming_service = streaming_service.capitalize()
      await channel.send(f"@everyone\n\n:red_circle: **LIVE** \n\nBathinjan is now streaming on Twitch!\n\n{stream_url}")
      
    elif isinstance(before.activity, Streaming):
      await after.remove_roles(role)
      async for message in channel.history(limit=200):
        if before.mention in message.content and "is now streaming" in message.content:
          await message.delete()
        else:
          return


print("Server Running")

# Logging
logging.basicConfig(level=logging.INFO)

### ---------- COMMANDS ---------- ###

# !hello
@bot.command()
async def hello(ctx):
    await ctx.send("Hiya!")

# !ping
@bot.command()
async def ping(ctx):
    await ctx.send(f"Current latency: {round(bot.latency) * 1000} milliseconds"
                   )
# !8ball
@bot.command(aliases=["8ball"])
async def eight_ball(ctx, *, question):
    responses = [
        'Yeah dude.',
        'Absolutely.',
        'Uhhhh sure.',
        'Mmmmyep.',
        'Why not.',
        'I\'m gonna say yes.',
        'Probably.',
        'Yeah sure.',
        'Yeah.',
        'I forgor.',
        'Reply hazy, try again immediately.',
        'Ask me again immediately.',
        'I really, REALLY shouldn\'t tell you...',
        'No idea dude.',
        'Concentrate harder and ask me nicely.',
        'Don\'t put money on that one, champ.',
        'I\'m gonna say no.',
        'My sources say : nahhh.',
        'Outlook isn\'t great, is it...',
        'Absolutely not.',
    ]

    if question:
        await ctx.send(
            f"You asked: {question} \nMy Answer: {random.choice(responses)}")
    else:
        await ctx.send(
            "You gotta ask a question for the mediocre 8-ball to answer you! (missing second arg 'question'"
        )


# !flipacoin
@bot.command()
async def flipacoin(ctx):
    response = [
        'Heads',
        'Tails',
    ]
    await ctx.send(f"{random.choice(response)}")


# !commands
# probably a better way to implement this, but for now it's coded by hand ¯\_(ツ)_/¯
@bot.command()
async def commands(ctx):
    await ctx.send(
        "The following commands are available:\n\n!8ball\n!commands\n!flipacoin\n!hello\n!ping\n!test"
    )

### ---------- REACTION ROLES ---------- ###

# Adding roles
@bot.event
async def on_raw_reaction_add(payload):

    # message ID of roles message in #add-your-pronouns channel
    messageID = 976979042836295771

    # making sure it matches up with the user's reactive message
    if messageID == payload.message_id:

        # obtain member, guild and emoji from payload
        member = payload.member
        guild = member.guild
        emoji = payload.emoji.name

        # because the emoji names don't match exactly with roles
        # use the emoji name, then iterate through guild roles to find the match
        if emoji == 'sheher':
            role = discord.utils.get(guild.roles, name="she/her")
        if emoji == 'hehim':
            role = discord.utils.get(guild.roles, name="he/him")
        if emoji == 'theythem':
            role = discord.utils.get(guild.roles, name="they/them")
        if emoji == 'anyall':
            role = discord.utils.get(guild.roles, name="any/all")
        if emoji == 'ask':
            role = discord.utils.get(guild.roles, name="ask")
        if emoji == 'other':
            role = discord.utils.get(guild.roles, name="other")

        # check the role isn't null before add
        if role is not None:
            await member.add_roles(role)


# Deleting roles
@bot.event
async def on_raw_reaction_remove(payload):

    messageID = 976979042836295771

    if messageID == payload.message_id:

        guild = await (bot.fetch_guild(payload.guild_id))

        emoji = payload.emoji.name

        if emoji == 'sheher':
            role = discord.utils.get(guild.roles, name="she/her")
        if emoji == 'hehim':
            role = discord.utils.get(guild.roles, name="he/him")
        if emoji == 'theythem':
            role = discord.utils.get(guild.roles, name="they/them")
        if emoji == 'anyall':
            role = discord.utils.get(guild.roles, name="any/all")
        if emoji == 'ask':
            role = discord.utils.get(guild.roles, name="ask")
        if emoji == 'other':
            role = discord.utils.get(guild.roles, name="other")

        member = await (guild.fetch_member(payload.user_id))

        if member is not None:
            await member.remove_roles(role)
        else:
            print("Member not found.")

### ---------- WEBSERVER PING ---------- ###
# continuous Ping for bot availability when offline
keep_awake()

### ---------- RUN BOT ---------- ###
bot.run(BOT_TOKEN)
