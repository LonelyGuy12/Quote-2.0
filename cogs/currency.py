import random
import math
import time
from datetime import date, datetime, timedelta  

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
        print("ready")
        await self.bot.pg_con.execute("CREATE TABLE IF NOT EXISTS currency (userid TEXT NOT NULL, quotes INT)")
        await self.bot.pg_con.execute("ALTER TABLE currency ADD COLUMN IF NOT EXISTS userid TEXT NOT NULL")
        await self.bot.pg_con.execute("ALTER TABLE currency ADD COLUMN IF NOT EXISTS quotes INT")

        await self.bot.pg_con.execute("CREATE TABLE IF NOT EXISTS cooldown (userid TEXT NOT NULL, time TIMESTAMP NOT NULL)")
        await self.bot.pg_con.execute("ALTER TABLE cooldown ADD COLUMN IF NOT EXISTS userid TEXT NOT NULL")
        await self.bot.pg_con.execute("ALTER TABLE cooldown ADD COLUMN IF NOT EXISTS time TIMESTAMP NOT NULL")

        await self.bot.pg_con.execute("""CREATE TABLE IF NOT EXISTS inventory 
        (userid TEXT NOT NULL, 
        pizzas INT NOT NULL DEFAULT 0, 
        sushi INT NOT NULL DEFAULT 0, 
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
        siren INT NOT NULL DEFAULT 0)""")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS userid TEXT NOT NULL")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS pizzas INT NOT NULL DEFAULT 0")
        await self.bot.pg_con.execute("ALTER TABLE inventory ADD COLUMN IF NOT EXISTS sushi INT NOT NULL DEFAULT 0")
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
    async def bal(self, ctx):
        id = str(ctx.author.id)
        await self.check_bal(id)
        bal = await ctx.bot.pg_con.fetchrow("SELECT quotes FROM currency WHERE userid = $1", id)
        await ctx.send(f'{ctx.author.mention} Your balance: {bal[0]} Quote/s')

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
    @commands.command(name = 'quiz', help = 'Test your knowledge in multiple quiz categories! At the moment, the categories are: quick maths.')
    async def quiz(self, ctx, category):
        id = str(ctx.author.id)
        await self.check_bal(id)
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

    @commands.cooldown(1, 3600, commands.BucketType.user)
    @commands.command(name = "work", help = "Earn Quotes by working.")
    async def work(self, ctx):
        id = str(ctx.author.id)
        await self.check_bal(id)
        bal = await ctx.bot.pg_con.fetchrow("SELECT quotes FROM currency WHERE userid = $1", id)
        bal = bal[0]
        jobs = ['a cleaner', 'a dentist', 'a GP doctor', 'a surgeon', 'a welder', 'a miner', 'a pro gamer', 'a streamer', 'a volunteer', 'a terrorist', "a McDonald's employee", 'a chef']
        job = random.choices(jobs, weights = (50, 15, 12, 9, 30, 14, 37, 47, 35, 4, 49, 33))
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
                await ctx.send(f"{ctx.author.mention} Your {random.choice(scams)} scam was discoverd because {random.choice(reasons_scam)}! You were fined {round((100 - fine)/100 * bal)} Quote/s ({100 - fine}% of your Quotes).\nYou now have {round((float(fine) / 100) * bal)} Quote/s.")
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
    @commands.command(name = 'shop', help = "See what's available in the virtual shop.")
    async def shop(self, ctx):
        await ctx.send("""```css
[Shop]

Pizza - 5 Quotes
Sushi - 4 Quotes
```""")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name = 'buy', help = 'Buy virtual items from the virtual shop with your Quotes.')
    async def buy(self, ctx, item, amount):
        try:
            amount = int(amount)
            id = str(ctx.author.id)
            await self.check_bal(id)
            await self.check_inv(id)
            bal = await self.bot.pg_con.fetchrow("SELECT quotes FROM currency WHERE userid = $1", id)
            bal = bal[0]
            pizzas = await self.bot.pg_con.fetchrow("SELECT pizzas FROM inventory WHERE userid = $1", id)
            pizzas = pizzas[0]
            sushi = await self.bot.pg_con.fetchrow("SELECT sushi FROM inventory WHERE userid = $1", id)
            sushi = sushi[0]

            if amount == 1:
                plural  = ''
                valid = True
            elif amount > 1:
                plural = 's'
                valid = True
            elif amount <= 0:
                valid = False
            else:
                valid = False

            if item.lower() == 'pizza' and valid == True:
                price = int(5)
                total = int(price * amount)
                if bal >= total:
                    await self.balChange(id, -total)
                    current_bal = await self.bot.pg_con.fetchrow("SELECT quotes FROM currency WHERE userid = $1", id)
                    current_bal = current_bal[0]
                    await self.bot.pg_con.execute("UPDATE inventory SET pizzas = $1 WHERE userid = $2", amount + pizzas, id)
                    current_pizzas = await self.bot.pg_con.fetchrow("SELECT pizzas FROM inventory WHERE userid = $1", id)
                    current_pizzas = current_pizzas[0]
                    await ctx.send(f"{ctx.author.mention} Thank you for purchasing {amount} {item}{plural}! You have spent a total of {total} Quotes. You now have {current_bal} Quotes and {current_pizzas} pizzas.")
                elif valid == False:
                    await ctx.send(f"{ctx.author.mention} Invalid input.")
                else:
                    await ctx.send(f"{ctx.author.mention} You do not have enough money to purchase this item! Use $shop to check the prices of items.")
            
            elif item.lower() == 'sushi' and valid == True:
                price = int(4)
                total = int(price * amount)
                if bal >= total:
                    await self.balChange(id, -total)
                    current_bal = await self.bot.pg_con.fetchrow("SELECT quotes FROM currency WHERE userid = $1", id)
                    current_bal = current_bal[0]
                    await self.bot.pg_con.execute("UPDATE inventory SET sushi = $1 WHERE userid = $2", amount + sushi, id) 
                    current_sushi = await self.bot.pg_con.fetchrow("SELECT sushi FROM inventory WHERE userid = $1", id)
                    current_sushi = current_sushi[0]
                    await ctx.send(f"{ctx.author.mention} Thank you for purchasing {amount} {item}! You have spent a total of {total} Quotes. You now have {current_bal} Quotes and {current_sushi} sushi.")
                elif valid == False:
                    await ctx.send(f"{ctx.author.mention} Invalid input.")
                else:
                    await ctx.send(f"{ctx.author.mention} You do not have enough money to purchase this item! Use $shop to check the prices of items.")

        except ValueError:
            await ctx.send(f"{ctx.author.mention} Error, check the command usage using `$help [command]`.")
            
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name = 'inventory' and 'inv', help = 'Checks your for items that you have purchased. Categories are: food, fish.')
    async def inventory(self, ctx, category):
        id = str(ctx.author.id)
        await self.check_bal(id)
        await self.check_inv(id)

        if category == 'food':
            if  (await self.bot.pg_con.fetchrow("SELECT pizzas FROM inventory WHERE userid = $1", id))[0] > 0:
                pizza = (f'\nPizza: {str((await self.bot.pg_con.fetchrow("SELECT pizzas FROM inventory WHERE userid = $1", id))[0])}')
            else:
                pizza = ''

            if (await self.bot.pg_con.fetchrow("SELECT sushi FROM inventory WHERE userid = $1", id))[0] > 0:
                sushi = (f'\nSushi: {str((await self.bot.pg_con.fetchrow("SELECT sushi FROM inventory WHERE userid = $1", id))[0])}')
            else:
                sushi = ''

            await ctx.send(f'''{ctx.author.mention}```css\n[Inventory: Food]\n{pizza}{sushi}```''')

        if category == 'fish':

            if (await self.bot.pg_con.fetchrow("SELECT catfish FROM inventory WHERE userid = $1", id))[0] > 0:
                catfish = (f'\nCatfish: {str((await self.bot.pg_con.fetchrow("SELECT catfish FROM inventory WHERE userid = $1", id))[0])}')
            else:
                catfish = ''

            if (await self.bot.pg_con.fetchrow("SELECT mackerel FROM inventory WHERE userid = $1", id))[0] > 0:
                mackerel = (f'\nMackerel: {str((await self.bot.pg_con.fetchrow("SELECT mackerel FROM inventory WHERE userid = $1", id))[0])}')
            else:
                mackerel = ''
            
            if (await self.bot.pg_con.fetchrow("SELECT sardine FROM inventory WHERE userid = $1", id))[0] > 0:
                sardine = (f'\nSardine: {str((await self.bot.pg_con.fetchrow("SELECT mackerel FROM inventory WHERE userid = $1", id))[0])}')
            else:
                sardine = ''

            if (await self.bot.pg_con.fetchrow("SELECT walleye FROM inventory WHERE userid = $1", id))[0] > 0:
                walleye = (f'\nWalleye: {str((await self.bot.pg_con.fetchrow("SELECT walleye FROM inventory WHERE userid = $1", id))[0])}')
            else:
                walleye = ''
            
            if (await self.bot.pg_con.fetchrow("SELECT salmon FROM inventory WHERE userid = $1", id))[0] > 0:
                salmon = (f'\Salmon: {str((await self.bot.pg_con.fetchrow("SELECT salmon FROM inventory WHERE userid = $1", id))[0])}')
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

            await ctx.send(f'''{ctx.author.mention}```css\n[Inventory: Fish]\n{catfish}{mackerel}{sardine}{walleye}{salmon}{cod}{tuna}{whale}{mermaid}{dragon}{kraken}{siren}```''')


    @commands.command(name = 'top', help = 'Check who is at the top of the leaderboard.')
    async def top(self, ctx):
        id = str(ctx.author.id)
        leaderboard = await self.bot.pg_con.fetch("SELECT (userid, quotes) FROM currency ORDER BY quotes DESC")
        leaderboard = str(leaderboard)
        leaderboard = leaderboard.replace("[", "").replace("<Record row=('", "").replace("'", "").replace(")>", "").replace("]", "")
        await ctx.send(leaderboard)
    
    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.command(name = 'fish', help = 'Fish some virtual fish to earn Quotes!')
    async def fish(self, ctx):
        id = str(ctx.author.id)
        await self.check_bal(id)
        await self.check_inv(id)
        fish_species = ['nothing', 'catfish', 'mackerel', 'sardine', 'walleye', 'salmon', 'cod', 'tuna', 'whale', 'mermaid', 'dragon', 'kraken', 'siren']
        fish = (random.choices(fish_species, weights = (125, 100, 95, 93, 92, 90, 88, 87, 30, 15, 7, 4, 2)))[0]
        if fish != 'nothing':
            species_amount = int((await self.bot.pg_con.fetchrow(f"SELECT {fish} FROM inventory WHERE userid = $1", id))[0])
            await self.bot.pg_con.execute(f"UPDATE inventory SET {fish} = $1 WHERE userid = $2", (species_amount + 1), id)
            current_species_amount = (await self.bot.pg_con.fetchrow(f"SELECT {fish} FROM inventory WHERE userid = $1", id))[0]
            await ctx.send(f"You fished up a **{fish}**, you now have {current_species_amount} {fish}.")
        else:
            await ctx.send(f"You fished up **nothing**. Better luck next time.")
    
    @commands.command(name = 'sell', help = 'Sell some items that you have obtained from fishing, events, rewards, etc.')
    async def sell(self, ctx, item):
        id = str(ctx.author.id)
        await self.check_bal(id)
        await self.check_inv(id)



def setup(bot):
    bot.add_cog(Currency(bot))
