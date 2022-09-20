import sqlite3

conn = sqlite3.connect("steamsinventory.db")
conn.execute("CREATE TABLE IF NOT EXISTS skins (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,name TEXT,quantity INTEGER, status TEXT, cost REAL, source TEXT);")
conn.execute("CREATE TABLE IF NOT EXISTS cases (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,name TEXT,quantity INTEGER, status TEXT);")
conn.commit()
print("Database created!")


