import sqlite3 as lite

con = lite.connect('server/log.db')

with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE Messages(Id INTEGER PRIMARY KEY AUTOINCREMENT , Sender TEXT, Receiver TEXT, Text TEXT, Date DATE)")