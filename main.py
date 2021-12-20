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
@commands.cooldown(1, 15, commands.BucketType.user)
async def rps(ctx, arg):
    rps = str(random.choices(['rock', 'paper', 'scissors'], k = 1)[0])
    if rps == arg:
        await ctx.send(f"{str.capitalize(rps)}. It's a tie!")

    elif rps == 'rock' and arg == 'paper':
        await ctx.send(f"{str.capitalize(rps)}. You win!")
        
    elif rps == 'rock' and arg == 'scissors':
        await ctx.send(f"{str.capitalize(rps)}. You lose...")

    elif rps == 'paper' and arg == 'scissors':
        await ctx.send(f"{str.capitalize(rps)}. You win!")
         
    elif rps == 'paper' and arg == 'rock':
        await ctx.send(f"{str.capitalize(rps)}. You lose...")

    elif rps == 'scissors' and arg == 'rock':
        await ctx.send(f"{str.capitalize(rps)}. You win!")
    
    elif rps == 'scissors' and arg == 'paper':
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


bot.run(TOKEN)
