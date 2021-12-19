import os
import random
from discord import user
#import psycopg2
#from psycopg2 import Error

import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from discord.ext.commands.errors import MissingPermissions

TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix = '$')

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

@bot.command(name = 'hello', help = 'Random greeting!')
@commands.cooldown(1, 30, commands.BucketType.user)
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

@bot.command(name = 'quote', help = 'Sends a random message selected from the last 1000 messages!')
@commands.cooldown(1, 30, commands.BucketType.user)
async def quote(ctx):
    messages = await ctx.history(limit = 1000).flatten()
    msg = random.choice(messages)
    await ctx.send(f'{msg.content} - {str(msg.author)}\n{str(msg.jump_url)}')

@bot.command(name = '')

bot.run(TOKEN)
