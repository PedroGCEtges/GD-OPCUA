import sqlite3
import pandas as pd
from datetime import datetime, timedelta

conn = sqlite3.connect("opcua.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")

names = cursor.fetchall()

for name in names:
    if 'opcua_data' == name[0]:
        print(name[0])
    else:
        cursor.execute(f"DROP TABLE \"{name[0]}\"")