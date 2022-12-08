#!/usr/bin/python

# This section works with sqlite3 database
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def nextFilePath():
    database = r"/home/pi/adhan/Quran.db"
    # create a database connection
    conn = create_connection(database)
    with conn:
        #print("List all records:")
        cur = conn.cursor()
        cur.execute("SELECT * FROM QuranTask WHERE CHECKED = 0")
        rows = cur.fetchall()
        #QPath = (rows[0][0])
        QID = (rows[0][0])
        QPath = (rows[0][1])
        cur.execute("UPDATE QuranTask SET CHECKED = 1 WHERE ID = "+str(QID)+"")
        if (QID == 83):
            cur.execute("UPDATE QuranTask SET CHECKED = 0")
            print (str(QID))

        #print (rows[0][1])
        #for row in rows:
        #    print(row[0])
    return QPath

### Function currently not in use ###
def getFilePathByID(FileID):
    database = r"/home/pi/adhan/Quran.db"
    # create a database connection
    conn = create_connection(database)
    with conn:
        #print("List all records:")
        cur = conn.cursor()
        cur.execute("SELECT Location FROM QuranTask WHERE ID = " + FileID + "")
        rows = cur.fetchall()
        QPath = (rows[0][0])
        #print (rows[0][0])
        #for row in rows:
        #    print(row[0])
    return QPath

# This section works with a python class and list of class objects
class QuranPath:
    def __init__(self, FileID, Desc, Location):
        self.FileID = FileID
        self.Desc = Desc
        self.Location = Location

# Creating a list
list = []
list.append( QuranPath(1, "Fatiha", "fatiha.mp3"))
list.append( QuranPath(2, "Mariyam", "mariyam.mp3"))
list.append( QuranPath(3, "RahmanMuzzamilMulk", "rahmanmuzzamilmulk.mp3"))
list.append( QuranPath(4, "Yaseen", "yaseen.mp3"))
list.append( QuranPath(5, "Yousuf", "yousuf.mp3"))
list.append( QuranPath(6, "Al-Furqaan", "alfurqaan.mp3"))
list.append( QuranPath(7, "Al-Muzzamil", "almuzzamil.mp3"))
list.append( QuranPath(8, "Al-Rehman", "alrehman.mp3"))

# This section provides two functions to retrieve FilePath and FileDescription saved in above QuranPath list class objects
def FilePath(FileID):
    for obj in list:
        if obj.FileID == FileID:
            Location = obj.Location
    return (Location)

def FileDescription(FileID):
    for obj in list:
        if obj.FileID == FileID:
            Description = obj.Desc
    return (Description)
