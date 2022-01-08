import medical_quizzes
import maths_adv_quizzes

import random
import math
import time
from datetime import date, datetime, timedelta 
import asyncio

import discord
from discord.ext import commands
from discord.colour import Color
from discord.ext.commands.core import command
from discord.utils import get

vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']
consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z', 'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z']

class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_ready(self):
        print("Currency cog ready.")
        await self.bot.pg_con.execute("CREATE TABLE IF NOT EXISTS currency (userid TEXT NOT NULL, quotes INT)")
        await self.bot.pg_con.execute("ALTER TABLE currency ADD COLUMN IF NOT EXISTS userid TEXT NOT NULL")
        await self.bot.pg_con.execute("ALTER TABLE currency ADD COLUMN IF NOT EXISTS quotes INT")

        await self.bot.pg_con.execute("CREATE TABLE IF NOT EXISTS cooldown (userid TEXT NOT NULL, time TIMESTAMP NOT NULL)")
        await self.bot.pg_con.execute("ALTER TABLE cooldown ADD COLUMN IF NOT EXISTS userid TEXT NOT NULL")
        await self.bot.pg_con.execute("ALTER TABLE cooldown ADD COLUMN IF NOT EXISTS time TIMESTAMP NOT NULL")

        await self.bot.pg_con.execute("""CREATE TABLE IF NOT EXISTS inventory 
        (userid TEXT NOT NULL, 
        catfish INT NOT NULL DEFAULT 0, 
        mackerel INT NOT NULL DEFAULT 0, 
        sardine INT NOT NULL DEFAULT 0, 
        walleye INT NOT NULL DEFAULT 0, 
        salmon INT NOT NULL DEFAULT 0, 
        cod INT NOT NULL DEFAULT 0, 
        tuna INT NOT NULL DEFAULT 0, 
        whale INT NOT NULL DEFAULT 0, 
        mermaid INT NOT NULL DEFAULT 0, 
        dragon INT NOT NULL DEFAULT 0, 
        kraken INT NOT NULL DEFAULT 0, 
        siren INT NOT NULL DEFAULT 0,
        technoblade INT NOT NULL DEFAULT 0,
        hydra INT NOT NULL DEFAULT 0,
        selkie INT NOT NULL DEFAULT 0,
        boar INT NOT NULL DEFAULT 0,
        goose INT NOT NULL DEFAULT 0,
        python INT NOT NULL DEFAULT 0,
        tiger INT NOT NULL DEFAULT 0,
        rabbit INT NOT NULL DEFAULT 0,
        griffin INT NOT NULL DEFAULT 0,
        manticore INT NOT NULL DEFAULT 0,
        bear INT NOT NULL DEFAULT 0,
        panda INT NOT NULL DEFAULT 0,
        cyclops INT NOT NULL DEFAULT 0,
        fairy INT NOT NULL DEFAULT 0,
        medusa INT NOT NULL DEFAULT 0,
        avocado INT NOT NULL DEFAULT 0,
        rice INT NOT NULL DEFAULT 0,
        seaweed INT NOT NULL DEFAULT 0,
        sushi_kit INT NOT NULL DEFAULT 0,
        tuna_roll INT NOT NULL DEFAULT 0,
        salmon_roll INT NOT NULL DEFAULT 0,
        cocoa_beans INT NOT NULL DEFAULT 0,
        milk INT NOT NULL DEFAULT 0,
        sugar INT NOT NULL DEFAULT 0,
        cocoa_butter INT NOT NULL DEFAULT 0,
        soy_lecithin INT NOT NULL DEFAULT 0,
        vegetable_oil INT NOT NULL DEFAULT 0,
        vanilla INT NOT NULL DEFAULT 0,
        chocolate_kit INT NOT NULL DEFAULT 0,
        milk_chocolate INT NOT NULL DEFAULT 0,
        dark_chocolate INT NOT NULL DEFAULT 0
        )""")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS userid TEXT NOT NULL")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS catfish INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS mackerel INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS sardine INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS walleye INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS salmon INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS cod INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS tuna INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS whale INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS mermaid INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS dragon INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS kraken INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS siren INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS selkie INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS hydra INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS technoblade INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS boar INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS goose INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS python INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS tiger INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS rabbit INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS griffin INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS manticore INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS bear INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS panda INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS cyclops INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS fairy INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS medusa INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS sushi_kit INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS rice INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS seaweed INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS avocado INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS tuna_roll INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS salmon_roll INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS milk INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS cocoa_beans INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS sugar INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS cocoa_butter INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS soy_lecithin INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS vegetable_oil INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS vanilla INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS chocolate_kit INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS milk_chocolate INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS dark_chocolate INT NOT NULL DEFAULT 0")


    async def cooldown(self, id, time):
        current_time = self.bot.pg_con.fetch("SELECT TIME() FROM cooldown")
        

    async def check_bal(self, id):
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

    async def check_inv(self, id):
        user = await self.bot.pg_con.fetch("SELECT * FROM inventory WHERE userid = $1", id)
        if not user:
            await self.bot.pg_con.execute("INSERT INTO inventory (userid) VALUES ($1)", id)

    @commands.command()
    async def bal(self, ctx, user = None):
        if user == None:
            id = str(ctx.author.id)
            await self.check_bal(id)
            bal = await ctx.bot.pg_con.fetchrow("SELECT quotes FROM currency WHERE userid = $1", id)
            await ctx.send(f'{ctx.author.mention} Your balance: {bal[0]} Quote/s')
        else:
            if user.startswith("<@") and user.endswith(">"):
                if "<@!" in user:
                    user = (user.removeprefix(str("<@!"))).removesuffix(str(">"))
                else:
                    user = (user.removeprefix(str("<@"))).removesuffix(str(">"))

                await self.check_bal(user)
                bal = await ctx.bot.pg_con.fetchrow("SELECT quotes FROM currency WHERE userid = $1", user)
                await ctx.send(f"<@{user}>'s balance: {bal[0]} Quote/s")

            else:
                await ctx.send(f"{ctx.author.mention} Invalid user!")

    @commands.cooldown(3, 30, commands.BucketType.user)
    @commands.command()
    async def gamble(self, ctx, amount):
        id = str(ctx.author.id)
        await self.check_bal(id)
        try:
            bal = await ctx.bot.pg_con.fetchrow("SELECT quotes FROM currency WHERE userid = $1", id)
            bal = bal[0]
            if amount == 'all':
                amount = int(bal)
            else:
                amount = int(amount)
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
        await self.check_bal(id)
        rps = str(random.choices(['rock', 'paper', 'scissors'], k = 1)[0])
        if rps == choice:
            await ctx.send(f"{ctx.author.mention} {str.capitalize(rps)}. It's a tie!")

        elif rps == 'rock' and choice == 'paper':
            await self.balChange(id, 2)
            currentBal = await ctx.bot.pg_con.fetchrow("SELECT quotes FROM currency WHERE userid = $1", id)
            currentBal = currentBal[0]
            await ctx.send(f"{ctx.author.mention} {str.capitalize(rps)}. You win! You now have {currentBal} Quote/s.")
            
        elif rps == 'rock' and choice == 'scissors':
            await ctx.send(f"{ctx.author.mention} {str.capitalize(rps)}. You lose...")

        elif rps == 'paper' and choice == 'scissors':
            await self.balChange(id, 2)
            currentBal = await ctx.bot.pg_con.fetchrow("SELECT quotes FROM currency WHERE userid = $1", id)
            currentBal = currentBal[0]
            await ctx.send(f"{ctx.author.mention} {str.capitalize(rps)}. You win! You now have {currentBal} Quote/s.")
            
        elif rps == 'paper' and choice == 'rock':
            await ctx.send(f"{ctx.author.mention} {str.capitalize(rps)}. You lose...")

        elif rps == 'scissors' and choice == 'rock':
            await self.balChange(id, 2)
            currentBal = await ctx.bot.pg_con.fetchrow("SELECT quotes FROM currency WHERE userid = $1", id)
            currentBal = currentBal[0]
            await ctx.send(f"{ctx.author.mention} {str.capitalize(rps)}. You win! You now have {currentBal} Quote/s.")
        
        elif rps == 'scissors' and choice == 'paper':
            await ctx.send(f"{ctx.author.mention} {str.capitalize(rps)}. You lose...")
            
        else:
            await ctx.send(f'{ctx.author.mention} Invalid input! Please choose from: paper, scissors and rock.')
    
    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.command(name = 'quiz', help = 'Test your knowledge in multiple quiz categories! At the moment, the categories are: quick maths, medical.')
    async def quiz(self, ctx, *, category):
        id = str(ctx.author.id)
        await self.check_bal(id)
        category = category.lower()

        if category == "quick maths":
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

            await ctx.send(f'{ctx.author.mention}{question}')
                    
            def check(msg):
                return msg.channel == ctx.channel and msg.author == ctx.author

            msg = await self.bot.wait_for('message', check=check)
            try:
                if isinstance(int(msg.content), int) == True:  
                    if int(msg.content) == answer:
                        await self.balChange(id, 2)
                        currentBal = await ctx.bot.pg_con.fetchrow("SELECT quotes FROM currency WHERE userid = $1", id)
                        currentBal = currentBal[0]
                        await ctx.send('Correct {.author.mention}!\nYou now have {} Quote/s.'.format(msg, currentBal))        
                    else:
                        await ctx.send('Incorrect {.author.mention}... The correct answer was '.format(msg) + str(answer) + '.')
            except ValueError:
                await ctx.send('Invalid response {.author.mention}! The correct answer was '.format(msg) + str(answer) + '.')

        elif category == "medical":
            questions = medical_quizzes.questions
            question = random.choice(list(questions.keys()))
            answer = questions[question]

            await ctx.send(f'{ctx.author.mention}{question}')

            def check(msg):
                return msg.channel == ctx.channel and msg.author == ctx.author
            
            msg = await self.bot.wait_for('message', check=check)
            if (msg.content.lower()) == answer.lower():
                await self.balChange(id, 4)
                currentBal = await ctx.bot.pg_con.fetchrow("SELECT quotes FROM currency WHERE userid = $1", id)
                currentBal = currentBal[0]
                await ctx.send('Correct {.author.mention}!\nYou now have {} Quote/s.'.format(msg, currentBal))        
            else:
                await ctx.send('Incorrect {.author.mention}... The correct answer was '.format(msg) + str(answer) + '.')

        elif category == 'maths adv' or category == 'maths advanced':
            questions = maths_adv_quizzes.questions
            question = random.choice(list(questions.keys()))
            answer = questions[question]

            await ctx.send("[NOTE]: When the question has multiple parts/sections, use commas with a space after it to separate answers (e.g. '1, 2, 3'). Units and variables are not required unless the question is asking for an equation (e.g. 't = 2s' can be written as just '2'). Use mathematical symbols where applicable to answer questions (e.g. π instead of pi, √ instead of sqrt().) Red lines crossing out a part means that no answer is required for that part. Questions asking for 'dimensions' can be answered with an astrix (e.g. 3*4 meaning 3 by 4). ")
            await ctx.send(ctx.author.mention)
            await ctx.send(file = discord.File(f'images/{question}'))

            def check(msg):
                return msg.channel == ctx.channel and msg.author == ctx.author
            
            msg = await self.bot.wait_for('message', check=check)
            if (msg.content) == answer:
                await self.balChange(id, 4)
                currentBal = await ctx.bot.pg_con.fetchrow("SELECT quotes FROM currency WHERE userid = $1", id)
                currentBal = currentBal[0]
                await ctx.send('Correct {.author.mention}!\nYou now have {} Quote/s.'.format(msg, currentBal))        
            else:
                await ctx.send('Incorrect {.author.mention}... The correct answer was '.format(msg) + str(answer) + '.')
        else:
            await ctx.send(f"{ctx.author.mention} This category does not exist. The categories are: quick maths and medical. $quiz [category]")

    @commands.cooldown(1, 3600, commands.BucketType.user)
    @commands.command(name = "work", help = "Earn Quotes by working.")
    async def work(self, ctx):
        id = str(ctx.author.id)
        await self.check_bal(id)
        bal = await ctx.bot.pg_con.fetchrow("SELECT quotes FROM currency WHERE userid = $1", id)
        bal = bal[0]
        jobs = ['a cleaner', 'a dentist', 'a GP doctor', 'a surgeon', 'a welder', 'a miner', 'a pro gamer', 'a streamer', 'a volunteer', 'a terrorist', "a McDonald's employee", 'a chef']
        job = random.choices(jobs, weights = (50, 15, 12, 9, 30, 14, 37, 47, 35, 2, 49, 33))
        job = job[0]
        wage = 0
        if job == 'a cleaner':
            wage = random.randint(16, 23)
        elif job == 'a dentist':
            wage = random.randint(68, 85)
        elif job == 'a GP doctor':
            wage = random.randint(75, 85)
        elif job == 'a surgeon':
            wage = random.randint(95, 110)
        elif job == 'a welder':
            wage = random.randint(30, 45)
        elif job == 'a miner':
            wage = random.randint(70, 80)
        elif job == 'a pro gamer':
            wage = random.randint(25, 41)
        elif job == 'a streamer':
            wage = random.randint(15, 29)
        elif job == 'a volunteer':
            wage = 0
        elif job == 'a terrorist':
            wage = -int((round(bal/2)))
        elif job == "a McDonald's employee":
            wage = random.randint(15, 25)
        elif job == 'a chef':
            wage = random.randint(28, 40)

        await self.balChange(id, wage)
        current_bal = await ctx.bot.pg_con.fetchrow("SELECT quotes FROM currency WHERE userid = $1", id)
        current_bal = current_bal[0]
        await ctx.send(f'{ctx.author.mention} You worked as {job} and earned {wage} Quotes! You now have {current_bal} Quotes.')            

    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.command(name = "crime", help = "Commit a crime for high stake rewards and punishments. (Rob, Scam, Murder)")
    async def crime(self, ctx, choice):
        id = str(ctx.author.id)
        await self.check_bal(id)
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
                await ctx.send(f"{ctx.author.mention} Your {random.choice(scams)} scam was discovered because {random.choice(reasons_scam)}! You were fined {round((100 - fine)/100 * bal)} Quote/s ({100 - fine}% of your Quotes).\nYou now have {round((float(fine) / 100) * bal)} Quote/s.")
                await self.bot.pg_con.execute("UPDATE currency SET quotes = $1 WHERE userid = $2", (float(fine) / 100) * bal, id)
            if (chance >= 85):
                reward = random.randrange(120, 200)
                await ctx.send(f"{ctx.author.mention} You're too good at this, your {random.choice(scams)} scam worked and earned {round(bal * (float(reward) / 100) - bal)} Quote/s ({reward - 100}% of your Quotes).\nYou now have {(round(float(reward) / 100) * bal)} Quote/s.")
                await self.bot.pg_con.execute("UPDATE currency SET quotes = $1 WHERE userid = $2", (float(reward) / 100) * bal, id)
        elif bal < 10:
            await ctx.send(f"{ctx.author.mention} Insufficient funds, try again when you have at least 10 Quotes!")

        if (choice.lower() == "murder") and bal >= 10:
            chance = random.randrange(0,100)
            if (chance < 95):
                fine = random.randrange(45,90)
                await ctx.send(f"{ctx.author.mention} Your murder was prevented! You were fined {round((100 - fine)/100 * bal)} Quote/s ({100 - fine}% of your Quotes).\nYou now have {round((float(fine) / 100) * bal)} Quote/s.")
                await self.bot.pg_con.execute("UPDATE currency SET quotes = $1 WHERE userid = $2", (float(fine) / 100) * bal, id)
            if (chance >= 95):
                reward = random.randrange(300, 500)
                await ctx.send(f"{ctx.author.mention} What is wrong with you, you earned {round(bal * (float(reward) / 100) - bal)} Quote/s from your target ({reward - 100}% of your Quotes).\nYou now have {(round(float(reward) / 100) * bal)} Quote/s.")
                await self.bot.pg_con.execute("UPDATE currency SET quotes = $1 WHERE userid = $2", (float(reward) / 100) * bal, id)
        elif bal < 10:
            await ctx.send(f"{ctx.author.mention} Insufficient funds, try again when you have at least 10 Quotes!")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name = 'shop', help = "See what's available in the virtual shop. Categories: food, ingredients, fish, hunt, sellable.")
    async def shop(self, ctx, category):
        if category.lower() == 'food':
            await ctx.send("""```css
[Shop: Food]

Tuna Roll - Buy: 10 Quotes, Sell: 6 Quotes 
Salmon Roll - Buy: 11 Quotes, Sell: 7 Quotes
Milk Chocolate - Buy: 14 Quotes, Sell: 9 Quotes
Dark Chocolate - Buy: 13 Quotes, Sell: 8 Quotes

```
""")

        elif category.lower() == 'ingredients':
            await ctx.send("""```css
[Shop: Ingredients]

Rice - Buy: 3 Quotes, Sell: N/A
Avocado - Buy: 3 Quotes, Sell: N/A
Seaweed - Buy: 2 Quotes, Sell: N/A
Sushi_Kit - Buy: 2 Quotes, Sell: N/A
Cocoa_Beans - Buy: 4 Quotes, Sell: N/A
Milk - Buy: 3 Quotes, Sell: N/A
Sugar - Buy: 2 Quotes, Sell: N/A
Cocoa_Butter - Buy: 3 Quotes, Sell: N/A
Soy_Lecithin - Buy: 3 Quotes, Sell: N/A
Vegetable_Oil - Buy: 5 Quotes, Sell: N/A
Vanilla - Buy: 6 Quotes, Sell: N/A
Chocolate_Kit - Buy: 15 Quotes, Sell: N/A

```
""")

        elif category.lower() == 'fish':
            await ctx.send("""```css
[Shop: Fish]

Catfish - Buy: N/A, Sell: 5 Quotes
Mackerel - Buy: N/A, Sell: 6 Quotes
Sardine - Buy: N/A, Sell: 7 Quotes
Walleye - Buy: N/A, Sell: 7 Quotes
Salmon - Buy: N/A, Sell: 9 Quotes
Cod - Buy: N/A, Sell: 8 Quotes
Tuna - Buy: N/A, Sell: 9 Quotes
Whale - Buy: N/A, Sell: 30 Quotes
Mermaid - Buy: N/A, Sell: 80 Quotes
Dragon - Buy: N/A, Sell: 140 Quotes
Kraken - Buy: N/A, Sell: 300 Quotes
Siren - Buy: N/A, Sell: 550 Quotes
Selkie - Buy: N/A, Sell: 250 Quotes
Technoblade - Buy: N/A, Sell: 1000 Quotes
Hydra - Buy: N/A, Sell: 700 Quotes

```
""")
        elif category.lower() == 'hunt':
            await ctx.send("""```css
[Shop: Hunt]

Boar - Buy: N/A, Sell: 6 Quotes
Goose - Buy: N/A, Sell: 5 Quotes
Python - Buy: N/A, Sell: 30 Quotes
Tiger - Buy: N/A, Sell: 60 Quotes
Dragon - Buy: N/A, Sell: 140 Quotes
Rabbit - Buy: N/A, Sell: 12 Quotes
Griffin - Buy: N/A, Sell: 100 Quotes
Manticore - Buy: N/A, Sell: 800 Quotes
Hydra - Buy: N/A, Sell: 700 Quotes
Bear - Buy: N/A, Sell: 75 Quotes
Panda - Buy: N/A, Sell: 100 Quotes
Cyclops - Buy: N/A, Sell: 475 Quotes
Fairy - Buy: N/A, Sell: 130 Quotes
Medusa - Buy: N/A, Sell: 1000 Quotes

```
""")

        elif category.lower() == 'sellable':
            await ctx.send("""```css
[Shop: Sellable]

Catfish - Buy: N/A, Sell: 5 Quotes
Mackerel - Buy: N/A, Sell: 6 Quotes
Sardine - Buy: N/A, Sell: 7 Quotes
Walleye - Buy: N/A, Sell: 7 Quotes
Salmon - Buy: N/A, Sell: 9 Quotes
Cod - Buy: N/A, Sell: 8 Quotes
Tuna - Buy: N/A, Sell: 9 Quotes
Whale - Buy: N/A, Sell: 30 Quotes
Mermaid - Buy: N/A, Sell: 80 Quotes
Dragon - Buy: N/A, Sell: 140 Quotes
Kraken - Buy: N/A, Sell: 300 Quotes
Siren - Buy: N/A, Sell: 550 Quotes
Selkie - Buy: N/A, Sell: 250 Quotes
Technoblade - Buy: N/A, Sell: 1000 Quotes
Hydra - Buy: N/A, Sell: 700 Quotes
Boar - Buy: N/A, Sell: 6 Quotes
Goose - Buy: N/A, Sell: 5 Quotes
Python - Buy: N/A, Sell: 30 Quotes
Tiger - Buy: N/A, Sell: 60 Quotes
Dragon - Buy: N/A, Sell: 140 Quotes
Rabbit - Buy: N/A, Sell: 12 Quotes
Griffin - Buy: N/A, Sell: 100 Quotes
Manticore - Buy: N/A, Sell: 800 Quotes
Hydra - Buy: N/A, Sell: 700 Quotes
Bear - Buy: N/A, Sell: 75 Quotes
Panda - Buy: N/A, Sell: 100 Quotes
Cyclops - Buy: N/A, Sell: 475 Quotes
Fairy - Buy: N/A, Sell: 130 Quotes
Medusa - Buy: N/A, Sell: 1000 Quotes

```
""")

    @commands.command(name = 'buy', help = 'Buy virtual items from the virtual shop with your Quotes. NOTE: when buying items, please seperate words with underscores instead of spaces. (e.g. $buy tuna_roll 1)')
    async def buy(self, ctx, amount = 1, *, item):
        try:
            amount = int(amount)
            id = str(ctx.author.id)
            item = (str(item.lower())).replace(' ', '_')

            await self.check_bal(id)
            await self.check_inv(id)
            bal = (await self.bot.pg_con.fetchrow("SELECT quotes FROM currency WHERE userid = $1", id))[0]

            buyable_items = {
                'avocado': 3,
                'rice': 3,
                'seaweed': 2,
                'sushi_kit': 15,
                'cocoa_beans': 4,
                'milk': 3,
                'sugar': 2,
                'cocoa_butter': 3,
                'soy_lecithin': 3,
                'vegetable_oil': 5,
                'vanilla': 6,
                'chocolate_kit': 15,
                'milk_chocolate': 14,
                'dark_chocolate': 13,
                'tuna_roll': 10,
                'salmon_roll': 11,

            }

            if amount == 1:
                valid = True
            elif amount > 1:
                valid = True
            elif amount <= 0:
                valid = False
            else:
                valid = False


            if item in buyable_items and valid == True:
                price = int(buyable_items[item])
                total = price * amount
                item_in_inv = int((await self.bot.pg_con.fetchrow(f"SELECT {item} FROM inventory WHERE userid = $1", id))[0])
                
                if bal >= total:
                    await self.balChange(id, -total)
                    current_bal = await self.bot.pg_con.fetchrow("SELECT quotes FROM currency WHERE userid = $1", id)
                    current_bal = current_bal[0]
                    await self.bot.pg_con.execute(f"UPDATE inventory SET {item} = $1 WHERE userid = $2", item_in_inv + amount, id)
                    current_item_in_inv = (await self.bot.pg_con.fetchrow(f"SELECT {item} FROM inventory WHERE userid = $1", id))[0]
                    item = (str(item.lower())).replace('_', ' ')
                    await ctx.send(f"{ctx.author.mention} Thank you for purchasing {amount} {item}! You have spent a total of {total} Quotes. You now have {current_bal} Quotes and {current_item_in_inv} {item}.")
        
                else:
                    await ctx.send(f"{ctx.author.mention} You do not have enough money to purchase this item! Use $shop to check the prices of items.")

            elif valid == False:
                await ctx.send(f"{ctx.author.mention} Invalid input.")

            else:
                await ctx.send(f'{ctx.author.mention} The item you specified is not buyable or invalid.')

        except ValueError:
            await ctx.send(f"{ctx.author.mention} Error, check the command usage using `$help [command]`.")
            
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name = 'inventory' and 'inv', help = 'Checks your for items that you have purchased. Categories are: food, ingredients, sellable, hunt, fish.')
    async def inventory(self, ctx, category):
        id = str(ctx.author.id)
        await self.check_bal(id)
        await self.check_inv(id)

        if category.lower() == 'food':

            if (await self.bot.pg_con.fetchrow("SELECT salmon_roll FROM inventory WHERE userid = $1", id))[0] > 0:
                salmon_roll = (f'\nSalmon Avocado Roll: {str((await self.bot.pg_con.fetchrow("SELECT salmon_roll FROM inventory WHERE userid = $1", id))[0])}')
            else:
                salmon_roll = ''

            if (await self.bot.pg_con.fetchrow("SELECT tuna_roll FROM inventory WHERE userid = $1", id))[0] > 0:
                tuna_roll = (f'\nTuna Avocado Roll: {str((await self.bot.pg_con.fetchrow("SELECT tuna_roll FROM inventory WHERE userid = $1", id))[0])}')
            else:
                tuna_roll = ''
            
            if (await self.bot.pg_con.fetchrow("SELECT milk_chocolate FROM inventory WHERE userid = $1", id))[0] > 0:
                milk_chocolate = (f'\nMilk Chocolate: {str((await self.bot.pg_con.fetchrow("SELECT milk_chocolate FROM inventory WHERE userid = $1", id))[0])}')
            else:
                milk_chocolate = ''

            if (await self.bot.pg_con.fetchrow("SELECT dark_chocolate FROM inventory WHERE userid = $1", id))[0] > 0:
                dark_chocolate = (f'\nDark Chocolate: {str((await self.bot.pg_con.fetchrow("SELECT dark_chocolate FROM inventory WHERE userid = $1", id))[0])}')
            else:
                dark_chocolate = ''
            
            await ctx.send(f'''{ctx.author.mention}```css\n[Inventory: Food]\n{tuna_roll}{salmon_roll}{dark_chocolate}{milk_chocolate}```''')

        elif category.lower() == 'fish':

            if (await self.bot.pg_con.fetchrow("SELECT catfish FROM inventory WHERE userid = $1", id))[0] > 0:
                catfish = (f'\nCatfish: {str((await self.bot.pg_con.fetchrow("SELECT catfish FROM inventory WHERE userid = $1", id))[0])}')
            else:
                catfish = ''

            if (await self.bot.pg_con.fetchrow("SELECT mackerel FROM inventory WHERE userid = $1", id))[0] > 0:
                mackerel = (f'\nMackerel: {str((await self.bot.pg_con.fetchrow("SELECT mackerel FROM inventory WHERE userid = $1", id))[0])}')
            else:
                mackerel = ''
            
            if (await self.bot.pg_con.fetchrow("SELECT sardine FROM inventory WHERE userid = $1", id))[0] > 0:
                sardine = (f'\nSardine: {str((await self.bot.pg_con.fetchrow("SELECT sardine FROM inventory WHERE userid = $1", id))[0])}')
            else:
                sardine = ''

            if (await self.bot.pg_con.fetchrow("SELECT walleye FROM inventory WHERE userid = $1", id))[0] > 0:
                walleye = (f'\nWalleye: {str((await self.bot.pg_con.fetchrow("SELECT walleye FROM inventory WHERE userid = $1", id))[0])}')
            else:
                walleye = ''
            
            if (await self.bot.pg_con.fetchrow("SELECT salmon FROM inventory WHERE userid = $1", id))[0] > 0:
                salmon = (f'\nSalmon: {str((await self.bot.pg_con.fetchrow("SELECT salmon FROM inventory WHERE userid = $1", id))[0])}')
            else:
                salmon = ''

            if (await self.bot.pg_con.fetchrow("SELECT cod FROM inventory WHERE userid = $1", id))[0] > 0:
                cod = (f'\nCod: {str((await self.bot.pg_con.fetchrow("SELECT cod FROM inventory WHERE userid = $1", id))[0])}')
            else:
                cod = ''

            if (await self.bot.pg_con.fetchrow("SELECT tuna FROM inventory WHERE userid = $1", id))[0] > 0:
                tuna = (f'\nTuna: {str((await self.bot.pg_con.fetchrow("SELECT tuna FROM inventory WHERE userid = $1", id))[0])}')
            else:
                tuna = ''
            
            if (await self.bot.pg_con.fetchrow("SELECT whale FROM inventory WHERE userid = $1", id))[0] > 0:
                whale = (f'\nWhale: {str((await self.bot.pg_con.fetchrow("SELECT whale FROM inventory WHERE userid = $1", id))[0])}')
            else:
                whale = ''

            if (await self.bot.pg_con.fetchrow("SELECT mermaid FROM inventory WHERE userid = $1", id))[0] > 0:
                mermaid = (f'\nMermaid: {str((await self.bot.pg_con.fetchrow("SELECT mermaid FROM inventory WHERE userid = $1", id))[0])}')
            else:
                mermaid = ''

            if (await self.bot.pg_con.fetchrow("SELECT dragon FROM inventory WHERE userid = $1", id))[0] > 0:
                dragon = (f'\nDragon: {str((await self.bot.pg_con.fetchrow("SELECT dragon FROM inventory WHERE userid = $1", id))[0])}')
            else:
                dragon = ''
            
            if (await self.bot.pg_con.fetchrow("SELECT kraken FROM inventory WHERE userid = $1", id))[0] > 0:
                kraken = (f'\nKraken: {str((await self.bot.pg_con.fetchrow("SELECT kraken FROM inventory WHERE userid = $1", id))[0])}')
            else:
                kraken = ''

            if (await self.bot.pg_con.fetchrow("SELECT siren FROM inventory WHERE userid = $1", id))[0] > 0:
                siren = (f'\nSiren: {str((await self.bot.pg_con.fetchrow("SELECT siren FROM inventory WHERE userid = $1", id))[0])}')
            else:
                siren = ''

            if (await self.bot.pg_con.fetchrow("SELECT hydra FROM inventory WHERE userid = $1", id))[0] > 0:
                hydra = (f'\nHydra: {str((await self.bot.pg_con.fetchrow("SELECT hydra FROM inventory WHERE userid = $1", id))[0])}')
            else:
                hydra = ''

            if (await self.bot.pg_con.fetchrow("SELECT selkie FROM inventory WHERE userid = $1", id))[0] > 0:
                selkie = (f'\nSelkie: {str((await self.bot.pg_con.fetchrow("SELECT selkie FROM inventory WHERE userid = $1", id))[0])}')
            else:
                selkie = ''

            if (await self.bot.pg_con.fetchrow("SELECT technoblade FROM inventory WHERE userid = $1", id))[0] > 0:
                technoblade = (f'\nTechnoblade: {str((await self.bot.pg_con.fetchrow("SELECT technoblade FROM inventory WHERE userid = $1", id))[0])}')
            else:
                technoblade = ''

            await ctx.send(f'''{ctx.author.mention}```css\n[Inventory: Fish]\n{catfish}{mackerel}{sardine}{walleye}{salmon}{cod}{tuna}{whale}{mermaid}{dragon}{kraken}{siren}{hydra}{selkie}{technoblade}```''')

        elif category.lower() == 'hunt':

            if (await self.bot.pg_con.fetchrow("SELECT boar FROM inventory WHERE userid = $1", id))[0] > 0:
                boar = (f'\nBoar: {str((await self.bot.pg_con.fetchrow("SELECT boar FROM inventory WHERE userid = $1", id))[0])}')
            else:
                boar = ''

            if (await self.bot.pg_con.fetchrow("SELECT goose FROM inventory WHERE userid = $1", id))[0] > 0:
                goose = (f'\nGoose: {str((await self.bot.pg_con.fetchrow("SELECT goose FROM inventory WHERE userid = $1", id))[0])}')
            else:
                goose = ''
            
            if (await self.bot.pg_con.fetchrow("SELECT python FROM inventory WHERE userid = $1", id))[0] > 0:
                python = (f'\nPython: {str((await self.bot.pg_con.fetchrow("SELECT python FROM inventory WHERE userid = $1", id))[0])}')
            else:
                python = ''
            
            if (await self.bot.pg_con.fetchrow("SELECT tiger FROM inventory WHERE userid = $1", id))[0] > 0:
                tiger = (f'\nTiger: {str((await self.bot.pg_con.fetchrow("SELECT tiger FROM inventory WHERE userid = $1", id))[0])}')
            else:
                tiger = ''
            
            if (await self.bot.pg_con.fetchrow("SELECT dragon FROM inventory WHERE userid = $1", id))[0] > 0:
                dragon = (f'\nDragon: {str((await self.bot.pg_con.fetchrow("SELECT dragon FROM inventory WHERE userid = $1", id))[0])}')
            else:
                dragon = ''
            
            if (await self.bot.pg_con.fetchrow("SELECT rabbit FROM inventory WHERE userid = $1", id))[0] > 0:
                rabbit = (f'\nRabbit: {str((await self.bot.pg_con.fetchrow("SELECT rabbit FROM inventory WHERE userid = $1", id))[0])}')
            else:
                rabbit = ''

            if (await self.bot.pg_con.fetchrow("SELECT griffin FROM inventory WHERE userid = $1", id))[0] > 0:
                griffin = (f'\nGriffin: {str((await self.bot.pg_con.fetchrow("SELECT griffin FROM inventory WHERE userid = $1", id))[0])}')
            else:
                griffin = ''

            if (await self.bot.pg_con.fetchrow("SELECT manticore FROM inventory WHERE userid = $1", id))[0] > 0:
                manticore = (f'\nManticore: {str((await self.bot.pg_con.fetchrow("SELECT manticore FROM inventory WHERE userid = $1", id))[0])}')
            else:
                manticore = ''
            
            if (await self.bot.pg_con.fetchrow("SELECT hydra FROM inventory WHERE userid = $1", id))[0] > 0:
                hydra = (f'\nHydra: {str((await self.bot.pg_con.fetchrow("SELECT hydra FROM inventory WHERE userid = $1", id))[0])}')
            else:
                hydra = ''

            if (await self.bot.pg_con.fetchrow("SELECT bear FROM inventory WHERE userid = $1", id))[0] > 0:
                bear = (f'\nBear: {str((await self.bot.pg_con.fetchrow("SELECT bear FROM inventory WHERE userid = $1", id))[0])}')
            else:
                bear = ''
            
            if (await self.bot.pg_con.fetchrow("SELECT panda FROM inventory WHERE userid = $1", id))[0] > 0:
                panda = (f'\nPanda: {str((await self.bot.pg_con.fetchrow("SELECT panda FROM inventory WHERE userid = $1", id))[0])}')
            else:
                panda = ''

            if (await self.bot.pg_con.fetchrow("SELECT cyclops FROM inventory WHERE userid = $1", id))[0] > 0:
                cyclops = (f'\nCyclops: {str((await self.bot.pg_con.fetchrow("SELECT cyclops FROM inventory WHERE userid = $1", id))[0])}')
            else:
                cyclops = ''

            if (await self.bot.pg_con.fetchrow("SELECT fairy FROM inventory WHERE userid = $1", id))[0] > 0:
                fairy = (f'\nFairy: {str((await self.bot.pg_con.fetchrow("SELECT fairy FROM inventory WHERE userid = $1", id))[0])}')
            else:
                fairy = ''

            if (await self.bot.pg_con.fetchrow("SELECT medusa FROM inventory WHERE userid = $1", id))[0] > 0:
                medusa = (f'\nMedusa: {str((await self.bot.pg_con.fetchrow("SELECT medusa FROM inventory WHERE userid = $1", id))[0])}')
            else:
                medusa = ''

            await ctx.send(f'''{ctx.author.mention}```css\n[Inventory: Hunt]\n{boar}{goose}{python}{tiger}{dragon}{rabbit}{griffin}{manticore}{hydra}{bear}{panda}{cyclops}{fairy}{medusa}```''')
        
        elif category.lower() == 'ingredients':

            if (await self.bot.pg_con.fetchrow("SELECT rice FROM inventory WHERE userid = $1", id))[0] > 0:
                rice = (f'\nRice: {str((await self.bot.pg_con.fetchrow("SELECT rice FROM inventory WHERE userid = $1", id))[0])}')
            else:
                rice = ''

            if (await self.bot.pg_con.fetchrow("SELECT seaweed FROM inventory WHERE userid = $1", id))[0] > 0:
                seaweed = (f'\nSeaweed: {str((await self.bot.pg_con.fetchrow("SELECT seaweed FROM inventory WHERE userid = $1", id))[0])}')
            else:
                seaweed = ''
            
            if (await self.bot.pg_con.fetchrow("SELECT avocado FROM inventory WHERE userid = $1", id))[0] > 0:
                avocado = (f'\nAvocado: {str((await self.bot.pg_con.fetchrow("SELECT avocado FROM inventory WHERE userid = $1", id))[0])}')
            else:
                avocado = ''

            if (await self.bot.pg_con.fetchrow("SELECT sushi_kit FROM inventory WHERE userid = $1", id))[0] > 0:
                sushi_kit = (f'\nSushi Kit: {str((await self.bot.pg_con.fetchrow("SELECT sushi_kit FROM inventory WHERE userid = $1", id))[0])}')
            else:
                sushi_kit = ''

            if (await self.bot.pg_con.fetchrow("SELECT cocoa_beans FROM inventory WHERE userid = $1", id))[0] > 0:
                cocoa_beans = (f'\nCocoa Beans: {str((await self.bot.pg_con.fetchrow("SELECT cocoa_beans FROM inventory WHERE userid = $1", id))[0])}')
            else:
                cocoa_beans = ''

            if (await self.bot.pg_con.fetchrow("SELECT milk FROM inventory WHERE userid = $1", id))[0] > 0:
                milk = (f'\nMilk: {str((await self.bot.pg_con.fetchrow("SELECT milk FROM inventory WHERE userid = $1", id))[0])}')
            else:
                milk = ''

            if (await self.bot.pg_con.fetchrow("SELECT sugar FROM inventory WHERE userid = $1", id))[0] > 0:
                sugar = (f'\nSugar: {str((await self.bot.pg_con.fetchrow("SELECT sugar FROM inventory WHERE userid = $1", id))[0])}')
            else:
                sugar = ''

            if (await self.bot.pg_con.fetchrow("SELECT cocoa_butter FROM inventory WHERE userid = $1", id))[0] > 0:
                cocoa_butter = (f'\nCocoa Butter: {str((await self.bot.pg_con.fetchrow("SELECT cocoa_butter FROM inventory WHERE userid = $1", id))[0])}')
            else:
                cocoa_butter = ''
            
            if (await self.bot.pg_con.fetchrow("SELECT soy_lecithin FROM inventory WHERE userid = $1", id))[0] > 0:
                soy_lecithin = (f'\nSoy Lecithin: {str((await self.bot.pg_con.fetchrow("SELECT soy_lecithin FROM inventory WHERE userid = $1", id))[0])}')
            else:
                soy_lecithin = ''

            if (await self.bot.pg_con.fetchrow("SELECT vegetable_oil FROM inventory WHERE userid = $1", id))[0] > 0:
                vegetable_oil = (f'\nVegetable Oil: {str((await self.bot.pg_con.fetchrow("SELECT vegetable_oil FROM inventory WHERE userid = $1", id))[0])}')
            else:
                vegetable_oil = ''
            
            if (await self.bot.pg_con.fetchrow("SELECT vanilla FROM inventory WHERE userid = $1", id))[0] > 0:
                vanilla = (f'\nVanilla: {str((await self.bot.pg_con.fetchrow("SELECT vanilla FROM inventory WHERE userid = $1", id))[0])}')
            else:
                vanilla = ''

            if (await self.bot.pg_con.fetchrow("SELECT chocolate_kit FROM inventory WHERE userid = $1", id))[0] > 0:
                chocolate_kit = (f'\nChocolate Kit: {str((await self.bot.pg_con.fetchrow("SELECT chocolate_kit FROM inventory WHERE userid = $1", id))[0])}')
            else:
                chocolate_kit = ''

            await ctx.send(f'''{ctx.author.mention}```css\n[Inventory: Ingredients]\n{rice}{seaweed}{avocado}{sushi_kit}{cocoa_beans}{milk}{sugar}{cocoa_butter}{soy_lecithin}{vegetable_oil}{vanilla}{chocolate_kit}```''')

        elif category.lower() == 'sellable':

            if (await self.bot.pg_con.fetchrow("SELECT catfish FROM inventory WHERE userid = $1", id))[0] > 0:
                catfish = (f'\nCatfish: {str((await self.bot.pg_con.fetchrow("SELECT catfish FROM inventory WHERE userid = $1", id))[0])}')
            else:
                catfish = ''

            if (await self.bot.pg_con.fetchrow("SELECT mackerel FROM inventory WHERE userid = $1", id))[0] > 0:
                mackerel = (f'\nMackerel: {str((await self.bot.pg_con.fetchrow("SELECT mackerel FROM inventory WHERE userid = $1", id))[0])}')
            else:
                mackerel = ''
            
            if (await self.bot.pg_con.fetchrow("SELECT sardine FROM inventory WHERE userid = $1", id))[0] > 0:
                sardine = (f'\nSardine: {str((await self.bot.pg_con.fetchrow("SELECT sardine FROM inventory WHERE userid = $1", id))[0])}')
            else:
                sardine = ''

            if (await self.bot.pg_con.fetchrow("SELECT walleye FROM inventory WHERE userid = $1", id))[0] > 0:
                walleye = (f'\nWalleye: {str((await self.bot.pg_con.fetchrow("SELECT walleye FROM inventory WHERE userid = $1", id))[0])}')
            else:
                walleye = ''
            
            if (await self.bot.pg_con.fetchrow("SELECT salmon FROM inventory WHERE userid = $1", id))[0] > 0:
                salmon = (f'\nSalmon: {str((await self.bot.pg_con.fetchrow("SELECT salmon FROM inventory WHERE userid = $1", id))[0])}')
            else:
                salmon = ''

            if (await self.bot.pg_con.fetchrow("SELECT cod FROM inventory WHERE userid = $1", id))[0] > 0:
                cod = (f'\nCod: {str((await self.bot.pg_con.fetchrow("SELECT cod FROM inventory WHERE userid = $1", id))[0])}')
            else:
                cod = ''

            if (await self.bot.pg_con.fetchrow("SELECT tuna FROM inventory WHERE userid = $1", id))[0] > 0:
                tuna = (f'\nTuna: {str((await self.bot.pg_con.fetchrow("SELECT tuna FROM inventory WHERE userid = $1", id))[0])}')
            else:
                tuna = ''
            
            if (await self.bot.pg_con.fetchrow("SELECT whale FROM inventory WHERE userid = $1", id))[0] > 0:
                whale = (f'\nWhale: {str((await self.bot.pg_con.fetchrow("SELECT whale FROM inventory WHERE userid = $1", id))[0])}')
            else:
                whale = ''

            if (await self.bot.pg_con.fetchrow("SELECT mermaid FROM inventory WHERE userid = $1", id))[0] > 0:
                mermaid = (f'\nMermaid: {str((await self.bot.pg_con.fetchrow("SELECT mermaid FROM inventory WHERE userid = $1", id))[0])}')
            else:
                mermaid = ''

            if (await self.bot.pg_con.fetchrow("SELECT dragon FROM inventory WHERE userid = $1", id))[0] > 0:
                dragon = (f'\nDragon: {str((await self.bot.pg_con.fetchrow("SELECT dragon FROM inventory WHERE userid = $1", id))[0])}')
            else:
                dragon = ''
            
            if (await self.bot.pg_con.fetchrow("SELECT kraken FROM inventory WHERE userid = $1", id))[0] > 0:
                kraken = (f'\nKraken: {str((await self.bot.pg_con.fetchrow("SELECT kraken FROM inventory WHERE userid = $1", id))[0])}')
            else:
                kraken = ''

            if (await self.bot.pg_con.fetchrow("SELECT siren FROM inventory WHERE userid = $1", id))[0] > 0:
                siren = (f'\nSiren: {str((await self.bot.pg_con.fetchrow("SELECT siren FROM inventory WHERE userid = $1", id))[0])}')
            else:
                siren = ''

            if (await self.bot.pg_con.fetchrow("SELECT hydra FROM inventory WHERE userid = $1", id))[0] > 0:
                hydra = (f'\nHydra: {str((await self.bot.pg_con.fetchrow("SELECT hydra FROM inventory WHERE userid = $1", id))[0])}')
            else:
                hydra = ''

            if (await self.bot.pg_con.fetchrow("SELECT selkie FROM inventory WHERE userid = $1", id))[0] > 0:
                selkie = (f'\nSelkie: {str((await self.bot.pg_con.fetchrow("SELECT selkie FROM inventory WHERE userid = $1", id))[0])}')
            else:
                selkie = ''

            if (await self.bot.pg_con.fetchrow("SELECT technoblade FROM inventory WHERE userid = $1", id))[0] > 0:
                technoblade = (f'\nTechnoblade: {str((await self.bot.pg_con.fetchrow("SELECT technoblade FROM inventory WHERE userid = $1", id))[0])}')
            else:
                technoblade = ''

            if (await self.bot.pg_con.fetchrow("SELECT boar FROM inventory WHERE userid = $1", id))[0] > 0:
                boar = (f'\nBoar: {str((await self.bot.pg_con.fetchrow("SELECT boar FROM inventory WHERE userid = $1", id))[0])}')
            else:
                boar = ''

            if (await self.bot.pg_con.fetchrow("SELECT goose FROM inventory WHERE userid = $1", id))[0] > 0:
                goose = (f'\nGoose: {str((await self.bot.pg_con.fetchrow("SELECT goose FROM inventory WHERE userid = $1", id))[0])}')
            else:
                goose = ''
            
            if (await self.bot.pg_con.fetchrow("SELECT python FROM inventory WHERE userid = $1", id))[0] > 0:
                python = (f'\nPython: {str((await self.bot.pg_con.fetchrow("SELECT python FROM inventory WHERE userid = $1", id))[0])}')
            else:
                python = ''
            
            if (await self.bot.pg_con.fetchrow("SELECT tiger FROM inventory WHERE userid = $1", id))[0] > 0:
                tiger = (f'\nTiger: {str((await self.bot.pg_con.fetchrow("SELECT tiger FROM inventory WHERE userid = $1", id))[0])}')
            else:
                tiger = ''
            
            if (await self.bot.pg_con.fetchrow("SELECT dragon FROM inventory WHERE userid = $1", id))[0] > 0:
                dragon = (f'\nDragon: {str((await self.bot.pg_con.fetchrow("SELECT dragon FROM inventory WHERE userid = $1", id))[0])}')
            else:
                dragon = ''
            
            if (await self.bot.pg_con.fetchrow("SELECT rabbit FROM inventory WHERE userid = $1", id))[0] > 0:
                rabbit = (f'\nRabbit: {str((await self.bot.pg_con.fetchrow("SELECT rabbit FROM inventory WHERE userid = $1", id))[0])}')
            else:
                rabbit = ''

            if (await self.bot.pg_con.fetchrow("SELECT griffin FROM inventory WHERE userid = $1", id))[0] > 0:
                griffin = (f'\nGriffin: {str((await self.bot.pg_con.fetchrow("SELECT griffin FROM inventory WHERE userid = $1", id))[0])}')
            else:
                griffin = ''

            if (await self.bot.pg_con.fetchrow("SELECT manticore FROM inventory WHERE userid = $1", id))[0] > 0:
                manticore = (f'\nManticore: {str((await self.bot.pg_con.fetchrow("SELECT manticore FROM inventory WHERE userid = $1", id))[0])}')
            else:
                manticore = ''
            
            if (await self.bot.pg_con.fetchrow("SELECT hydra FROM inventory WHERE userid = $1", id))[0] > 0:
                hydra = (f'\nHydra: {str((await self.bot.pg_con.fetchrow("SELECT hydra FROM inventory WHERE userid = $1", id))[0])}')
            else:
                hydra = ''

            if (await self.bot.pg_con.fetchrow("SELECT bear FROM inventory WHERE userid = $1", id))[0] > 0:
                bear = (f'\nBear: {str((await self.bot.pg_con.fetchrow("SELECT bear FROM inventory WHERE userid = $1", id))[0])}')
            else:
                bear = ''
            
            if (await self.bot.pg_con.fetchrow("SELECT panda FROM inventory WHERE userid = $1", id))[0] > 0:
                panda = (f'\nPanda: {str((await self.bot.pg_con.fetchrow("SELECT panda FROM inventory WHERE userid = $1", id))[0])}')
            else:
                panda = ''

            if (await self.bot.pg_con.fetchrow("SELECT cyclops FROM inventory WHERE userid = $1", id))[0] > 0:
                cyclops = (f'\nCyclops: {str((await self.bot.pg_con.fetchrow("SELECT cyclops FROM inventory WHERE userid = $1", id))[0])}')
            else:
                cyclops = ''

            if (await self.bot.pg_con.fetchrow("SELECT fairy FROM inventory WHERE userid = $1", id))[0] > 0:
                fairy = (f'\nFairy: {str((await self.bot.pg_con.fetchrow("SELECT fairy FROM inventory WHERE userid = $1", id))[0])}')
            else:
                fairy = ''

            if (await self.bot.pg_con.fetchrow("SELECT medusa FROM inventory WHERE userid = $1", id))[0] > 0:
                medusa = (f'\nMedusa: {str((await self.bot.pg_con.fetchrow("SELECT medusa FROM inventory WHERE userid = $1", id))[0])}')
            else:
                medusa = ''

            await ctx.send(f'''{ctx.author.mention}```css\n[Inventory: Sellable]\n{boar}{goose}{python}{tiger}{dragon}{rabbit}{griffin}{manticore}{hydra}{bear}{panda}{cyclops}{fairy}{medusa}{catfish}{mackerel}{sardine}{walleye}{salmon}{cod}{tuna}{whale}{mermaid}{dragon}{kraken}{siren}{hydra}{selkie}{technoblade}```''')
        else:
            await ctx.send(f"{ctx.author.mention} Please specify a valid category. Categories: fish, food, hunt.")

    @commands.command(name = 'top', help = 'Check who is at the top of the leaderboard.')
    async def top(self, ctx):
        id = str(ctx.author.id)
        leaderboard = await self.bot.pg_con.fetch("SELECT (userid, quotes) FROM currency ORDER BY quotes DESC")
        leaderboard = str(leaderboard)
        leaderboard = leaderboard.replace("[", "").replace("<Record row=('", "").replace("'", "").replace(")>", "").replace("]", "")
        await ctx.send(leaderboard)
    
    @commands.cooldown(1, 180, commands.BucketType.user)
    @commands.command(name = 'fish', help = 'Fish some virtual fish to earn Quotes!')
    async def fish(self, ctx):
        id = str(ctx.author.id)
        await self.check_bal(id)
        await self.check_inv(id)
        fish_species = ['nothing', 'catfish', 'mackerel', 'sardine', 'walleye', 'salmon', 'cod', 'tuna', 'whale', 'mermaid', 'dragon', 'kraken', 'siren', 'hydra', 'technoblade', 'selkie']
        fish = (random.choices(fish_species, weights = (200, 160, 155, 153, 152, 150, 145, 143, 40, 20, 10, 6, 4, 3, 1, 8)))[0]
        if fish != 'nothing':
            species_amount = int((await self.bot.pg_con.fetchrow(f"SELECT {fish} FROM inventory WHERE userid = $1", id))[0])
            await self.bot.pg_con.execute(f"UPDATE inventory SET {fish} = $1 WHERE userid = $2", (species_amount + 1), id)
            current_species_amount = (await self.bot.pg_con.fetchrow(f"SELECT {fish} FROM inventory WHERE userid = $1", id))[0]
            await ctx.send(f"{ctx.author.mention} You fished up a **{fish}**, you now have {current_species_amount} {fish}.")
        else:
            await ctx.send(f"{ctx.author.mention} You fished up **nothing**. Better luck next time.")
    
    @commands.cooldown(1, 180, commands.BucketType.user)
    @commands.command(name = 'hunt', help = 'Hunt some virtual creatures to earn Quotes!')
    async def hunt(self, ctx):
        id = str(ctx.author.id)
        await self.check_bal(id)
        await self.check_inv(id)
        hunt_species = ['nothing', 'griffin', 'boar', 'goose', 'python', 'tiger', 'dragon', 'rabbit', 'manticore', 'hydra', 'bear', 'panda', 'cyclops', 'fairy', 'medusa']
        hunt = (random.choices(hunt_species, weights = (200, 15, 150, 165, 100, 65, 10, 135, 2, 3, 30, 15, 5, 10, 1)))[0]
        if hunt != 'nothing':
            species_amount = int((await self.bot.pg_con.fetchrow(f"SELECT {hunt} FROM inventory WHERE userid = $1", id))[0])
            await self.bot.pg_con.execute(f"UPDATE inventory SET {hunt} = $1 WHERE userid = $2", (species_amount + 1), id)
            current_species_amount = (await self.bot.pg_con.fetchrow(f"SELECT {hunt} FROM inventory WHERE userid = $1", id))[0]
            await ctx.send(f"{ctx.author.mention} You hunted a **{hunt}**, you now have {current_species_amount} {hunt}.")
        else:
            await ctx.send(f"{ctx.author.mention} You found **nothing** to hunt. Better luck next time.")

    @commands.command(name = 'sell', help = 'Sell some items that you have obtained from fishing, events, rewards, etc.')
    async def sell(self, ctx, amount = 1, *, item):
        item = (str(item.lower())).replace(' ', '_')
        amount = int(amount)
        id = str(ctx.author.id)
        bal = (await self.bot.pg_con.fetchrow("SELECT quotes FROM currency WHERE userid = $1", id))[0]
        await self.check_bal(id)
        await self.check_inv(id)
        sellable_items = {
        #Fish
        'catfish': 5, 
        'mackerel': 6, 
        'sardine': 7, 
        'walleye': 7, 
        'salmon': 9, 
        'cod': 8, 
        'tuna': 9, 
        'whale': 30, 
        'mermaid': 80, 
        'dragon': 140, 
        'kraken': 300, 
        'siren': 500,
        'selkie': 250,
        'technoblade': 1000, 
        'hydra': 700,

        #Hunt
        'boar': 6,
        'goose': 5,
        'python': 30,
        'tiger': 60,
        'dragon': 140,
        'rabbit': 12,
        'griffin': 100,
        'manticore': 800,
        'hydra': 700,
        'bear': 75,
        'panda': 100,
        'cyclops': 475,
        'fairy': 130,
        'medusa': 1000,

        #Food
        'tuna_roll': 6,
        'salmon_roll': 7,
        'milk_chocolate': 9,
        'dark_chocolate': 8,

        }

        if item in sellable_items:
            sell_price = int(sellable_items[item])
            item_in_inv = int((await self.bot.pg_con.fetchrow(f"SELECT {item} FROM inventory WHERE userid = $1", id))[0])

            if item_in_inv >= amount:
                if amount > 0:
                    total = int(amount * sell_price)
                    await self.bot.pg_con.execute(f"UPDATE inventory SET {item} = $1 WHERE userid = $2", item_in_inv - amount, id)
                    await self.balChange(id, total)
                    current_bal = (await self.bot.pg_con.fetchrow("SELECT quotes FROM currency WHERE userid = $1", id))[0]
                    item = (str(item.lower())).replace('_', ' ')
                    await ctx.send(f"{ctx.author.mention} You have sold {amount} {item}, earning {total} Quote/s. You now have {current_bal} Quote/s.")
                else:
                    await ctx.send(f"{ctx.author.mention} You cannot sell less than 1 item!")
            else:
                item = (str(item.lower())).replace('_', ' ')
                await ctx.send(f"{ctx.author.mention} You do not have {amount} {item} in your inventory.")
        else:
            await ctx.send(f'{ctx.author.mention} The item that you have specified is not sellable or invalid, please check the shop using $shop [category] for more info.')

    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.command(name = 'recipes', help = 'View food recipes to make food.')
    async def recipes(self, ctx):
        await ctx.send(
"""```css
[Sushi]

Tuna Avocado Roll (5 Servings)
* Sushi Kit
* 1 Avocado
* Rice
* Seaweed
* 1 Tuna

Salmon Avocado Roll (5 Servings)
* Sushi Kit
* 1 Avocado
* Rice
* Seaweed
* 1 Salmon

[Desserts]

Milk Chocolate (5 Bars)
* Cocoa beans
* Milk
* Sugar
* Cocoa Butter
* Soy Lecithin (Emulsifier)
* Vegetable Oil
* Vanilla
* Chocolate Kit

Dark Chocolate (5 Bars)
* Cocoa beans
* Sugar
* Cocoa Butter
* Soy Lecithin (Emulsifier)
* Vegetable Oil
* Vanilla
* Chocolate Kit

```""")

    
    @commands.cooldown(1, 600, commands.BucketType.user)
    @commands.command(name = 'cook', help = 'Cook food using virtual ingredients. Use $recipes to find out what food you can make.')
    async def cook(self, ctx, *, food):
        id = str(ctx.author.id)
        await self.check_bal(id)
        await self.check_inv(id)
        foods = {
            'Tuna Avocado Roll',
            'Salmon Avocado Roll',
            'Milk Chocolate',
            'Dark Chocolate'
        }      

        if food.title() in foods:
            sushi_kits = (await self.bot.pg_con.fetchrow("SELECT sushi_kit FROM inventory WHERE userid = $1", id))[0]
            avocados = (await self.bot.pg_con.fetchrow("SELECT avocado FROM inventory WHERE userid = $1", id))[0]
            rice = (await self.bot.pg_con.fetchrow("SELECT rice FROM inventory WHERE userid = $1", id))[0]
            seaweed = (await self.bot.pg_con.fetchrow("SELECT seaweed FROM inventory WHERE userid = $1", id))[0]
            tuna = (await self.bot.pg_con.fetchrow("SELECT tuna FROM inventory WHERE userid = $1", id))[0]
            salmon = (await self.bot.pg_con.fetchrow("SELECT salmon FROM inventory WHERE userid = $1", id))[0]
            cocoa_beans = (await self.bot.pg_con.fetchrow("SELECT cocoa_beans FROM inventory WHERE userid = $1", id))[0]
            milk = (await self.bot.pg_con.fetchrow("SELECT milk FROM inventory WHERE userid = $1", id))[0]
            sugar = (await self.bot.pg_con.fetchrow("SELECT sugar FROM inventory WHERE userid = $1", id))[0]
            cocoa_butter = (await self.bot.pg_con.fetchrow("SELECT cocoa_butter FROM inventory WHERE userid = $1", id))[0]
            soy_lecithin = (await self.bot.pg_con.fetchrow("SELECT soy_lecithin FROM inventory WHERE userid = $1", id))[0]
            vegetable_oil = (await self.bot.pg_con.fetchrow("SELECT vegetable_oil FROM inventory WHERE userid = $1", id))[0]
            vanilla = (await self.bot.pg_con.fetchrow("SELECT vanilla FROM inventory WHERE userid = $1", id))[0]
            chocolate_kit = (await self.bot.pg_con.fetchrow("SELECT chocolate_kit FROM inventory WHERE userid = $1", id))[0]

            if food.title() == 'Tuna Avocado Roll':
                if sushi_kits >= 1 and avocados >= 1 and rice >= 1 and seaweed >= 1 and tuna >= 1:
                    await self.bot.pg_con.execute("UPDATE inventory SET avocado = $1 WHERE userid = $2", avocados - 1, id)
                    await self.bot.pg_con.execute("UPDATE inventory SET rice = $1 WHERE userid = $2", rice - 1, id)
                    await self.bot.pg_con.execute("UPDATE inventory SET seaweed = $1 WHERE userid = $2", seaweed - 1, id)
                    await self.bot.pg_con.execute("UPDATE inventory SET tuna = $1 WHERE userid = $2", tuna - 1, id)

                    await ctx.send(f"{ctx.author.mention} You are now making {food}. Please wait 10 minutes.")
                    await asyncio.sleep(600)
                    tuna_rolls = (await self.bot.pg_con.fetchrow("SELECT tuna_roll FROM inventory WHERE userid = $1", id))[0]
                    await self.bot.pg_con.execute("UPDATE inventory SET tuna_roll = $1 WHERE userid = $2", tuna_rolls + 5, id)
                    await ctx.send(f"{ctx.author.mention} Your {food} is now ready.")

                else:
                    await ctx.send(f"{ctx.author.mention} You do not have all required ingredients, use $shop ingredients to buy ingredients and/or catch some fish ($fish) or hunt ($hunt).")

            elif food.title() == 'Salmon Avocado Roll':
                if sushi_kits >= 1 and avocados >= 1 and rice >= 1 and seaweed >= 1 and salmon >= 1:
                    await self.bot.pg_con.execute("UPDATE inventory SET avocado = $1 WHERE userid = $2", avocados - 1, id)
                    await self.bot.pg_con.execute("UPDATE inventory SET rice = $1 WHERE userid = $2", rice - 1, id)
                    await self.bot.pg_con.execute("UPDATE inventory SET seaweed = $1 WHERE userid = $2", seaweed - 1, id)
                    await self.bot.pg_con.execute("UPDATE inventory SET salmon = $1 WHERE userid = $2", salmon - 1, id)

                    await ctx.send(f"{ctx.author.mention} You are now making {food}. Please wait 10 minutes.")
                    await asyncio.sleep(600)
                    salmon_rolls = (await self.bot.pg_con.fetchrow("SELECT salmon_roll FROM inventory WHERE userid = $1", id))[0]
                    await self.bot.pg_con.execute("UPDATE inventory SET salmon_roll = $1 WHERE userid = $2", salmon_rolls + 5, id)
                    await ctx.send(f"{ctx.author.mention} Your {food} is now ready.")

                else:
                    await ctx.send(f"{ctx.author.mention} You do not have all required ingredients, use $shop food to buy ingredients and/or catch some fish ($fish) or hunt ($hunt). Note: when buying ingredients, seperate words with underscore in between, not space, however, you can use space for $cook.")

            elif food.title() == 'Milk Chocolate':
                if chocolate_kit >= 1 and cocoa_beans >= 1 and milk >= 1 and sugar >= 1 and cocoa_butter >= 1 and soy_lecithin >= 1 and vegetable_oil >= 1 and vanilla >= 1:
                    await self.bot.pg_con.execute("UPDATE inventory SET cocoa_beans = $1 WHERE userid = $2", cocoa_beans - 1, id)
                    await self.bot.pg_con.execute("UPDATE inventory SET milk = $1 WHERE userid = $2", milk - 1, id)
                    await self.bot.pg_con.execute("UPDATE inventory SET sugar = $1 WHERE userid = $2", sugar - 1, id)
                    await self.bot.pg_con.execute("UPDATE inventory SET cocoa_butter = $1 WHERE userid = $2", cocoa_butter - 1, id)
                    await self.bot.pg_con.execute("UPDATE inventory SET soy_lecithin = $1 WHERE userid = $2", soy_lecithin - 1, id)
                    await self.bot.pg_con.execute("UPDATE inventory SET vegetable_oil = $1 WHERE userid = $2", vegetable_oil - 1, id)
                    await self.bot.pg_con.execute("UPDATE inventory SET vanilla = $1 WHERE userid = $2", vanilla - 1, id)

                    await ctx.send(f"{ctx.author.mention} You are now making {food}. Please wait 10 minutes.")
                    await asyncio.sleep(600)
                    milk_chocolate = (await self.bot.pg_con.fetchrow("SELECT milk_chocolate FROM inventory WHERE userid = $1", id))[0]
                    await self.bot.pg_con.execute("UPDATE inventory SET milk_chocolate = $1 WHERE userid = $2", milk_chocolate + 5, id)
                    await ctx.send(f"{ctx.author.mention} Your {food} is now ready.")

                else:
                    await ctx.send(f"{ctx.author.mention} You do not have all required ingredients, use $shop food to buy ingredients and/or catch some fish ($fish) or hunt ($hunt).")

            elif food.title() == 'Dark Chocolate':
                if chocolate_kit >= 1 and cocoa_beans >= 1 and sugar >= 1 and cocoa_butter >= 1 and soy_lecithin >= 1 and vegetable_oil >= 1 and vanilla >= 1:
                    await self.bot.pg_con.execute("UPDATE inventory SET cocoa_beans = $1 WHERE userid = $2", cocoa_beans - 1, id)
                    await self.bot.pg_con.execute("UPDATE inventory SET sugar = $1 WHERE userid = $2", sugar - 1, id)
                    await self.bot.pg_con.execute("UPDATE inventory SET cocoa_butter = $1 WHERE userid = $2", cocoa_butter - 1, id)
                    await self.bot.pg_con.execute("UPDATE inventory SET soy_lecithin = $1 WHERE userid = $2", soy_lecithin - 1, id)
                    await self.bot.pg_con.execute("UPDATE inventory SET vegetable_oil = $1 WHERE userid = $2", vegetable_oil - 1, id)
                    await self.bot.pg_con.execute("UPDATE inventory SET vanilla = $1 WHERE userid = $2", vanilla - 1, id)

                    await ctx.send(f"{ctx.author.mention} You are now making {food}. Please wait 10 minutes.")
                    await asyncio.sleep(600)
                    dark_chocolate = (await self.bot.pg_con.fetchrow("SELECT dark_chocolate FROM inventory WHERE userid = $1", id))[0]
                    await self.bot.pg_con.execute("UPDATE inventory SET dark_chocolate = $1 WHERE userid = $2", dark_chocolate + 5, id)
                    await ctx.send(f"{ctx.author.mention} Your {food} is now ready.")

                else:
                    await ctx.send(f"{ctx.author.mention} You do not have all required ingredients, use $shop food to buy ingredients and/or catch some fish ($fish) or hunt ($hunt).")    
        else:
            await ctx.send(f"{ctx.author.mention} The food specified is not cookable, please check recipes using $recipes. You can make a suggestion to the developer for more food recipes to be added.")

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(name = 'p_sell', help = 'Sell your items to other users for Quotes.')
    async def p_sell(self, ctx, user, quotes, amount = 1, *, item):
        try:
            amount = int(amount)
        except ValueError:
            await ctx.send("Amount of items needs to be an integer!")

        try:
            quotes = int(quotes)
        except ValueError:
            await ctx.send("Amount of Quotes needs to be an integer!")

        item = (str(item.lower())).replace(' ', '_')
        id = str(ctx.author.id)
        await self.check_bal(id)
        await self.check_inv(id)

        sellable_items = {
            'tuna_roll',
            'salmon_roll',
            'milk_chocolate',
            'dark_chocolate',
            'rice',
            'avocado',
            'seaweed',
            'sushi_kit',
            'cocoa_beans',
            'milk',
            'sugar',
            'cocoa_butter',
            'soy_lecithin',
            'vegetable_oil',
            'vanilla',
            'chocolate_kit',
            'catfish',
            'mackerel',
            'sardine',
            'walleye',
            'salmon',
            'cod',
            'tuna',
            'whale',
            'mermaid',
            'dragon',
            'kraken',
            'siren',
            'selkie',
            'technoblade',
            'hydra',
            'boar',
            'goose',
            'python',
            'tiger',
            'rabbit',
            'griffin',
            'manticore',
            'bear',
            'panda',
            'cyclops',
            'fairy',
            'medusa',
        }

        if user.startswith("<@") and user.endswith(">"):
            if "<@!" in user:
                user = (user.removeprefix(str("<@!"))).removesuffix(str(">"))

            else:
                user = (user.removeprefix(str("<@"))).removesuffix(str(">"))
            
            if user == id:
                await ctx.send(f"{ctx.author.mention} You cannot sell items to yourself!")

            else:
                await self.check_bal(user)
                await self.check_inv(user)
    
                item_in_inv = (await self.bot.pg_con.fetchrow(f"SELECT {item} FROM inventory WHERE userid = $1", id))[0]
                if item in sellable_items:
                    if item_in_inv >= amount:
                        bal = (await self.bot.pg_con.fetchrow("SELECT quotes FROM currency WHERE userid = $1", id))[0]
                        user_bal = (await self.bot.pg_con.fetchrow("SELECT quotes FROM currency WHERE userid = $1", user))[0]
                        if quotes >= 0 and amount > 0:
                            if user_bal >= quotes:
                                item = (str(item.lower())).replace('_', ' ')
                                await ctx.send(f"<@{user}>\n{ctx.author.mention} has requested to sell you {amount} {item} for {quotes} Quotes. Do you accept? [yes/no]")

                                def check(msg):
                                    return str(msg.author.id) == str(user) and msg.channel == ctx.channel

                                try: 
                                    active = True
                                    while active == True:
                                        msg = await self.bot.wait_for('message', timeout = 30, check=check)
                                        if (msg.content).lower() == 'yes':
                                            item = (str(item.lower())).replace(' ', '_')
                                            user_item_in_inv = (await self.bot.pg_con.fetchrow(f"SELECT {item} FROM inventory WHERE userid = $1", user))[0]
                                            await self.bot.pg_con.execute(f"UPDATE inventory SET {item} = $1 WHERE userid = $2", user_item_in_inv + amount, user)
                                            await self.bot.pg_con.execute("UPDATE currency SET quotes = $1 WHERE userid = $2", user_bal - quotes, user)
                                            await self.bot.pg_con.execute(f"UPDATE inventory SET {item} = $1 WHERE userid = $2", item_in_inv - amount, id)
                                            await self.bot.pg_con.execute("UPDATE currency SET quotes = $1 WHERE userid = $2", bal + quotes, id)
                                            await ctx.send(f"{ctx.author.mention} <@{user}> Your transaction has been successfully processed.")
                                            active = False

                                        elif (msg.content).lower() == 'no':
                                            await ctx.send(f"{ctx.author.mention} <@{user}> Your transaction has been cancelled.")
                                            active = False

                                except asyncio.TimeoutError:
                                    await ctx.send(f"{ctx.author.mention} Timeout, your transaction has been cancelled.")
                                    active = False
                            else:
                                await ctx.send(f"{ctx.author.mention} The user specified does not have enough Quotes to buy your item/s.")
                        else:
                            await ctx.send(f"{ctx.author.mention} You cannot sell for a negative amount of Quotes nor sell less than 1 item!")
                    else:
                        item = (str(item.lower())).replace('_', ' ')
                        await ctx.send(f"{ctx.author.mention} You do not have {amount} {item}! Please check your inventory.")
                else:
                    item = (str(item.lower())).replace('_', ' ')
                    await ctx.send(f"{ctx.author.mention} The item you specified ({item}) is not sellable.")

        else:
            await ctx.send(f"{ctx.author.mention} Invalid user!")
    
    @commands.command(name = 'use', help = 'Use/eat an item in your inventory.')
    async def use(self, ctx, *, item):
        id = str(ctx.author.id)
        await self.check_bal(id)
        await self.check_inv(id)
        item = (str(item.lower())).replace(' ', '_')

        useable_items = {
            'milk_chocolate',
            'dark_chocolate',
            ''
        }

def setup(bot):
    bot.add_cog(Currency(bot))
