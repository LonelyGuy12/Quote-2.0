import cogs.currency as currency

import os
import random
from discord import user
import math
import fractions
import asyncpg
from asyncpg import create_pool

import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from discord.ext.commands.errors import MissingPermissions
from discord.colour import Color
from discord.ext.commands.core import command
from discord.utils import get

TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix = '$')

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')    

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

async def create_db_pool():
    bot.pg_con = await asyncpg.create_pool(host = 'ec2-52-18-185-208.eu-west-1.compute.amazonaws.com', database = 'dd7okavdoaf3n5', user = 'wgaoxwcemfkpcz', port = '5432', password = '8052e09f5059c1e77834898b8f0e41937b0ae02efb3cbdfb9928ab3fccc3872b')

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"This command is on cooldown! You can use it again in {round(error.retry_after, 2)} seconds.")

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing required argument/s. Use $help [command] to view the required arguments.")
    
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"Missing required permisions, please check that you have the permission/s to perform this command.")

@commands.cooldown(1, 30, commands.BucketType.user)
@bot.command(name = 'hello', help = 'Random greeting!')
async def hello(ctx):
    greetings = [
        'Hello!',
        'Sup!',
        'Hi',
        'こんにちは!',
        '你好!',
    ]

    response = random.choice(greetings)
    await ctx.send(response)

@commands.cooldown(1, 8, commands.BucketType.user)
@bot.command(name = 'quote', help = 'Sends a random message selected from the last 1000 messages!')
async def quote(ctx):
    messages = await ctx.history(limit = 1000).flatten()
    msg = random.choice(messages)
    while msg.content.startswith("$") or msg.content.startswith("!") or msg.content.startswith("p!") or msg.author.bot:
        msg = random.choice(messages)

    await ctx.send(f'{msg.content} - {str(msg.author)}\n{str(msg.jump_url)}')

@commands.cooldown(1, 10, commands.BucketType.user)
@bot.command(name = 'yn', help = 'Yes or no')
async def yn(ctx):
    decision = ['yes', 'no']
    await ctx.send(random.choice(decision))

@commands.cooldown(1, 10, commands.BucketType.user)
@bot.command(name = 'randfloat', help = 'Generates a random float between 0 and 1.')
async def randfloat(ctx):
    num = random.random()
    await ctx.send(num)

@commands.cooldown(1, 10, commands.BucketType.user)
@bot.command(name = 'randnum', help = 'Generates a random integer between the range specified.')
async def randnum(ctx, num1, num2):
    num = random.randint(int(num1), int(num2))
    await ctx.send(num)

@commands.cooldown(1, 10, commands.BucketType.user)
@bot.command(name = 'rad', help = 'Convert degrees to radians')
async def randnum(ctx, arg):
    num = fractions.Fraction(arg * 1/180).limit_denominator()
    await ctx.send(str(num) + 'π')

@commands.cooldown(1, 60, commands.BucketType.user)
@bot.command(name = 'hug', help = 'Hug a person whom you specify!')
async def hug(ctx, user, *, reason):
    hug_gifs = [
    'https://tenor.com/view/mochi-peachcat-mochi-peachcat-hug-pat-gif-19092449',
    'https://tenor.com/view/hugs-sending-virtual-hugs-loading-gif-8158818',
    'https://tenor.com/view/milk-and-mocha-bear-couple-line-hug-cant-breathe-gif-12687187',
    'https://tenor.com/view/hug-love-hi-bye-cat-gif-15999080',
    'https://tenor.com/view/ghosthug-gif-7626784',
    'https://tenor.com/view/anime-hug-sweet-love-gif-14246498',
    'https://tenor.com/view/seal-hug-cute-love-hug-tight-gif-16412489',
    'https://tenor.com/view/virtual-hug-penguin-love-heart-gif-14712845',
    'https://tenor.com/view/hug-anime-gif-15793126',
    'https://tenor.com/view/anime-anime-love-hug-love-sweet-gif-16131468',
    'https://tenor.com/view/anime-hug-hearts-hug-bff-gif-13857541',
    'https://tenor.com/view/anime-hug-love-hug-gif-13925386',
    'https://tenor.com/view/love-cats-cat-cute-hug-love-gif-16191958',
    'https://tenor.com/view/cat-hug-dog-annoyed-puppy-gif-15579685',
    'https://tenor.com/view/hug-k-on-anime-cuddle-gif-16095203',

    ]
    gif = random.choice(hug_gifs)
    await ctx.send(f"{ctx.author.mention} hugged {user} {reason}.\n{gif}")

bot.loop.run_until_complete(create_db_pool())
bot.run(TOKEN)
