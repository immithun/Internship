import sqlite3 as sql
con = sql.connect('database.db')
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS customers")
sql ='''CREATE TABLE "customers" (
	"ID"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"NAME"	TEXT,
	"MOBILE" TEXT UNIQUE,
    "MAIL" TEXT UNIQUE,
    "SUBSCRIPTION" TEXT
)'''
cur.execute(sql)
con.commit()
con.close()