import sqlite3
import requests
import re
import urllib.parse
from bs4 import BeautifulSoup

def getSkins(all_skins, query):
    conn = sqlite3.connect('steaminventory.db')
    result = conn.execute(query)
    for row in result:
        skin_name = row[1]
        skin_quantity = row[2]
        skin_status = row[3]
        skin_cost = row[4]
        skin_origin = row[5]
        skin_quoted_name = urllib.parse.quote(skin_name)
        skin_url = "https://steamcommunity.com/market/listings/730/"+skin_quoted_name
        img_url = requests.get(skin_url)
        soup = BeautifulSoup(img_url.text, 'html.parser')

        for item in soup.select('.market_listing_largeimage'):
            skin_thumbnail = item.find('img').attrs['src']

        response = requests.get(f"http://steamcommunity.com/market/priceoverview/?appid=730&currency=6&market_hash_name={skin_quoted_name}").json()
        skin_current_price = response["lowest_price"]
        skin_int_price = re.sub('[^\d+,\d{0,2}$]', '', skin_current_price)
        skin_formated_price = float(skin_int_price.replace(',','.'))
        skin_sum_price = round(skin_formated_price*skin_quantity, 2)
        skin_net_price = round(skin_sum_price*0.8698, 2)

        if all_skins == True: yield skin_name, skin_quantity, skin_url, skin_thumbnail, skin_formated_price, skin_sum_price, skin_net_price
        if all_skins == False: yield skin_name, skin_status, skin_cost, skin_origin, skin_url, skin_formated_price, skin_sum_price, skin_thumbnail, skin_quantity