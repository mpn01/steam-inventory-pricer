import requests
import re
import sqlite3
import urllib.parse
import discord 
import os
import datetime
import asyncio
from commands import skins
from commands import cases
from commands import addcase
from commands import addskin
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()

bot = commands.Bot(command_prefix=".", intents=Intents.all())
DISCORD_KEY=os.getenv('DISCORD')

# ---BOT commands---
@bot.command(name="addskin")
async def command_addSkinToInventory(ctx, skinurl : str, quantity : int):
    for fetched_result, skinname in addskin.addCaseToInventory(skinurl, quantity):
        if fetched_result == 0:
            embed = discord.Embed(
                title = "Skin added",
                colour = discord.Colour.green(),
                description = skinname
            )
            await ctx.send(embed=embed)
        elif fetched_result == 1:
            embed = discord.Embed(
                title = "Added "+str(quantity)+" more cases",
                colour = discord.Colour.green(),
                description = skinname
            )
            await ctx.send(embed=embed)

@bot.command(name="addcase")
async def addCaseToInventory(ctx, caseurl : str, quantity : int):
    caseurl_unquoted = urllib.parse.unquote(caseurl)
    caseurl_unparsed = urllib.parse.urlparse(caseurl_unquoted)
    casename = caseurl_unparsed.path.lstrip("/market/listings/730/")
    data = [casename]
    result = conn.execute("SELECT EXISTS(SELECT quantity FROM cases WHERE name=?);", data)
    fetched_result = result.fetchone()[0]
    if fetched_result == 0:
        casedata = [casename, quantity]
        conn.execute("INSERT INTO cases(name, quantity) values(?,?);", casedata)
        conn.commit()
        embed = discord.Embed(
            title = "Case added",
            colour = discord.Colour.green(),
            description = casename
        )
        await ctx.send(embed=embed)
    elif fetched_result == 1:
        result_quantity = conn.execute("SELECT quantity FROM cases WHERE name=?", data)
        for x in result_quantity:
            quantity_increased = int(quantity) + int(x[0])
            casedata = [quantity_increased, casename]
            conn.execute("UPDATE cases SET quantity=? WHERE name=?;", casedata)
            conn.commit()
            embed = discord.Embed(
                title = "Added "+str(quantity)+" more cases",
                colour = discord.Colour.green(),
                description = casename
            )
            await ctx.send(embed=embed)

@bot.command(name="removeskin")
async def removeSkinFromInventory(ctx, skinname : str):
    sql = "DELETE FROM skins WHERE name = ?;"
    data = [skinname];
    conn.execute(sql, data)
    conn.commit()
    embed = discord.Embed(
        title = "Skin removed",
        description= skinname,
        colour = discord.Colour.red()
    )
    await ctx.send(embed=embed)

@bot.command(name="removecase")
async def removeCaseFromInventory(ctx, casename : str):
    sql_cases = "DELETE FROM cases WHERE name = ?;"
    data = [casename];
    conn.execute(sql_cases, data)
    conn.commit()
    embed = discord.Embed(
        title = "Case removed",
        description= casename,
        colour = discord.Colour.red()
    )
    await ctx.send(embed=embed)

@bot.command(name="skins")
async def command_getSkinPrices(ctx):
    sum = 0
    skins_value = []
    for name, skin_url, skin_thumbnail, quantity, price_formated, sum_price in skins.getSkinPrices():
        skins_value.append(price_formated*quantity)
        embed = discord.Embed(
            title = name,
            colour = discord.Colour.blue(),
            url = skin_url
        )
        embed.set_thumbnail(url=str(skin_thumbnail))
        embed.add_field(name = "Ilość", value=quantity, inline = False)
        embed.add_field(name = "Cena 1 szt.", value=str(price_formated)+" zł", inline = True)
        embed.add_field(name = "Cena", value=str(sum_price)+" zł", inline = True)
        # embed.add_field(name = "Cena netto", value=str(sum_price*0,8698)+" zł", inline = True)
        await ctx.send(embed=embed)
    for i in range(0,len(skins_value)):
        sum = round(sum + skins_value[i], 2)
    embedSumPrice = discord.Embed(
        title = str(sum)+" zł",
        colour = discord.Colour.green(),
        description= "Całkowita wartość skinów"
    )
    await ctx.send(embed=embedSumPrice)
    
