import requests
import re
import sqlite3
import urllib.parse
import eel

# Operation on database

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

@eel.expose
def getSkinPrices():
    with conn:
        result = conn.execute("SELECT * FROM skins;")
        sum = 0
        skins_value = []
        for row in result:
            # Fetch and display data from Steam market
            response = requests.get("http://steamcommunity.com/market/priceoverview/?appid=730&currency=6&market_hash_name="+row[1]).json()
            price = response["lowest_price"]
            price_int = re.sub('[^\d+,\d{0,2}$]', '', price)
            price_formated = float(price_int.replace(',','.'))
            print(row[1], "=>", price_formated, "zł", "|", price_formated*row[2],"zł")
            skins_value.append(price_formated*row[2])
            # old_price = conn.execute("SELECT price_new FROM skins")
            # for price in old_price:
            #     sql_update_prices = ("UPDATE skins SET price_old = ? WHERE name = ?")
            #     data_update_prices = [price, row[1]]
            #     conn.execuute(sql_update_prices, data_update_prices)
            #     conn.commit()
            # # Update database with new price
            # sql = "UPDATE skins SET price_new = ? WHERE name = ?"
            # data = [price_formated, row[1]]
            # conn.execute(sql, data)
            # conn.commit()
        for i in range(0,len(skins_value)):
            sum = round(sum + skins_value[i], 2)
        print("Total value:", str(sum), "zł")
    return(skins_value, sum)

def getCasePrices():
    result = conn.execute("SELECT * FROM cases;")
    sum = 0
    cases_value = []
    for row in result:
        response = requests.get("http://steamcommunity.com/market/priceoverview/?appid=730&currency=6&market_hash_name="+row[1]).json()
        price = response["lowest_price"]
        price_int = re.sub('[^\d+,\d{0,2}$]', '', price)
        price_formated = float(price_int.replace(',','.'))
        print(row[1],"=>", price_formated, "zł", "|", round(price_formated*row[2], 2), "zł")
        cases_value.append(price_formated*row[2])
    for i in range(0,len(cases_value)):
        sum = round(sum + cases_value[i], 2)
    print("Total value:", str(sum), "zł")


if __name__ == "__main__":
    conn = sqlite3.connect('steaminventory.db')
    eel.init('web')
    eel.start('index.html', size=(1024,640))