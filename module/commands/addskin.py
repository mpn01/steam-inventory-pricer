import sqlite3
import urllib.parse

def addSkinToInventory(skinurl : str, quantity : int):
    conn = sqlite3.connect('steaminventory.db')

    skinurl_unquoted = urllib.parse.unquote(skinurl)
    skinurl_unparsed = urllib.parse.urlparse(skinurl_unquoted)
    skinname = skinurl_unparsed.path.lstrip("/martket/listings/730/")
    data = [skinname]
    result = conn.execute("SELECT EXISTS(SELECT quantity FROM skins WHERE name=?);", data)
    fetched_result = result.fetchone()[0]
    if fetched_result == 0:
        skindata = [skinname, quantity]
        conn.execute("INSERT INTO skins(name, quantity) values(?,?);", skindata)
        conn.commit()

        yield fetched_result, skinname
    elif fetched_result == 1:
        result_quantity = conn.execute("SELECT quantity FROM skins WHERE name=?", data)
        for x in result_quantity:
            quantity_increased = int(quantity) + int(x[0])
            skindata = [quantity_increased, skinname]
            conn.execute("UPDATE skins SET quantity=? WHERE name=?;", skindata)
            conn.commit()
            yield fetched_result, skinname