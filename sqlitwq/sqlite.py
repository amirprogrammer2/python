import sqlite3
from sqlite3 import Error

con = sqlite3.connect("mydb.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS amir_programmer (id INTEGER PRIMARY KEY  , name TEXT, age INTEGER )")
cur.execute("INSERT INTO amir_programmer(id,name,age ) VALUES(1,'amir',18)")
con.commit()
con.close()