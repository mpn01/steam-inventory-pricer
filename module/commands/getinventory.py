import requests
import sqlite3
user_steam_id = 76561198144159412

def getInventory():
    conn = sqlite3.connect("../steaminventory.db")

    response = requests.get(f"https://steamcommunity.com/inventory/{user_steam_id}/730/2?l=english&count=1000").json()
    inventory_count = response["total_inventory_count"]

    for x in range(inventory_count-1):
        player_item_type = response["descriptions"][x]["type"]
        if player_item_type != "Extraordinary Collectible" and player_item_type != "Stock Pistol" and player_item_type != "Stock Rifle" and player_item_type != "Base Grade Tool":
            print(response["descriptions"][x]["market_hash_name"])

getInventory()