# <p align="center"> 💰 Steam Inventory Pricer </p>

## 📖 Description
A program written in Python to monitor your prices of your CS:GO items. This program is working as an Discord BOT.

## 💻 Usage
To use this program you need to create SQLite database and complete it with your CS:GO items. For now, it's the only way it works. You can use script called `create_db.py` to create it automatically. Then you need to configure your Discord BOT. Simply, just make an .env file and insert your BOT token there, it should look like this:

```env
DISCORD=y0u4t0k3n
```

Then you can run this script by running `python module/core.py` in a console.

There are ten commands to use, `.skins` `.cases` `.addcase` `.addskin` `.removeskin` `.removecase` `.trackskin` `.trackcase` `.untrackskin` and `.untrackcase`. First two commands are displaying every item from inventory. The rest are just operations on database to add/remove items and track/untrack items in daily message which displays current value of your inventory.

Using commands:
#### Displaying info about one item (current price, bought price, item origin and status)
```python
.skins <skin-name>
# Example
.skins Red Laminate
```
#### Adding item(s) to database
```python
.addcase <steam-url-to-skin> <quantity>
# Example
.addcase https://steamcommunity.com/market/listings/730/StatTrak%E2%84%A2%20P250%20|%20Cassette%20(Factory%20New) 1
```
#### Removing item(s) from database
```python
.removeskin <item-name>
# Example
.removeskin P250 Cassette
```
#### Tracking item in daily message
```python
.trackcase <item-name>
# Example
.trackcase Prisma 2 Case
```
#### Untracking item in daily message
```python
.untrackskin <item-name>
# Example
.untrackskin Bright Water
```

## 🛑 Limitations

This version of Steam API is limited to 8 API calls. This may stop program in the middle. Also, if you call API a lot in a short time you will be banned by Valve for a few minutes.

## 📚 Libraries used in this project

```
requests
re
sqlite3
urllib.parse
discord
discord.ext
os
dotenv
datetime
asyncio
```

## 📜 Todo

- [ ] Daily message about inventory value
- [ ] Rewrite API calls to diffrent API
- [ ] Fetch items from Steam Inventory to database
- [ ] Check one item with additional informations (price you paid, purchase date etc.)

