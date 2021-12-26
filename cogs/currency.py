import random
import math
import time
from datetime import date, datetime, timedelta  

import discord
from discord.ext import commands
from discord.colour import Color
from discord.ext.commands.core import command
from discord.utils import get

class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_ready(self):
        print("ready")
        await self.bot.pg_con.execute("CREATE TABLE IF NOT EXISTS currency (userid TEXT NOT NULL, quotes INT)")
        await self.bot.pg_con.execute("ALTER TABLE currency ADD COLUMN IF NOT EXISTS userid TEXT NOT NULL")
        await self.bot.pg_con.execute("ALTER TABLE currency ADD COLUMN IF NOT EXISTS quotes INT")

        await self.bot.pg_con.execute("CREATE TABLE IF NOT EXISTS cooldown (userid TEXT NOT NULL, time TIMESTAMP NOT NULL)")
        await self.bot.pg_con.execute("ALTER TABLE cooldown ADD COLUMN IF NOT EXISTS userid TEXT NOT NULL")
        await self.bot.pg_con.execute("ALTER TABLE cooldown ADD COLUMN IF NOT EXISTS time TIMESTAMP NOT NULL")

    async def cooldown(self, id, time):
        current_time = self.bot.pg_con.fetch("SELECT TIME() FROM cooldown")
        

    async def check(self, id):
        user = await self.bot.pg_con.fetch("SELECT * FROM currency WHERE userid = $1", id)
        if not user:
            await self.bot.pg_con.execute("INSERT INTO currency (userid, quotes) VALUES ($1, $2)", id, 10)

    async def balance(self, id):
        bal = await self.bot.pg_con.fetchrow("SELECT quotes FROM currency WHERE userid = $1", id)
        return bal[0] 
        
    async def top(self):
        leaderboard = await self.bot.pg_con.fetchrow("SELECT * FROM currency ORDER BY quotes DESC NULLS LAST")
        return leaderboard
    
    async def balChange(self, id, amount):
        bal = await self.bot.pg_con.fetchrow("SELECT Quotes FROM currency WHERE userid = $1", id)
        await self.bot.pg_con.execute("UPDATE currency SET quotes = $1 WHERE userid = $2", amount + bal[0], id)


    @commands.command()
    async def bal(self, ctx):
        id = str(ctx.author.id)
        await self.check(id)
        bal = await ctx.bot.pg_con.fetchrow("SELECT quotes FROM currency WHERE userid = $1", id)
        await ctx.send(f'{ctx.author.mention} Your balance: {bal[0]} Quote/s')

    @commands.cooldown(3, 30, commands.BucketType.user)
    @commands.command()
    async def gamble(self, ctx, amount):
        id = str(ctx.author.id)
        await self.check(id)
        try:
            amount = int(amount)
            bal = await ctx.bot.pg_con.fetchrow("SELECT quotes FROM currency WHERE userid = $1", id)
            bal = bal[0]
            if amount >= 5:
                if bal >= amount:
                    dieroll = random.randint(1, 6)
                    if dieroll == 1 or dieroll == 2 or dieroll == 3:
                        await self.balChange(id, -amount)
                        currentBal = await ctx.bot.pg_con.fetchrow("SELECT quotes FROM currency WHERE userid = $1", id)
                        currentBal = currentBal[0]
                        await ctx.send(f'{ctx.author.mention} You lost all of your Quotes...\nYou now have {currentBal} Quote/s.')
                    if dieroll == 4:
                        currentBal = await ctx.bot.pg_con.fetchrow("SELECT quotes FROM currency WHERE userid = $1", id)
                        currentBal = currentBal[0]
                        await ctx.send(f'{ctx.author.mention} You get nothing. The amount that you have gambled has been returned to you.\nYou now have {currentBal} Quote/s.')
                    if dieroll == 5:
                        await self.balChange(id, amount * 0.5)
                        currentBal = await ctx.bot.pg_con.fetchrow("SELECT quotes FROM currency WHERE userid = $1", id)
                        currentBal = currentBal[0]
                        await ctx.send(f'{ctx.author.mention} The amount that you have gambled has been multiplied by 1.5!\nYou now have {currentBal} Quote/s.')
                    if dieroll == 6:
                        await self.balChange(id, amount)
                        currentBal = await ctx.bot.pg_con.fetchrow("SELECT quotes FROM currency WHERE userid = $1", id)
                        currentBal = currentBal[0]
                        await ctx.send(f'{ctx.author.mention} The amount that you have gambled has been doubled!\nYou now have {currentBal} Quote/s.')
                else: 
                    await ctx.send(f"{ctx.author.mention} You don't have enough money!")
            else:
                await ctx.send(f"{ctx.author.mention} You cannot gamble less than 5 Quote!")
        except ValueError:
            await ctx.send(f"{ctx.author.mention} Invaid amount! You cannot gamble a string or decimal.")

    @commands.cooldown(1, 7, commands.BucketType.user)                
    @commands.command(name = 'rps', help = 'Play rock paper scissors.')
    async def rps(self, ctx, choice):
        id = str(ctx.author.id)
        await self.check(id)
        rps = str(random.choices(['rock', 'paper', 'scissors'], k = 1)[0])
        if rps == choice:
            await ctx.send(f"{str.capitalize(rps)}. It's a tie!")

        elif rps == 'rock' and choice == 'paper':
            await self.balChange(id, 2)
            currentBal = await ctx.bot.pg_con.fetchrow("SELECT quotes FROM currency WHERE userid = $1", id)
            currentBal = currentBal[0]
            await ctx.send(f"{str.capitalize(rps)}. You win! You now have {currentBal} Quote/s.")
            
        elif rps == 'rock' and choice == 'scissors':
            await ctx.send(f"{str.capitalize(rps)}. You lose...")

        elif rps == 'paper' and choice == 'scissors':
            await self.balChange(id, 2)
            currentBal = await ctx.bot.pg_con.fetchrow("SELECT quotes FROM currency WHERE userid = $1", id)
            currentBal = currentBal[0]
            await ctx.send(f"{str.capitalize(rps)}. You win! You now have {currentBal} Quote/s.")
            
        elif rps == 'paper' and choice == 'rock':
            await ctx.send(f"{str.capitalize(rps)}. You lose...")

        elif rps == 'scissors' and choice == 'rock':
            await self.balChange(id, 2)
            currentBal = await ctx.bot.pg_con.fetchrow("SELECT quotes FROM currency WHERE userid = $1", id)
            currentBal = currentBal[0]
            await ctx.send(f"{str.capitalize(rps)}. You win! You now have {currentBal} Quote/s.")
        
        elif rps == 'scissors' and choice == 'paper':
            await ctx.send(f"{str.capitalize(rps)}. You lose...")
            
        else:
            await ctx.send('Invalid input! Please choose from: paper, scissors and rock.')
    
    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.command(name = 'quiz', help = 'Test your knowledge in multiple quiz categories! At the moment, the categories are: quick maths.')
    async def quiz(self, ctx, category):
        id = str(ctx.author.id)
        await self.check(id)
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

            msg = await self.bot.wait_for('message', check=check)
            try:
                if isinstance(int(msg.content), int) == True:  
                    if int(msg.content) == answer:
                        await self.balChange(id, 4)
                        currentBal = await ctx.bot.pg_con.fetchrow("SELECT quotes FROM currency WHERE userid = $1", id)
                        currentBal = currentBal[0]
                        await ctx.send('Correct {.author.mention}!\nYou now have {} Quote/s.'.format(msg, currentBal))        
                    else:
                        await ctx.send('Incorrect {.author.mention}... The correct answer was '.format(msg) + str(answer) + '.')
            except ValueError:
                await ctx.send('Invalid response {.author.mention}! The correct answer was '.format(msg) + str(answer) + '.')
            
    @commands.cooldown(1, 45, commands.BucketType.user)
    @commands.command(name = "crime", help = "Commit a crime for high stake rewards and punishments. (Rob, Scam)")
    async def crime(self, ctx, choice):
        id = str(ctx.author.id)
        await self.check(id)
        bal = await ctx.bot.pg_con.fetchrow("SELECT quotes FROM currency WHERE userid = $1", id)
        bal = bal[0]        
        locations = ["a sushi store", "a bank", "a school", "a bedroom", "the Google HQ", "your mother's wallet" ]
        scams = ["crypto", "illicit goods", "phone", "phishing", "email", "TV", "website", "school based", "fishing"]
        reasons_scam = ['you suck at programming', 'your English level is lower than a primary school student', "you haven't had your daily dose of sushi", "your phishing skills aren't up to standard"]

        if (choice.lower() == "rob") and bal >= 10:
            chance = random.randrange(0,100)
            if (chance < 93):
                fine = random.randrange(50, 80)
                await ctx.send(f"{ctx.author.mention} You were caught stealing from {random.choice(locations)}! You were fined {round((100 - fine)/100 * bal)} Quote/s ({100 - fine}% of your Quotes).\nYou now have {round((float(fine) / 100) * bal)} Quote/s.")
                await self.bot.pg_con.execute("UPDATE currency SET quotes = $1 WHERE userid = $2", (float(fine) / 100) * bal, id)
            if (chance >= 93):
                reward = random.randrange(300, 425)
                await ctx.send(f"{ctx.author.mention} You're too good at this, you stole from {random.choice(locations)} and earned {round((bal * (float(reward) / 100) - bal))} Quote/s ({reward - 100}% of your Quotes).\nYou now have {round(float(reward) / 100)} Quote/s.")
                await self.bot.pg_con.execute("UPDATE currency SET quotes = $1 WHERE userid = $2", (float(reward) / 100) * bal, id)
        elif bal < 10:
            await ctx.send("Insufficient funds, try again when you have at least 10 Quotes!")

        if (choice.lower() == "scam") and bal >= 10:
            chance = random.randrange(0,100)
            if (chance < 85):
                fine = random.randrange(90,98)
                await ctx.send(f"{ctx.author.mention} Your {random.choice(scams)} scam was discoverd because {random.choice(reasons_scam)}! You were fined {round((100 - fine)/100 * bal)} Quote/s ({100 - fine}% of your Quotes).\nYou now have {round((float(fine) / 100) * bal)} Quote/s.")
                await self.bot.pg_con.execute("UPDATE currency SET quotes = $1 WHERE userid = $2", (float(fine) / 100) * bal, id)
            if (chance >= 85):
                reward = random.randrange(120, 200)
                await ctx.send(f"{ctx.author.mention} You're too good at this, your {random.choice(scams)} scam worked and earned {round(bal * (float(reward) / 100) - bal)} Quote/s ({reward - 100}% of your Quotes).\nYou now have {(round(float(reward) / 100) * bal)} Quote/s.")
                await self.bot.pg_con.execute("UPDATE currency SET quotes = $1 WHERE userid = $2", (float(reward) / 100) * bal, id)
        elif bal < 10:
            await ctx.send("Insufficient funds, try again when you have at least 10 Quotes!")
        
    @commands.cooldown(1, 86400, commands.BucketType.user)
    @commands.command(name = 'daily')
    async def daily(self, ctx):
        id = str(ctx.author.id)
        await self.check(id)
        await self.balChange(id, 50)
        bal = await ctx.bot.pg_con.fetchrow("SELECT quotes FROM currency WHERE userid = $1", id)
        bal = bal[0]
        await ctx.send(f'Enjoy your daily 50 Quotes.\nYour current balance is {bal} Quotes.')
        
def setup(bot):
    bot.add_cog(Currency(bot))
