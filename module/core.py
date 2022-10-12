import sqlite3
import discord
import os
from commands import skins
from commands import cases
from commands import addskin
from commands import addcase
from commands import track
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
async def removeSkinFromInventory(ctx, *, user_input : str):
    sql_select_skin = f"SELECT name FROM skins WHERE name LIKE '%{user_input}%';"
    result = conn.execute(sql_select_skin)
    for row in result:
        skin_name = row[0]
    sql_delete_skin = f"DELETE FROM skins WHERE name='{skin_name}';"
    conn.execute(sql_delete_skin)
    conn.commit()
    embed = discord.Embed(
        title = "Skin removed",
        description= skin_name,
        colour = discord.Colour.red()
    )
    await ctx.send(embed=embed)

@bot.command(name="removecase")
async def removeCaseFromInventory(ctx, *, user_input : str):
    sql_select_case = f"SELECT name FROM cases WHERE name LIKE '%{user_input}%';"
    result = conn.execute(sql_select_case)
    for row in result:
        case_name = row[0]
    sql_delete_case = f"DELETE FROM cases WHERE name='{case_name}';"
    conn.execute(sql_delete_case)
    conn.commit()
    embed = discord.Embed(
        title = "Case removed",
        description= case_name,
        colour = discord.Colour.red()
    )
    await ctx.send(embed=embed)

@bot.command(name="skins")
async def command_getSkinPrices(ctx, *, user_input=None):
    if user_input == None:
        sql_query = "SELECT * FROM skins WHERE status='tracked';"
        sum = 0
        skins_value = []
        for skin_name, skin_quantity, skin_url, skin_thumbnail, skin_formated_price, skin_sum_price, skin_net_price in skins.getSkins(all_skins=True, query=sql_query):
            skins_value.append(skin_formated_price*skin_quantity)
            embed = discord.Embed(
                title = skin_name,
                colour = discord.Colour.blue(),
                url = skin_url
            )
            embed.set_thumbnail(url = str(skin_thumbnail))
            embed.add_field(name = "Ilość", value = skin_quantity, inline = False)
            embed.add_field(name = "Cena 1 szt.", value = f"{skin_formated_price} zł", inline = True)
            embed.add_field(name = "Cena", value = f"{skin_sum_price} zł", inline = True)
            embed.add_field(name = "Cena netto", value = f"{skin_net_price} zł", inline = True)
            await ctx.send(embed = embed)
        for i in range(0,len(skins_value)):
            sum = round(sum + skins_value[i], 2)
        embedSumPrice = discord.Embed(
            title = str(sum)+" zł",
            colour = discord.Colour.green(),
            description = "Całkowita wartość skinów"
        )
        await ctx.send(embed=embedSumPrice)
    else:
        sql_query = f"SELECT * FROM skins WHERE name LIKE '%{user_input}%';"
        for skin_name, skin_status, skin_cost, skin_origin, skin_url, skin_formated_price, skin_sum_price, skin_thumbnail, skin_quantity in skins.getSkins(all_skins=False, query=sql_query):
            embed = discord.Embed(
                title = skin_name,
                colour = discord.Colour.blue(),
                url = skin_url
            )
            embed.set_thumbnail(url=str(skin_thumbnail))
            embed.add_field(name = "Ilość", value = skin_quantity, inline = False)
            embed.add_field(name = "Cena 1 szt.", value = f"{skin_formated_price} zł", inline = True)
            embed.add_field(name = "Wartość", value = f"{skin_sum_price} zł", inline = True)
            embed.add_field(name = "Kupiono za", value = f"{skin_cost} zł", inline = True)
            embed.add_field(name = "Pochodzenie", value = f"{skin_origin}", inline = True)
            embed.add_field(name = "Status", value = skin_status, inline = True)
            await ctx.send(embed = embed)

@bot.command(name="cases")
async def command_getCasePrices(ctx, *, user_input=None):
    if user_input == None:
        sql_query = "SELECT * FROM cases WHERE status = 'tracked';"
        sum = 0
        cases_value = []
        for case_name, case_quantity, case_url, case_thumbnail, case_formated_price, case_sum_price in cases.getCases(all_cases=True, query=sql_query):
            cases_value.append(case_formated_price*case_quantity)
            embed = discord.Embed(
                title = case_name,
                colour = discord.Colour.blue(),
                url = case_url
            )
            embed.set_thumbnail(url = str(case_thumbnail))
            embed.add_field(name = "Ilość", value = case_quantity, inline = False)
            embed.add_field(name = "Cena 1 szt.", value = str (case_formated_price)+" zł", inline = True)
            embed.add_field(name = "Cena", value=str(case_sum_price)+" zł", inline = True)
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
    else:
        sql_query = f"SELECT * FROM cases WHERE name LIKE '%{user_input}%';"
        for case_name, case_quantity, case_status, case_url, case_formated_price, case_sum_price, case_thumbnail in cases.getCases(all_cases=False, query=sql_query):
            embed = discord.Embed(
                title = case_name,
                colour = discord.Colour.blue(),
                url = case_url
            )
            embed.set_thumbnail(url=str(case_thumbnail))
            embed.add_field(name = "Ilość", value = case_quantity, inline = False)
            embed.add_field(name = "Cena 1 szt.", value = f"{case_formated_price} zł", inline = True)
            embed.add_field(name = "Wartość", value = f"{case_sum_price} zł", inline = True)
            embed.add_field(name = "Status", value = case_status, inline = True)
            await ctx.send(embed = embed)

@bot.command(name="trackcase")
async def command_trackCase(ctx, *, user_input):
    case_name = track.changeStatus(user_input, "cases", "tracked")
    embed = discord.Embed(
        title = "Skrzynia oznaczona jako śledzona",
        colour = discord.Colour.yellow(),
        description = case_name
    )
    await ctx.send(embed=embed)

@bot.command(name="untrackcase")
async def command_trackCase(ctx, *, user_input):
    case_name = track.changeStatus(user_input, "cases", "untracked")
    embed = discord.Embed(
        title = "Przestano śledzić skrzynię",
        colour = discord.Colour.yellow(),
        description = case_name
    )
    await ctx.send(embed=embed)

@bot.command(name="trackskin")
async def command_trackCase(ctx, *, user_input):
    skin_name = track.changeStatus(user_input, "skins", "tracked")
    embed = discord.Embed(
        title = "Skin oznaczony jako śledzony",
        colour = discord.Colour.yellow(),
        description = skin_name
    )
    await ctx.send(embed=embed)

@bot.command(name="untrackskin")
async def command_trackCase(ctx, *, user_input):
    skin_name = track.changeStatus(user_input, "skins", "untracked")
    embed = discord.Embed(
        title = "Przestano śledzić skina",
        colour = discord.Colour.yellow(),
        description = skin_name
    )
    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    print("Listening for commands...")

if __name__ == "__main__":
    conn = sqlite3.connect('steaminventory.db')
    bot.run(DISCORD_KEY)