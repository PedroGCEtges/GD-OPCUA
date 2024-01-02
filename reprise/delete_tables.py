import sqlite3

from time_normalizer import get_cursor_and_conn

def delete_tables(cursor,bools=False):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")

    names = cursor.fetchall()

    for name in names:
        if 'opcua_data' == name[0]:
            if bools == True:
                cursor.execute(f"DROP TABLE \"{name[0]}\"")
            print(name[0])
        else:
            cursor.execute(f"DROP TABLE \"{name[0]}\"")
    


# cursor, conn = get_cursor_and_conn("PickAndPlace.db")

# delete_tables(cursor=cursor,yes=True)