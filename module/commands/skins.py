import sqlite3
import requests
import re
import urllib.parse
from bs4 import BeautifulSoup

def getSkinPrices():
    conn = sqlite3.connect('steaminventory.db')
    result = conn.execute("SELECT * FROM skins;")

    for row in result:
        response = requests.get("http://steamcommunity.com/market/priceoverview/?appid=730&currency=6&market_hash_name="+row[1]).json()
        price = response["lowest_price"]
        price_int = re.sub('[^\d+,\d{0,2}$]', '', price)
        price_formated = float(price_int.replace(',','.'))
        sum_price = round(price_formated*row[2], 2)
        # print(row[1], "=>", price_formated, "zł", "|", round(price_formated*row[2], 2), "zł")
        skin_row = urllib.parse.quote(row[1])
        skin_url = "https://steamcommunity.com/market/listings/730/"+skin_row
        img_url = requests.get(skin_url)
        soup = BeautifulSoup(img_url.text, 'html.parser')
        for item in soup.select('.market_listing_largeimage'):
            skin_thumbnail = item.find('img').attrs['src']

        yield row[1], skin_url, skin_thumbnail, row[2], price_formated, sum_price
