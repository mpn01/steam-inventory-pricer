# <p align="center"> 💰 Steam Inventory Pricer </p>

[bot teaser - skin.webm](https://user-images.githubusercontent.com/33598365/195581988-21c5bede-86f4-4563-b7e2-47d67c5ffbff.webm)

## 📖 Description
A program written in Python to monitor your prices of your CS:GO items. This program is working as an Discord BOT.

## 💻 Usage
To use this program you need to create SQLite database and complete it with your CS:GO items. For now, it's the only way it works. You can use script called `create_db.py` to create it automatically. Then you need to configure your Discord BOT. Simply, just make an .env file and insert your BOT token there, it should look like this:

```env
DISCORD=y0u4t0k3n
```

Then you can run this script by running `python module/core.py` in a console.

There are ten commands to use, `.skins` `.cases` `.addcase` `.addskin` `.removeskin` `.removecase` `.trackskin` `.trackcase` `.untrackskin` and `.untrackcase`. First two commands are displaying every tracked item from inventory. The rest are just operations on database to add/remove items and track/untrack items.

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

I really don't know how the Steam API works. Sometimes you can do only 8 calls, sometimes more. I'm not seeing any pattern there.

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
beautifulsoup4
```

## 📜 Todo

- [ ] Daily message about inventory value
- [ ] Rewrite API calls to diffrent API
- [ ] Fetch items from Steam Inventory and store them in database
- [ ] Add tags support for all items
- [ ] Change commands syntax and prefix (probably to '/')

