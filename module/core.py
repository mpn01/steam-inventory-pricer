import sqlite3
import discord
import os
from commands import skins
from commands import cases
from commands import addskin
from commands import addcase
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix=".", intents=Intents.all())
DISCORD_KEY=os.getenv('DISCORD')

@bot.command(name="addskin")
async def command_addSkinToInventory(ctx, skinurl : str, quantity : int):
    for fetched_result, skinname in addskin.addSkinToInventory(skinurl, quantity):
        if fetched_result == 0:
            embed = discord.Embed(
                title = "Skin added",
                colour = discord.Colour.green(),
                description = skinname
            )
            await ctx.send(embed=embed)
        elif fetched_result == 1:
            embed = discord.Embed(
                title = "Added "+str(quantity)+" more skin(s)",
                colour = discord.Colour.green(),
                description = skinname
            )
            await ctx.send(embed=embed)

@bot.command(name="addcase")
async def command_addCaseToInventory(ctx, caseurl : str, quantity : int):
    for fetched_result, casename in addcase.addCaseToInventory(caseurl, quantity):
        if fetched_result == 0:
            embed = discord.Embed(
                title = "Case added",
                colour = discord.Colour.green(),
                description = casename
            )
            await ctx.send(embed=embed)
        elif fetched_result == 1:
                embed = discord.Embed(
                    title = "Added "+str(quantity)+" more case(s)",
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
async def command_getSkinPrices(ctx, user_input=None):
    if user_input == None:
        sum = 0
        skins_value = []
        for name, skin_url, skin_thumbnail, quantity, price_formated, sum_price in skins.getSkinPrices(all_skins=True, input=None):
            net_price = round(sum_price*0.8698, 2)
            skins_value.append(price_formated*quantity)
            embed = discord.Embed(
                title = name,
                colour = discord.Colour.blue(),
                url = skin_url
            )
            embed.set_thumbnail(url=str(skin_thumbnail))
            embed.add_field(name = "Ilość", value=quantity, inline = False)
            embed.add_field(name = "Cena 1 szt.", value=f"{price_formated} zł", inline = True)
            embed.add_field(name = "Cena", value=f"{sum_price} zł", inline = True)
            embed.add_field(name = "Cena netto", value=f"{net_price} zł", inline = True)
            await ctx.send(embed=embed)
        for i in range(0,len(skins_value)):
            sum = round(sum + skins_value[i], 2)
        embedSumPrice = discord.Embed(
            title = str(sum)+" zł",
            colour = discord.Colour.green(),
            description= "Całkowita wartość skinów"
        )
        await ctx.send(embed=embedSumPrice)
    else:
        for name, status, cost, origin, url, thumbnail, price, sum_price, quantity in skins.getSkinPrices(all_skins=False, input=user_input):
            embed = discord.Embed(
                title = name,
                colour = discord.Colour.blue(),
                url = url
            )
            embed.set_thumbnail(url=str(thumbnail))
            embed.add_field(name = "Ilość", value = quantity, inline = False)
            embed.add_field(name = "Cena 1 szt.", value = f"{price} zł", inline = True)
            embed.add_field(name = "Wartość", value = f"{sum_price} zł", inline = True)
            embed.add_field(name = "Kupiono za", value = f"{cost} zł", inline = True)
            embed.add_field(name = "Pochodzenie", value = f"{origin}", inline = True)
            embed.add_field(name = "Status", value = status, inline = True)
            await ctx.send(embed = embed)

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

@bot.event
async def on_ready():
    print("Listening for commands...")

if __name__ == "__main__":
    conn = sqlite3.connect('steaminventory.db')
    bot.run(DISCORD_KEY)