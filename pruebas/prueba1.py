import sqlite3

with sqlite3.connect("PRUEBA.db") as con:
    select = con.execute("SELECT * FROM usuarios WHERE username=\"luis3\"")
    print(len(select.fetchall()))