@bot.command(name="cases")
async def command_getCasePrices(ctx):
    sum = 0
    cases_value = []
    for name, case_url, case_thumbnail, quantity, price_formated, sum_price in cases.getCasePrices():
        cases_value.append(price_formated*quantity)
        embed = discord.Embed(
            title = name,
            colour = discord.Colour.blue(),
            url = case_url
        )
        embed.set_thumbnail(url=str(case_thumbnail))
        embed.add_field(name = "Ilość", value=quantity, inline = False)
        embed.add_field(name = "Cena 1 szt.", value=str(price_formated)+" zł", inline = True)
        embed.add_field(name = "Cena", value=str(sum_price)+" zł", inline = True)
        # embed.add_field(name = "Cena netto", value=str(sum_price*0,8698)+" zł", inline = True)
        await ctx.send(embed=embed)
    for i in range(0,len(cases_value)):
        sum = round(sum + cases_value[i], 2)
    embedSumPrice = discord.Embed(
        title = str(sum)+" zł",
        colour = discord.Colour.green(),
        description= "Całkowita wartość skrzynek"
    )
    await ctx.send(embed=embedSumPrice)

# ---Scheduled functions---
def scheduledGetCasePrices():
    result = conn.execute("SELECT * FROM cases;")
    cases_price_sum = 0
    cases_value = []
    for row in result:
        response = requests.get("http://steamcommunity.com/market/priceoverview/?appid=730&currency=6&market_hash_name="+row[1]).json()
        price = response["lowest_price"]
        price_int = re.sub('[^\d+,\d{0,2}$]', '', price)
        price_formated = float(price_int.replace(',','.'))
        cases_value.append(price_formated*row[2])
    for i in range(0,len(cases_value)):
        cases_price_sum = round(cases_price_sum + cases_value[i], 2)
    return cases_price_sum

def scheduledGetSkinPrices():
    result = conn.execute("SELECT * FROM skins;")
    skins_price_sum = 0
    skins_value = []
    for row in result:
        response = requests.get("http://steamcommunity.com/market/priceoverview/?appid=730&currency=6&market_hash_name="+row[1]).json()
        price = response["lowest_price"]
        price_int = re.sub('[^\d+,\d{0,2}$]', '', price)
        price_formated = float(price_int.replace(',','.'))
        skins_value.append(price_formated*row[2])
    for i in range(0,len(skins_value)):
        skins_price_sum = round(skins_price_sum + skins_value[i], 2)
    return skins_price_sum

# every day at 10 AM send message with price of whole inventory
async def getPrices():
    while True:
        now = datetime.datetime.now()
        then = now+datetime.timedelta(days=1)
        then.replace(hour=10, minute=00)
        waittime = (then-now).total_seconds()
        await asyncio.sleep(waittime)

        channel = bot.get_channel(1017927811467591741)
        cases_price_sum = scheduledGetCasePrices()
        datetime.sleep(15)
        skins_price_sum = scheduledGetSkinPrices()
        sum_prices = float(round(skins_price_sum, 2))+float(round(cases_price_sum, 2))
        print(sum_prices)
        embed = discord.Embed(
            title = str(sum_prices)+" zł",
            colour = discord.Colour.yellow(),
            description= "Całkowita wartość ekwipunku"
        )
        embed.add_field(name = "W skinach", value=str(skins_price_sum)+" zł", inline = True)
        embed.add_field(name = "W skrzynkach", value=str(cases_price_sum)+" zł", inline = True)
        await channel.send(embed=embed)

@bot.event
async def on_ready():
    print("Listening for commands...")
    await getPrices()

if __name__ == "__main__":
    conn = sqlite3.connect('steaminventory.db')
    bot.run(DISCORD_KEY)    