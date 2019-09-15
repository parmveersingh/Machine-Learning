import sqlite3 as sq
con=sq.connect('connection.db')
cur=con.cursor()
cars = (
    (1, 'Audi', 52642),
    (2, 'Mercedes', 57127),
    (3, 'Skoda', 9000),
    (4, 'Volvo', 29000),
    (5, 'Bentley', 350000),
    (6, 'Hummer', 41400),
    (7, 'Volkswagen', 21600)
)
""" cur.execute('CREATE TABLE cars(id INT,name TEXT,price INT)') """
cur.execute('INSERT INTO cars VALUES(1,"Buggati",2343)')
cur.execute('INSERT INTO cars VALUES(1,"Audi",2323)')
cur.executemany('INSERT INTO cars VALUES(?,?,?)',cars)
con.commit()
con.close()
