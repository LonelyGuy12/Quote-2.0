import os
import random
from discord import user
#import psycopg2
#from psycopg2 import Error

import discord
from discord.ext import commands
from discord.ext.commands.errors import MissingPermissions

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

@bot.command(name = 'slap', help = 'Slaps the person whom you specify.')
async def slap(ctx, user, *, reason):
    slap_gifs = [
        'https://tenor.com/view/nope-stupid-slap-in-the-face-phone-gif-15151334',
        'https://tenor.com/view/baka-slap-huh-angry-gif-15696850',
        'https://tenor.com/view/pikachu-slap-fight-mad-no-gif-16415016',
        'https://tenor.com/view/slap-cat-gif-11314821',
        'https://tenor.com/view/face-slap-gif-18146312',
        'https://tenor.com/view/spank-slap-butt-anime-gif-17784858',
        'https://c.tenor.com/D8hEg0H26hAAAAAM/cat-smack.gif',
        'https://c.tenor.com/mMGM1FfaXLgAAAAM/slap-cat.gif',
        'https://tenor.com/view/mochicat-slap-cute-adorable-gif-15575210',

    ]
    try:
        await ctx.message.delete()
    except Exception:
        pass

    await ctx.send('{0.author.mention} slapped {1} {2}'.format(ctx, user, reason))
    await ctx.send(random.choice(slap_gifs))

@bot.command(name = 'quote', help = 'Sends a random message selected from the last 1000 messages!')
async def quote(ctx):
    messages = await ctx.history(limit = 1000).flatten()
    msg = random.choice(messages)
    await ctx.send(f'{msg.content} - {str(msg.author)}\n{str(msg.jump_url)}')


bot.run(TOKEN)
