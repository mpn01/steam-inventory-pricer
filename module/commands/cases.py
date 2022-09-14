import sqlite3
import requests
import re
import urllib.parse
from bs4 import BeautifulSoup

def getCasePrices():
    conn = sqlite3.connect('steaminventory.db')
    result = conn.execute("SELECT * FROM cases;")

    for row in result:
        response = requests.get("http://steamcommunity.com/market/priceoverview/?appid=730&currency=6&market_hash_name="+row[1]).json()
        price = response["lowest_price"]
        price_int = re.sub('[^\d+,\d{0,2}$]', '', price)
        price_formated = float(price_int.replace(',','.'))
        sum_price = round(price_formated*row[2], 2)
        # print(row[1], "=>", price_formated, "zł", "|", round(price_formated*row[2], 2), "zł")
        case_row = urllib.parse.quote(row[1])
        case_url = "https://steamcommunity.com/market/listings/730/"+case_row
        img_url = requests.get(case_url)
        soup = BeautifulSoup(img_url.text, 'html.parser')
        for item in soup.select('.market_listing_largeimage'):
            case_thumbnail = item.find('img').attrs['src']
        
        yield row[1], case_url, case_thumbnail, row[2], price_formated, sum_price