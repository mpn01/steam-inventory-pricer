import requests, re, sqlite3, urllib.parse, discord, os, datetime, asyncio
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

bot = commands.Bot(command_prefix=".", intents=Intents.all())
DISCORD_KEY=os.getenv('DISCORD')

# ---BOT commands---
@bot.command(name="addskin")
async def addSkinToInventory(ctx, skinurl : str, quantity : int):
    skinurl_unquoted = urllib.parse.unquote(skinurl)
    skinurl_unparsed = urllib.parse.urlparse(skinurl_unquoted)
    skinname = skinurl_unparsed.path.lstrip("/martket/listings/730/")
    data = [skinname]
    result = conn.execute("SELECT quantity FROM skins WHERE name=?;", data)
    print(result)
    for row in result:
        if row[0] > 0:
            skindata = [skinname, quantity]
            conn.execute("INSERT INTO skins(name, quantity) values(?,?);", skindata)
        elif row[0] == 0:
            quantity_increased = int(quantity) + int(row[0])
            skindata = [quantity_increased, skinname]
            conn.execute("UPDATE skins SET quantity=? WHRE name=?;", skindata)
            conn.commit()
    embed = discord.Embed(
        title = "Case added",
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
    result = conn.execute("SELECT quantity FROM cases WHERE name=?;", data)
    for row in result:
        if row[0] == 0:
            casedata = [casename, quantity]
            conn.execute("INSERT INTO cases(name, quantity) values(?,?);", casedata)
            conn.commit()
            embed = discord.Embed(
                title = "Case added",
                colour = discord.Colour.green(),
                description = casename
            )
            await ctx.send(embed=embed)
        elif row[0] > 0:
            quantity_increased = int(quantity) + int(row[0])
            casedata = [quantity_increased, casename]
            conn.execute("UPDATE cases SET quantity=? WHERE name=?;", casedata)
            conn.commit()
            embed = discord.Embed(
                title = "Added more cases",
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
async def getSkinPrices(ctx):
    result = conn.execute("SELECT * FROM skins WHERE status='tracked';")
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
        img_url = requests.get(skin_url)
        soup = BeautifulSoup(img_url.text, 'html.parser')
        for item in soup.select('.market_listing_largeimage'):
            skin_thumbnail = item.find('img').attrs['src']
        embed = discord.Embed(
            title = row[1],
            colour = discord.Colour.blue(),
            url = skin_url
        )
        embed.set_thumbnail(url=str(skin_thumbnail))
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

@bot.command(name="cases")
async def getCasePrices(ctx):
    result = conn.execute("SELECT * FROM cases WHERE status='tracked';")
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
        img_url = requests.get(case_url)
        soup = BeautifulSoup(img_url.text, 'html.parser')
        for item in soup.select('.market_listing_largeimage'):
            case_thumbnail = item.find('img').attrs['src']
        embed = discord.Embed(
            title = row[1],
            colour = discord.Colour.blue(),
            url = case_url
        )
        embed.set_thumbnail(url=str(case_thumbnail))
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