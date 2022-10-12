import sqlite3
import urllib.parse

def addCaseToInventory(caseurl : str, quantity : int):
    conn = sqlite3.connect('steaminventory.db')

    caseurl_unquoted = urllib.parse.unquote(caseurl)
    caseurl_unparsed = urllib.parse.urlparse(caseurl_unquoted)
    casename = caseurl_unparsed.path.lstrip("/market/listings/730/")
    data = [casename]
    result = conn.execute("SELECT EXISTS(SELECT quantity FROM cases WHERE name=?);", data)
    fetched_result = result.fetchone()[0]
    if fetched_result == 0:
        casedata = [casename, quantity]
        conn.execute("INSERT INTO cases(name, quantity) values(?,?);", casedata)
        conn.commit()

        yield fetched_result, casename
    elif fetched_result == 1:
        result_quantity = conn.execute("SELECT quantity FROM cases WHERE name=?", data)
        for x in result_quantity:
            quantity_increased = int(quantity) + int(x[0])
            casedata = [quantity_increased, casename]
            conn.execute("UPDATE cases SET quantity=? WHERE name=?;", casedata)
            conn.commit()

            yield fetched_result, casename