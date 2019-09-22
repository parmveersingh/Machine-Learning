import sqlite3 as sq
con=sq.connect('connection.db')
cur=con.cursor()
cur.execute('SELECT SQLITE_VERSION()')
data = cur.fetchall()
print data
con.close()
