import requests
import re
import sqlite3
import urllib.parse
import discord
from discord import Intents
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix=".", intents=Intents.all())
channel = bot.get_channel(1017927811467591741)
DISCORD_KEY=os.getenv('DISCORD')

@bot.event
async def on_ready():
    print("Listening...")

def addSkinToInventory(itemurl: str, quantity: int):
    itemurl_unquoted = urllib.parse.unquote(itemurl)
    itemurl_unparsed = urllib.parse.urlparse(itemurl_unquoted)
    itemname = itemurl_unparsed.path.lstrip("/martket/listings/730/")
    data = [itemname]
    result = conn.execute("SELECT quantity FROM skins WHERE name=?;", data)
    print(result)
    for row in result:
        if row[0] > 0:
            itemdata = [itemname, quantity]
            conn.execute("INSERT INTO skins(name, quantity) values(?,?);", itemdata)
        elif row[0] == 0:
            quantity_increased = int(quantity) + int(row[0])
            itemdata = [quantity_increased, itemname]
            conn.execute("UPDATE skins SET quantity=? WHRE name=?;", itemdata)
            conn.commit()

def addCaseToInventory(caseurl : str, quantity: int):
    caseurl_unquoted = urllib.parse.unquote(caseurl)
    caseurl_unparsed = urllib.parse.urlparse(caseurl_unquoted)
    casename = caseurl_unparsed.path.lstrip("/market/listings/730/")
    data = [casename]
    result = conn.execute("SELECT quantity FROM cases WHERE name=?;", data)
    for row in result:
        if row[0] == 0:
            casedata = [casename, quantity]
            conn.execute("INSERT INTO cases(name, quantity) values(?,?);", casedata)
        elif row[0] > 0:
            quantity_increased = int(quantity) + int(row[0])
            casedata = [quantity_increased, casename]
            conn.execute("UPDATE cases SET quantity=? WHERE name=?;", casedata)
            conn.commit()

def removeSkinFromInventory(itemname : str):
    sql = "DELETE FROM skins WHERE name = ?;"
    data = [itemname];
    conn.execute(sql, data)
    conn.commit()

def removeCaseFromInventory(casename : str):
    sql_cases = "DELETE FROM cases WHERE name = ?;"
    data = [casename];
    conn.execute(sql_cases, data)
    conn.commit()

@bot.command(name="skins")
async def getSkinPrices(ctx):
    result = conn.execute("SELECT * FROM skins;")
    sum = 0
    skins_value = []
    for row in result:
        response = requests.get("http://steamcommunity.com/market/priceoverview/?appid=730&currency=6&market_hash_name="+row[1]).json()
        price = response["lowest_price"]
        price_int = re.sub('[^\d+,\d{0,2}$]', '', price)
        price_formated = float(price_int.replace(',','.'))
        sum_price = round(price_formated*row[2], 2)
        # print(row[1], "=>", price_formated, "zł", "|", price_formated*row[2],"zł")
        skins_value.append(price_formated*row[2])
        skin_row = urllib.parse.quote(row[1])
        skin_url = "https://steamcommunity.com/market/listings/730/"+skin_row
        embed = discord.Embed(
                title = row[1],
                colour = discord.Colour.blue(),
                url = skin_url
            )
        embed.set_thumbnail(url=str(row[3]))
        embed.add_field(name = "Ilość", value=row[2], inline = False)
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
    # print("Total value:", str(sum), "zł")

@bot.command(name="cases")
async def getCasePrices(ctx):
    result = conn.execute("SELECT * FROM cases;")
    sum = 0
    cases_value = []
    for row in result:
        response = requests.get("http://steamcommunity.com/market/priceoverview/?appid=730&currency=6&market_hash_name="+row[1]).json()
        price = response["lowest_price"]
        price_int = re.sub('[^\d+,\d{0,2}$]', '', price)
        price_formated = float(price_int.replace(',','.'))
        sum_price = round(price_formated*row[2], 2)
        # print(row[1],"=>", price_formated, "zł", "|", round(price_formated*row[2], 2), "zł")
        cases_value.append(price_formated*row[2])
        case_row = urllib.parse.quote(row[1])
        case_url = "https://steamcommunity.com/market/listings/730/"+case_row
        embed = discord.Embed(
                title = row[1],
                colour = discord.Colour.blue(),
                url = case_url
            )
        embed.set_thumbnail(url=str(row[3]))
        embed.add_field(name = "Ilość", value=row[2], inline = False)
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
    # print("Total value:", str(sum), "zł")

if __name__ == "__main__":
    conn = sqlite3.connect('steaminventory.db')
    bot.run(DISCORD_KEY)