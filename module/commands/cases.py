import sqlite3
import requests
import re
import urllib.parse
from bs4 import BeautifulSoup

def getCases(all_cases, query):
    conn = sqlite3.connect('steaminventory.db')
    result = conn.execute(query)
    for row in result:
        case_name = row[1]
        case_quantity = row[2]
        case_status = row[3]
        case_quoted = urllib.parse.quote(case_name)
        case_url = "https://steamcommunity.com/market/listings/730/"+case_quoted
        img_url = requests.get(case_url)
        soup = BeautifulSoup(img_url.text, 'html.parser')

        for item in soup.select('.market_listing_largeimage'):
            case_thumbnail = item.find('img').attrs['src']

        response = requests.get(f"http://steamcommunity.com/market/priceoverview/?appid=730&currency=6&market_hash_name={case_quoted}").json()
        case_current_price = response["lowest_price"]
        case_int_price = re.sub('[^\d+,\d{0,2}$]', '', case_current_price)
        case_formated_price = float(case_int_price.replace(',','.'))
        case_sum_price = round(case_formated_price*case_quantity, 2)

        if all_cases == True: yield case_name, case_quantity, case_url, case_thumbnail, case_formated_price, case_sum_price
        if all_cases == False: yield case_name, case_quantity, case_status, case_url, case_formated_price, case_sum_price, case_thumbnail

