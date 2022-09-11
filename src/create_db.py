import sqlite3

conn = sqlite3.connect("steminventory.db")

with conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS skins (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            quantity INTEGER,
            img TEXT
        );
    """)
    conn.commit()

with conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            quantity INTEGER,
            img TEXT
        );
    """)
    conn.commit()
