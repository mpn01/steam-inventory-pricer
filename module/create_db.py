import sqlite3

conn = sqlite3.connect("steamsinventory.db")
conn.execute("CREATE TABLE IF NOT EXISTS skins (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,name TEXT,quantity INTEGER);")
conn.execute("CREATE TABLE IF NOT EXISTS cases (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,name TEXT,quantity INTEGER);")
conn.commit()
print("Database created!")


