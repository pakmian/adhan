import os
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def DeleteTableData():
    database = r"/home/pi/adhan/Quran.db"
    # Create a database connection
    conn = create_connection(database)
    with conn:
        #
        cur = conn.cursor()
        cur.execute('DELETE FROM QuranTask')
    conn.commit()

def UpdateQuranPaths(ID, FileName, Check):
    database = r"/home/pi/adhan/Quran.db"
    # Create a database connection
    conn = create_connection(database)
    with conn:
        #
        cur = conn.cursor()
        cur.execute('INSERT INTO QuranTask(ID, LOCATION, CHECKED) VALUES(?,?,?)',(ID, FileName, Check))
    conn.commit()

# List all files in a directory using scandir()
basepath = '/home/pi/adhan/quran'
DeleteTableData()
with os.scandir(basepath) as entries:
    # Sort filenames and store in a new variable arr
    arr = sorted(entries, key=lambda x:(x.is_file(), x.name))
    a = 0;
    for entry in arr:
        if entry.is_file():
            print(entry.name)
            UpdateQuranPaths(a, entry.name, 0)
            a = a + 1
