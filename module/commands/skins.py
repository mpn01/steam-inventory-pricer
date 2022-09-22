import sqlite3
import requests
import re
import urllib.parse
from bs4 import BeautifulSoup

def getSkinPrices(all_skins, input):
    conn = sqlite3.connect('steaminventory.db')
    
    if all_skins == True:
        result = conn.execute("SELECT * FROM skins WHERE status='tracked';")
        for row in result:
            skin_name = row[1]
            response = requests.get(f"http://steamcommunity.com/market/priceoverview/?appid=730&currency=6&market_hash_name={skin_name}").json()
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
    else:
        result = conn.execute(f"SELECT * FROM skins WHERE name LIKE '%{input}%';")
        for row in result:
            skin_name = row[1]
            skin_status = row[3]
            skin_cost = row[4]
            skin_origin = row[5]
            response = requests.get(f"http://steamcommunity.com/market/priceoverview/?appid=730&currency=6&market_hash_name={skin_name}").json()
            price = response["lowest_price"]
            price_int = re.sub('[^\d+,\d{0,2}$]', '', price)
            price_formated = float(price_int.replace(',','.'))
            sum_price = round(price_formated*row[2], 2)
            skin_row = urllib.parse.quote(row[1])
            skin_url = "https://steamcommunity.com/market/listings/730/"+skin_row
            img_url = requests.get(skin_url)
            soup = BeautifulSoup(img_url.text, 'html.parser')
            for item in soup.select('.market_listing_largeimage'):
                skin_thumbnail = item.find('img').attrs['src']

            yield skin_name, skin_status, skin_cost, skin_origin