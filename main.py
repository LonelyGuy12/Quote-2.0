import os
import random
from discord import user
import math
import fractions
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

@bot.command(name = 'rps', help = 'Play rock paper scissors!')
@commands.cooldown(1, 5, commands.BucketType.user)
async def rps(ctx, choice):
    rps = str(random.choices(['rock', 'paper', 'scissors'], k = 1)[0])
    if rps == choice:
        await ctx.send(f"{str.capitalize(rps)}. It's a tie!")

    elif rps == 'rock' and choice == 'paper':
        await ctx.send(f"{str.capitalize(rps)}. You win!")
        
    elif rps == 'rock' and choice == 'scissors':
        await ctx.send(f"{str.capitalize(rps)}. You lose...")

    elif rps == 'paper' and choice == 'scissors':
        await ctx.send(f"{str.capitalize(rps)}. You win!")
         
    elif rps == 'paper' and choice == 'rock':
        await ctx.send(f"{str.capitalize(rps)}. You lose...")

    elif rps == 'scissors' and choice == 'rock':
        await ctx.send(f"{str.capitalize(rps)}. You win!")
    
    elif rps == 'scissors' and choice == 'paper':
        await ctx.send(f"{str.capitalize(rps)}. You lose...")
        
    else:
        await ctx.send('Invalid input! Please choose from: paper, scissors and rock.')

@bot.command(name = 'quiz', help = 'Test your knowledge in multiple quiz categories! At the moment, the categories are: quick maths.')
@commands.cooldown(1, 15, commands.BucketType.user)
async def quiz(ctx, category):
    if category == "quick_maths":
        operator = random.randint(1, 3)
        if operator == 1:
            first = random.randint(0, 250)
            second = random.randint(0, 250)
            question = str(first) + " + " + str(second)
            answer = int(first) + int(second)

        elif operator == 2:
            first = random.randint(0, 250)
            second = random.randint(0, 250)
            question = str(first) + " - " + str(second)
            answer = int(first) - int(second)

        elif operator == 3:
            first = random.randint(0, 250)
            second = random.randint(0, 10)
            question = str(first) + " * " + str(second)
            answer = int(first) * int(second)

        await ctx.send(question)
                
        def check(msg):
            return msg.channel == ctx.channel and msg.author == ctx.author

        msg = await bot.wait_for('message', check=check)
        try:
            if isinstance(int(msg.content), int) == True:  
                if int(msg.content) == answer:
                    await ctx.send('Correct {.author.mention}!'.format(msg))
                            
                else:
                    await ctx.send('Incorrect {.author.mention}... The correct answer was '.format(msg) + str(answer) + '.')
        except ValueError:
            await ctx.send('Invalid response {.author.mention}! The correct answer was '.format(msg) + str(answer) + '.')

@bot.command(name = 'yn', help = 'Yes or no')
@commands.cooldown(1, 10, commands.BucketType.user)
async def yn(ctx):
    decision = ['yes', 'no']
    await ctx.send(random.choice(decision))

@bot.command(name = 'randfloat', help = 'Generates a random float between 0 and 1.')
@commands.cooldown(1, 10, commands.BucketType.user)
async def randfloat(ctx):
    num = random.random()
    await ctx.send(num)

@bot.command(name = 'randnum', help = 'Generates a random integer between the range specified.')
@commands.cooldown(1, 10, commands.BucketType.user)
async def randnum(ctx, num1, num2):
    num = random.randint(int(num1), int(num2))
    await ctx.send(num)

@bot.command(name = 'rad', help = 'Convert degrees to radians')
@commands.cooldown(1, 10, commands.BucketType.user)
async def randnum(ctx, arg):
    num = fractions.Fraction(arg * 1/180).limit_denominator()
    await ctx.send(str(num) + 'π')

@bot.command(name = 'hug', help = 'Hug a person whom you specify!')
@commands.cooldown(1, 60, commands.BucketType.user)
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


bot.run(TOKEN)
