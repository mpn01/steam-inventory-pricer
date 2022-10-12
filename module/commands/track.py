import sqlite3

def changeStatus(user_input, table, status):
    conn = sqlite3.connect('steaminventory.db')
    sql_query_select = f"SELECT name FROM {table} WHERE name LIKE '%{user_input}%'"
    result = conn.execute(sql_query_select)
    for row in result:
        case_name = row[0]
    sql_query_update = f"UPDATE {table} SET status='{status}' WHERE name='{case_name}';"
    conn.execute(sql_query_update)
    conn.commit()

    return case_name