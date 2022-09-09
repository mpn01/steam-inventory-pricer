# <p align="center"> 💰 Steam Inventory Pricer </p>

## 📖 Description
A program written in Python to monitor your prices of your CS:GO items. This program is working as an Discord BOT.

## 💻 Usage
To use this program you need to create SQLite database and complete it with your CS:GO items. For now, it's the only way it works. Then you need to configure your Discord BOT. I'm not providing it for you.

There are two commands to use, `.skins` and `.cases`. I don't need to explain which do what.

## 🛑 Limitations

This version of Steam API is limited to few API calls. This may stop program in the middle. Also, if you call API a lot in a short time you will be banned by Valve for a few minutes.

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
```

## 📜 Todo

#### Rewrite API calls to diffrent API
#### Fetch items from Steam Inventory to avoid adding them manually


## ©️ Credits
