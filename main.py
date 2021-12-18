import os
import random
#import psycopg2

import discord
from discord.ext import commands

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix = '$')

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')


@bot.command(name = 'hello')
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


bot.run(TOKEN)
