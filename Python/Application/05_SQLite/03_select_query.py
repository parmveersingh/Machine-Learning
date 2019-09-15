import sqlite3 as sq
con=sq.connect('connection.db')
con.row_factory = sq.Row
cur=con.cursor()
cur.execute('SELECT * FROM cars')
"""data = cur.fetchall()
for row in data:
    print row

"""

while True:
    dataone = cur.fetchone()
    if dataone == None:
        break
    print dataone['id']
con.close()
